# Generated by Django 3.0.2 on 2020-07-10 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesearchresult', '0014_auto_20200710_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='googlesearchresult',
            name='status',
        ),
        migrations.RemoveField(
            model_name='googlesearchresult',
            name='time',
        ),
        migrations.AddField(
            model_name='googlesearchresult',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2020-07-07 01:01:01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlesearchresult',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
