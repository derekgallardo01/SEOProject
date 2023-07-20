from django.contrib import admin
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.
from .models import SearchQueryAlalysis

class SearchQueryAlalysisAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('show_report', 'title', 'description', 'all_actions')
    search_fields = ('title', 'description', )
    list_display_links = ('all_actions',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'input_data', 'lookup_words_no_convs'),
            'description': "<h3>Need to add title and description and files as well</h3>."
        }),
    )

    #actions = ['bad_to_ok', 'no_conversion', 'converted_found', '']
    #format_html("<br /><br /><a target='_blank' href='{url}'>Converted</a>", url='/google/keyword-rising?recid='+str(obj.id))+

    def show_report(self, obj):
        return format_html("Download Below Reports <br /><br /><a target='_blank' href='{url}'>Not Converted</a>", url='/keyword-analysis/no-conversion?recid='+str(obj.id))+format_html("<br /><br /> <a target='_blank' href='{url}'>Bad To OK</a>", url='/keyword-analysis/bad-to-ok?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Converted And found in Console</a>", url='/keyword-analysis/converted-found/?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Converted but Not found in Console</a>", url='/keyword-analysis/converted-not-found?recid='+str(obj.id))
    
    

    def all_actions(self,obj):
        return mark_safe('<span class="changelink">Edit</span>')
    all_actions.short_description = 'actions'

    class FilesInline(admin.StackedInline):
        model = SearchQueryAlalysis
        extra = 1
        
    
    def bad_to_ok(self, request, queryset):
        books = queryset.values_list('id','filename')

        
        

admin.site.register(SearchQueryAlalysis, SearchQueryAlalysisAdmin)




