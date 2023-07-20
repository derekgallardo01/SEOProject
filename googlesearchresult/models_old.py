from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
from django.urls import reverse


class googlesearchresult(models.Model):
    search_query = models.TextField(null=True, blank=True)
    custom_url = models.CharField(max_length=255, null=True, blank=True, help_text = 'And a URL you would like to compare the keyword density.  '  )
    location = models.CharField(max_length=255, null=True, blank=True )
    file_path = models.CharField(max_length=150, null=True, blank=True )
    time = models.CharField(max_length=200, null=True, blank=True)
    STATUS =  (('A','Active'),('I','Inactive'))
    status = models.CharField( max_length=1, choices=STATUS, default='A',)

    class Meta:
        db_table = 'google_search_result'
        verbose_name = 'Search Query '
        verbose_name_plural  = 'Search Query'


class googlesearchresultData(models.Model):
    result = models.ForeignKey(googlesearchresult, related_name = 'googlesearchresult', on_delete=models.CASCADE )
    search_url = models.CharField(max_length=255, null=True, blank=True  )
    time = models.CharField(max_length=200, null=True, blank=True)
    keyword_density = models.CharField(max_length=50, null=True, blank=True  )
    url_keyword_density = models.CharField(max_length=50, null=True, blank=True  )

    class Meta:
        db_table = 'google_search_result_data'
        verbose_name = 'Search Query Data'
        verbose_name_plural  = 'Search Query Data'