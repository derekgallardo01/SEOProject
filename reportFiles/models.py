from django.db import models

# Create your models here.

class ReportFiles(models.Model):
    STATUSS = (
        ( 'A','A'),
        ( 'I','I')
    )
    name = models.CharField(max_length=50, blank=True,null=True,default=None)
    #top_caption = models.TextField(default=None)
    filename = models.FileField(upload_to='report_files/', verbose_name="Upload File", max_length=150, default= '', blank=True)
    #path = models.TextField(default=None)
    status = models.CharField( max_length=1, choices=STATUSS, default='A',)
    section = models.CharField(max_length=150, blank=True,null=True,default=None)

    def index(self, *args, **kwargs):
        response = admin.site.__class__.index(self, *args, **kwargs)
        my_app_context = [d for d in response.context_data['app_list'] if d.get('app_label','') == u'my_app_name']
        if my_app_context:
            for m in my_app_context[0]['models']:
                m['name'] = mark_safe(("<img src='...' /> " + unicode(m['name'])))
        
        return response

    class Meta:
        db_table = 'reportfiles'
        verbose_name = 'Report'
        verbose_name_plural  = 'Reports'



#admin.site.index = index.__get__(admin.site, admin.site.__class__)
