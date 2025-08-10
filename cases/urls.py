from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_search, name='case_search'),
    path('details/<int:query_id>/', views.case_details, name='case_details'),
    path('download/<int:order_id>/', views.download_pdf, name='download_pdf'),
    path('history/', views.query_history, name='query_history'),
]
