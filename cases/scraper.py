import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import time


class CourtScraper:
    """
    Scraper for Indian court case search portals.
    Currently supports Delhi High Court (manual CAPTCHA input).
    """

    def __init__(self, court):
        """
        :param court: Court model-like object with attributes:
                      - name (str)
                      - base_url (str)
        """
        self.court = court
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )
        })

    def fetch_case_data(self, case_type, case_number, filing_year):
        """
        Main entry point.
        Routes the request to the appropriate scraper based on court name.
        """
        court_name = self.court.name.lower()

        if 'delhi high court' in court_name:
            return self._scrape_delhi_high_court(case_type, case_number, filing_year)

        return {
            'success': False,
            'error': f"Unsupported court: {self.court.name}"
        }

    # --------------------
    # Delhi High Court
    # --------------------
    def _scrape_delhi_high_court(self, case_type, case_number, filing_year):
        try:
            base = self.court.base_url.rstrip('/')
            search_url = f"{base}/app/case-number"

            # STEP 1: Fetch the case search form page
            resp = self.session.get(search_url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            form = soup.find('form')
            if not form:
                return {'success': False, 'error': 'Search form not found'}

            # STEP 2: Download CAPTCHA image
            captcha_img = soup.find('img', {'src': re.compile(r'Captcha', re.I)})
            if not captcha_img:
                return {'success': False, 'error': 'Captcha image element not found'}

            captcha_url = urljoin(base, captcha_img['src'])
            cap_resp = self.session.get(captcha_url, timeout=30)
            with open('captcha.jpg', 'wb') as f:
                f.write(cap_resp.content)
            print("Captcha image saved as 'captcha.jpg' — please open and solve it.")

            # STEP 3: Extract hidden fields
            hidden_fields = form.find_all('input', type='hidden')
            form_data = {fld.get('name'): fld.get('value') for fld in hidden_fields if fld.get('name')}

            # STEP 4: Manual CAPTCHA entry
            captcha_text = input("Enter CAPTCHA text: ").strip()

            # STEP 5: Add visible form data
            form_data.update({
                'case_type': case_type,
                'case_number': case_number,
                'case_year': filing_year,
                'captcha_code': captcha_text,
                'submit': 'Submit'
            })

            # STEP 6: Submit the form
            post_url = urljoin(base, form.get('action') or '')
            post_resp = self.session.post(post_url, data=form_data, timeout=30)
            post_resp.raise_for_status()
            result_soup = BeautifulSoup(post_resp.text, 'html.parser')

            # STEP 7: Check if case was found
            if 'no record found' in result_soup.get_text().lower():
                return {'success': False, 'error': 'Case not found'}

            return self._parse_case_details(result_soup)

        except Exception as e:
            return {'success': False, 'error': f'Error during scraping: {e}'}


    def _parse_case_details(self, soup):
        """
        Parses Delhi High Court case details from the result HTML.
        """
        data = {
            'petitioner': '',
            'respondent': '',
            'case_status': '',
            'orders': [],
            'success': True
        }

        # Generic table parsing
        table = soup.find('table')
        if table:
            for tr in table.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    label = tds[0].get_text(strip=True).lower()
                    value = tds[1].get_text(strip=True)
                    if 'petitioner' in label:
                        data['petitioner'] = value
                    elif 'respondent' in label:
                        data['respondent'] = value
                    elif 'status' in label:
                        data['case_status'] = value

        # Extract order PDFs
        for a in soup.find_all('a', href=re.compile(r'\.pdf', re.I)):
            href = a['href']
            full_url = urljoin(self.court.base_url, href)
            data['orders'].append({
                'pdf_url': full_url,
                'description': a.get_text(strip=True) or 'Order PDF'
            })

        return data

    # --------------------
    # Utility HTTP Helpers
    # --------------------
    def _safe_get(self, url, **kwargs):
        """Wrapper for GET with error handling and retries."""
        for attempt in range(3):
            try:
                resp = self.session.get(url, timeout=30, **kwargs)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                print(f"[WARN] GET {url} failed ({e}), retry {attempt+1}/3")
                time.sleep(2)
        return None

    def _safe_post(self, url, **kwargs):
        """Wrapper for POST with error handling and retries."""
        for attempt in range(3):
            try:
                resp = self.session.post(url, timeout=30, **kwargs)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                print(f"[WARN] POST {url} failed ({e}), retry {attempt+1}/3")
                time.sleep(2)
        return None
