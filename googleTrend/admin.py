from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import googleTrend
# Register your models here.
from django.forms import forms
from django.template import Template
from django.conf import settings
from django.core import serializers
from django.conf.urls import url
#from django.template.response import TemplateResponse
from django.template.response import TemplateResponse


class GoogleTrendAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['show_report', 'id', 'name', 'filename', 'view_link']
    fieldsets = (
        (None, {
            'fields': ('name', 'filename', 'query_content' ),
            'description': "<h3>Add Query Content or file for trending data. </h3>."
        }),
    )
    
    def view_link(self,obj):
        return format_html("<a href='%d/change'>Edit</a>" % obj.id)
    view_link.short_description = 'Edit link'
    view_link.allow_tags = True
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_delete': False,
            'show_save_and_add_another': False,
            'show_addanother': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>Download Trending Report</a>", url='/google/trends?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Rising Report</a>", url='/google/keyword-rising?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Top Related Report</a>", url='/google/related-query/?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Suggestions Report</a>", url='/google/suggestions-keyword?recid='+str(obj.id))
    
    show_report.short_description = "Create Report"

    def get_urls(self):

        # get the default urls
        urls = super(GoogleTrendAdmin, self).get_urls()

        # define security urls
        files_urls = [
            url(r'^files/$', self.admin_site.admin_view(self.fileslist),name='files')
            # Add here more urls if you want following same logic
        ]

        '''files_urls =  patterns('',
           url(r'^files/$', self.admin_site.admin_view(self.fileslist),name='home'), 
        )'''

        # Make sure here you place your added urls first than the admin default urls
        return files_urls + urls
    
    #admin.autodiscover()

    def change_view(self, request, object_id=None, form_url='',
                extra_context=None):
        # get the default template response
        template_response = super().change_view(request, object_id, form_url,
                                                extra_context)
        # here we simply hide the div that contains the save and delete buttons
        template_response.content = template_response.rendered_content.replace(
            '<div class="submit-row">',
            '<div class="submit-row" style="display: none">')
        return template_response

    class Media:
          js = ('admin/google_trend.js',)

    # Your view definition fn
    def fileslist(self, request):

        
        plugin_name = 'Google Trend'

        title = ("Cannot delete %(name)s") % {"name": plugin_name}

        context = {
            "title": 'File Listing',
            "object_name": plugin_name,
            "object": 'Get Data',
            "deleted_objects": 'deleted_objects',
            "perms_lacking": 'perms_needed',
            "protected": 'protected',
            "opts": 'opts',
            "app_label": 'opts.app_label'
        }
        request.current_app = self.admin_site.name

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           #key=value,
           title= 'File Listing',
           object_name= plugin_name,
           object= 'Get Data',
           deleted_objects= 'deleted_objects',
           perms_lacking= 'perms_needed',
           protected= 'protected',
           opts= 'opts',
           app_label= 'opts.app_label'
        )
        return TemplateResponse(request, "admin/googleTrend/googletrend/configuration.html", context)

        #response =  render(request, "admin/googleTrend/googletrend/configuration.html", {})
        #response.add_post_render_callback(my_render_callback)
        return response





admin.site.register(googleTrend,GoogleTrendAdmin)

