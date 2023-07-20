from django.db import models

# Create your models here.




class ShortURL(models.Model):
    TABLES = (
        ( 'user_excel_data','User Excel Data'),
        ( 'news','News'),
        ( 'tab_video','Video'),
        ( 'categories','Categories')
    )
    STATUSS = (
        ( 'A','A'),
        ( 'I','I')
    )
    
    code = models.CharField(max_length=30, default="", blank=True)
    tablename = models.CharField(max_length=30, choices=TABLES, default="", blank=True)
    recordid = models.IntegerField(default="", blank=True)
    recordname = models.TextField( default="" )
    status = models.CharField(max_length=1, choices=STATUSS, default='A')

    class Meta:
        db_table = "shortURL"
        unique_together = (('code', 'tablename'),)