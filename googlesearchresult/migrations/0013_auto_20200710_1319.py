# Generated by Django 3.0.2 on 2020-07-10 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesearchresult', '0012_auto_20200703_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlesearchresult',
            name='custom_url_meta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresult',
            name='custom_url_title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='h1_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='h2_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='h3_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='h4_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='h5_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='h6_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='serach_position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='url_meta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='url_title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
