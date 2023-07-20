# Generated by Django 3.0.2 on 2020-05-25 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default=None)),
                ('link', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('top_caption', models.TextField(default=None)),
                ('bottom_caption', models.TextField(default=None)),
                ('type', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('type_id', models.IntegerField(blank=True, null=True)),
                ('path', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('alt_text', models.TextField(default=None)),
                ('ord', models.FloatField(default=None)),
                ('status', models.CharField(choices=[('A', 'A'), ('I', 'I')], default='I', max_length=1)),
                ('uploaderid', models.IntegerField(blank=True, null=True)),
                ('userid', models.IntegerField(blank=True, null=True)),
                ('image_section', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('img_section_category', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('date_time', models.DateField(blank=True, default=None, null=True, verbose_name='Date')),
                ('created_at', models.DateField(blank=True, default=None, null=True, verbose_name='Date')),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateField(blank=True, default=None, null=True, verbose_name='Date')),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateField(blank=True, default=None, null=True, verbose_name='Date')),
                ('upload_ip', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('upload_server_data', models.TextField(default=None)),
                ('user_type', models.CharField(blank=True, default=None, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Images',
                'db_table': 'images',
            },
        ),
    ]
