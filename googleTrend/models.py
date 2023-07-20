from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


class googleTrend(models.Model):
    STATUS =  (('A','Active'),('I','Inactive'))
    name = models.CharField(verbose_name="File Title", max_length=150, default= '', blank=True)
    filename = models.FileField(upload_to='trend_files/', verbose_name="Upload File", max_length=150, default= '', blank=True)
    #status = models.CharField(choices=STATUS, max_length=1, default= '', blank=True)
    #time = models.TimeField(max_length=150, default= '', blank=True)
    query_content = models.TextField( default= '', blank=True)
    
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.filename == '' and self.query_content == '':
            raise ValidationError('Please add query or upload file.')

    class Meta:
        #db_table = 'reportfiles'
        verbose_name = 'Report'
        verbose_name_plural  = 'Reports'
    

    