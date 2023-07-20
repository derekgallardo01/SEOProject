# Generated by Django 3.0.2 on 2020-07-13 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesearchresult', '0015_auto_20200710_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='googlesearchresult',
            options={'verbose_name': ' Search Query ', 'verbose_name_plural': ' Search Query'},
        ),
        migrations.AlterModelOptions(
            name='googlesearchresultdata',
            options={'verbose_name': ' Search Query Data', 'verbose_name_plural': ' Search Query Data'},
        ),
        migrations.AddField(
            model_name='googlesearchresultdata',
            name='density_position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='googlesearchresult',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
