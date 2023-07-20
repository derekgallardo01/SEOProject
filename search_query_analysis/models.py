from django.db import models

# Create your models here.


class SearchQueryAlalysis(models.Model):
    STATUSS = (
        ( 'A','A'),
        ( 'I','I')
    )
    title = models.CharField(max_length=50, blank=True,null=True,default=None)
    description = models.TextField(blank=True,null=True,default=None)
    input_data = models.FileField(upload_to='query_analysis_files/', verbose_name="Input Data File",  max_length=150, default= '', blank=True, help_text='Upload CSV file for Input Data')
    lookup_words_no_convs = models.FileField(upload_to='query_analysis_files/', verbose_name="Lookup Words No Convs", max_length=150, default= '', blank=True, help_text='Upload CSV file for Lookup Words No Convs')
    status = models.CharField( max_length=1, choices=STATUSS, default='A',)
    
    def index(self, *args, **kwargs):
        response = admin.site.__class__.index(self, *args, **kwargs)
        my_app_context = [d for d in response.context_data['app_list'] if d.get('app_label','') == u'my_app_name']
        if my_app_context:
            for m in my_app_context[0]['models']:
                m['name'] = mark_safe(("<img src='...' /> " + unicode(m['name'])))
        
        return response

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title

    class Meta:
        db_table = 'search_query_analysis'
        verbose_name = 'Report'
        verbose_name_plural  = 'Reports'
        #ordering = ['-my_field_name']