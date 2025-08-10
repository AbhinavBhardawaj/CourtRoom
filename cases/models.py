from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here. 

User = get_user_model()
class Court(models.Model):
    '''store info about diff courts'''
    name = models.CharField(max_length=200)
    base_url = models.URLField()
    court_type = models.CharField(max_length=50, choices=[
        ('High','High Court'),
        ('District', 'District Court'),
        ('Supreme','Supreme Court'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CaseQuery(models.Model):
    '''Stores each case quey'''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_case_queries')
    court = models.ForeignKey(Court, on_delete=models.CASCADE,  related_name='court_case_queries')
    case_type = models.CharField(max_length=100)
    case_number = models.CharField(max_length=100)
    filing_year = models.IntegerField()
    query_timestamp = models.DateTimeField(default=timezone.now)
    raw_response = models.TextField(blank=True) #store raw html/jsn resp
    status = models.CharField(max_length=20, choices=[
        ('SUCCESS','Success'),
        ('FAILED','Failed'),
        ('CAPTCHA_REQUIRED','CAPTCHA Required'),
        ('NOT_FOUND','Case Not Found'),
    ], default='SUCCESS')

    class Meta:
        ordering = ['-query_timestamp']
    
    def __str__(self):
        return f"{self.case_type}/{self.case_number}/{self.filing_year}-{self.court.name}"
    
class CaseMetadata(models.Model):
    '''stores parsed case info'''
    query = models.OneToOneField(CaseQuery, on_delete=models.CASCADE, related_name='metadata')
    petitioner = models.TextField(blank=True)
    respondent = models.TextField(blank=True)
    filing_date = models.DateField(null=True,blank=True)
    next_hearing_date = models.DateField(null=True,blank=True)
    case_status = models.CharField(max_length=100,blank=True)
    judge = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return f"Metadata for {self.query}"

class OrderJudgment(models.Model):
    '''store order/judgment pdf link and details'''
    case_metadata = models.ForeignKey(CaseMetadata, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(null=True, blank=True)
    order_type = models.CharField(max_length=50, choices=[
        ('ORDER', 'Order'),
        ('JUDGMENT', 'Judgment'),
        ('NOTICE', 'Notice'),
        ('OTHER', 'Other'),        
    ])
    pdf_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_latest = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-order_date']
    
    def __str__(self):
        return f"{self.order_type} - {self.order_date}"