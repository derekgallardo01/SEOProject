from django.contrib import admin
from .models import Images
# Register your models here.
from django.forms import forms
from django.template import Template
from django.conf import settings
from django.core import serializers
import json
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe


class ImagesAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ('name','all_actions')
    search_fields = ('name',)
    list_display_links = ('all_actions',)

    def all_actions(self,obj):
        return mark_safe('<span class="changelink">Edit</span>')
    all_actions.short_description = 'actions'

    



admin.site.register(Images,ImagesAdmin)

