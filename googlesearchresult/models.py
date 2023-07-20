from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
from django.urls import reverse


class googlesearchresult(models.Model):
    search_query = models.TextField(null=True, blank=True)
    custom_url = models.CharField(max_length=255, null=True, blank=True, help_text = 'And a URL you would like to compare the keyword density.  ' + ' You must include http:// or https://'  )
    location = models.CharField(max_length=255, null=True, blank=True )
    file_path = models.CharField(max_length=150, null=True, blank=True )
    custom_url_title = models.TextField(null=True, blank=True)
    custom_url_meta = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'google_search_result'
        verbose_name = ' Search Query '
        verbose_name_plural  = ' Search Query'


class googlesearchresultData(models.Model):
    result = models.ForeignKey(googlesearchresult, related_name = 'googlesearchresult', on_delete=models.CASCADE )
    search_url = models.CharField(max_length=255, null=True, blank=True  )
    time = models.CharField(max_length=200, null=True, blank=True)
    keyword_density = models.CharField(max_length=50, null=True, blank=True, help_text = 'And ' )
    individual_keyword_density = models.CharField(max_length=50, null=True, blank=True, help_text = 'And  lkjflkfjkldsjfjdskfjkldjf'  )
    url_keyword_density = models.CharField(max_length=50, null=True, blank=True  )
    file_path = models.CharField(max_length=150, null=True, blank=True )
    search_position = models.IntegerField(null=True, blank=True )
    density_position = models.IntegerField(null=True, blank=True )
    h1_tag = models.FloatField(null=True, blank=True)
    h2_tag = models.FloatField(null=True, blank=True)
    h3_tag = models.FloatField(null=True, blank=True)
    h4_tag = models.FloatField(null=True, blank=True)
    h5_tag = models.FloatField(null=True, blank=True)
    h6_tag = models.FloatField(null=True, blank=True)
    url_title = models.FloatField(null=True, blank=True)
    url_meta = models.FloatField(null=True, blank=True)
    all_title = models.FloatField(null=True, blank=True)
    bodytext = models.FloatField(null=True, blank=True)
    suggest_key = models.TextField(null=True, blank=True)
    suggest_key_density = models.FloatField(null=True, blank=True)
    tagstatus = models.IntegerField(null=True, blank=True )

    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms
        
    class Meta:
        db_table = 'google_search_result_data'
        verbose_name = ' Search Query Data'
        verbose_name_plural  = ' Search Query Data'

    

class keywordDensity(models.Model):
    rec = models.ForeignKey(googlesearchresultData, related_name = 'googlesearchresultData', on_delete=models.CASCADE )
    keyword = models.CharField(max_length=255, null=True, blank=True  )
    count = models.CharField(max_length=50, null=True, blank=True  )
    keyword_density = models.CharField(max_length=50, null=True, blank=True  )

    class Meta:
        db_table = 'keyword_density'
        verbose_name = 'Keyword Density'
        verbose_name_plural  = 'Keyword Density'