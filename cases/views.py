from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import CaseSearchForm
from .models import CaseQuery, CaseMetadata, OrderJudgment, Court
from .scraper import CourtScraper  # We'll create this next
import requests

def case_search(request):
    """Main case search form view with CAPTCHA handling"""
    form = CaseSearchForm()
    
    if request.method == 'POST':
        form = CaseSearchForm(request.POST)
        if form.is_valid():
            # Create query record
            query = CaseQuery.objects.create(
                user=request.user if request.user.is_authenticated else None,
                court=form.cleaned_data['court'],
                case_type=form.cleaned_data['case_type'],
                case_number=form.cleaned_data['case_number'],
                filing_year=form.cleaned_data['filing_year']
            )
            
            try:
                scraper = CourtScraper(query.court)
                result = scraper.fetch_case_data(
                    case_type=query.case_type,
                    case_number=query.case_number,
                    filing_year=query.filing_year
                )
                
                if result['success']:
                    # Save successful result
                    query.status = 'SUCCESS'
                    query.raw_response = result.get('raw_response', '')
                    query.save()
                    
                    # Create metadata
                    metadata = CaseMetadata.objects.create(
                        query=query,
                        petitioner=result.get('petitioner', ''),
                        respondent=result.get('respondent', ''),
                        filing_date=result.get('filing_date'),
                        next_hearing_date=result.get('next_hearing_date'),
                        case_status=result.get('case_status', ''),
                        judge=result.get('judge', '')
                    )
                    
                    # Create orders
                    for order in result.get('orders', []):
                        OrderJudgment.objects.create(
                            case_metadata=metadata,
                            order_date=order.get('date'),
                            order_type=order.get('type', 'ORDER'),
                            pdf_url=order.get('pdf_url', ''),
                            description=order.get('description', ''),
                            is_latest=order.get('is_latest', False)
                        )
                    
                    return redirect('case_details', query_id=query.id)
                
                elif 'captcha' in result.get('error', '').lower():
                    query.status = 'CAPTCHA_REQUIRED'
                    query.save()
                    messages.warning(request, 
                        "CAPTCHA is required for this search. "
                        "This is a known limitation. Please try again or use a different case number."
                    )
                else:
                    query.status = 'FAILED'
                    query.save()
                    messages.error(request, f"Search failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                query.status = 'FAILED'
                query.save()
                messages.error(request, f"Technical error: {str(e)}")
    
    return render(request, 'cases/search.html', {'form': form})

def case_details(request, query_id):
    """Display case details"""
    query = get_object_or_404(CaseQuery, id=query_id)
    
    context = {
        'query': query,
        'metadata': getattr(query, 'metadata', None),
        'orders': query.metadata.orders.all() if hasattr(query, 'metadata') else []
    }
    
    return render(request, 'cases/details.html', context)

def download_pdf(request, order_id):
    """Download PDF file"""
    order = get_object_or_404(OrderJudgment, id=order_id)
    
    if not order.pdf_url:
        messages.error(request, "PDF URL not available")
        return redirect('case_details', query_id=order.case_metadata.query.id)
    
    try:
        response = requests.get(order.pdf_url, timeout=30)
        response.raise_for_status()
        
        http_response = HttpResponse(response.content, content_type='application/pdf')
        filename = f"order_{order.id}_{order.order_date or 'unknown'}.pdf"
        http_response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return http_response
    except Exception as e:
        messages.error(request, f"Error downloading PDF: {str(e)}")
        return redirect('case_details', query_id=order.case_metadata.query.id)

def query_history(request):
    """Show user's query history"""
    queries = CaseQuery.objects.all()
    if request.user.is_authenticated:
        queries = queries.filter(user=request.user)
    
    return render(request, 'cases/history.html', {'queries': queries[:50]})  # Limit to 50
