from django.contrib import admin
from .models import Court, CaseQuery, CaseMetadata, OrderJudgment

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'court_type', 'is_active']
    list_filter = ['court_type', 'is_active']
    search_fields = ['name']

@admin.register(CaseQuery)
class CaseQueryAdmin(admin.ModelAdmin):
    list_display = ['case_type', 'case_number', 'filing_year', 'court', 'status', 'query_timestamp']
    list_filter = ['status', 'court', 'query_timestamp']
    search_fields = ['case_number', 'case_type']
    readonly_fields = ['query_timestamp']

@admin.register(CaseMetadata)
class CaseMetadataAdmin(admin.ModelAdmin):
    list_display = ['query', 'filing_date', 'next_hearing_date', 'case_status']

@admin.register(OrderJudgment)
class OrderJudgmentAdmin(admin.ModelAdmin):
    list_display = ['case_metadata', 'order_date', 'order_type', 'is_latest']
    list_filter = ['order_type', 'is_latest']
