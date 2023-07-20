from django.contrib import admin

from .models import ReportFiles

from django.forms import forms
from django.template import Template
from django.conf import settings
from django.core import serializers
import json
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import datetime
from django.utils import timezone
import time
import pandas as pd
import numpy as np
import os
import csv
from openpyxl import Workbook


class ReportFilesAdmin(admin.ModelAdmin):
    list_per_page = 20
    template_name = "profiles/user_profile.html"
    #fields = ['name','section']
    #formfield_overrides = ['name','section']
    fieldsets = (
        (None, {
            'fields': ('section','filename'),
        }),
    )
    list_display = ('name','section','all_actions')
    search_fields = ('name',)
    list_display_links = ('all_actions',)

    actions = ['merge_files', ]

    def all_actions(self,obj):
        return mark_safe('<span class="changelink">Edit</span>')
    all_actions.short_description = 'actions'

    class FilesInline(admin.StackedInline):
        model = ReportFiles
        extra = 1
        
    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('file_field')
        
        #return HttpResponse('ggg')
        for afile in request.FILES.getlist('files_multiple'):
            newdoc = ReportFiles(filename = afile, name = afile, section = request.POST["section"])
            newdoc.save()
            
            #obj.afile.path
            #obj.save()

    def merge_files(self, request, queryset):
        books = queryset.values_list('id','filename')
        for file in books:
            print(file[1])
            recid = file[0]
            csvdata = ReportFiles.objects.filter(pk=recid)
            
            filename = csvdata[0].filename
            #return HttpResponse('dddd')

            timenow = timezone.now().strftime('%Y%m%d%H%M%S')
            #filename = settings.FILES_ROOT +'google-trend-data'+ str(timenow)+'.csv'
            filename = settings.MEDIA_ROOT + str(filename)

            #data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
            wb = Workbook()

            # grab the active worksheet
            ws = wb.active

            with open(filename) as f:
                reader = csv.reader(f)
                for row in reader:
                    ws.append(row)

            #result.to_csv(filename, index = False)
            # Data can be assigned directly to cells
            #ws['A1'] = 42

            # Rows can also be appended
            #ws.append([1, 2, 3])

        # Python types will automatically be converted
        filename = settings.FILES_ROOT +'all_files_workbook'+ str(timenow)+'.xlsx'
        
        # Save the file
        wb.save(filename)

        '''
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
            return response
        '''

        #queryset.update(order_status=Order.CANCELLED)
        print(request)
        print('hhhhhhhhh')
    
    merge_files.short_description = "Merged Files"


admin.site.register(ReportFiles,ReportFilesAdmin)

