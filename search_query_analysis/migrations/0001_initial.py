# Generated by Django 3.0.2 on 2020-06-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQueryAlalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('input_data', models.FileField(blank=True, default='', max_length=150, upload_to='query_analysis_files/', verbose_name='Upload File')),
                ('lookup_words_no_convs', models.FileField(blank=True, default='', max_length=150, upload_to='query_analysis_files/', verbose_name='Upload File')),
                ('status', models.CharField(choices=[('A', 'A'), ('I', 'I')], default='A', max_length=1)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
                'db_table': 'search_query_analysis',
            },
        ),
    ]
