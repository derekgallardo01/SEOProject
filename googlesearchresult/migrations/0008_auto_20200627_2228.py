# Generated by Django 3.0.2 on 2020-06-27 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesearchresult', '0007_auto_20200627_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlesearchresult',
            name='file_path',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='googlesearchresult',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]