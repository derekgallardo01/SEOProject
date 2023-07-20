from django.db import models

# Create your models here.

class Images(models.Model):
    STATUSS = (
        ( 'A','A'),
        ( 'I','I')
    )
    name = models.TextField(default=None)
    link = models.CharField(max_length=150, blank=True,null=True,default=None)
    top_caption = models.TextField(default=None)
    bottom_caption = models.TextField(default=None)
    type = models.CharField(max_length=100, blank=True,null=True,default=None)
    type_id = models.IntegerField(blank=True,null=True)
    path = models.CharField(max_length=255, blank=True,null=True,default=None)
    height = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    alt_text = models.TextField(default=None)
    ord = models.FloatField(default=None)
    status = models.CharField( max_length=1, choices=STATUSS, default='I',)
    uploaderid = models.IntegerField(blank=True,null=True)
    userid = models.IntegerField(blank=True,null=True)
    image_section = models.CharField(max_length=30, blank=True,null=True,default=None)
    img_section_category = models.CharField(max_length=30, blank=True,null=True,default=None)
    date_time = models.DateField(("Date"),blank=True,null=True,default=None)
    created_at = models.DateField(("Date"),blank=True,null=True,default=None)
    created_by = models.IntegerField(blank=True,null=True)
    updated_at = models.DateField(("Date"),blank=True,null=True,default=None)
    updated_by = models.IntegerField(blank=True,null=True)
    deleted_by = models.IntegerField(blank=True,null=True)
    deleted_at = models.DateField(("Date"),blank=True,null=True,default=None)
    upload_ip = models.CharField(max_length=50, blank=True,null=True,default=None)
    upload_server_data = models.TextField(default=None)
    user_type = models.CharField(max_length=20, blank=True,null=True,default=None)


    class Meta:
        db_table = "images"
        verbose_name_plural = "Images"