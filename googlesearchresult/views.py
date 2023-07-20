from django.shortcuts import render
from googlesearchresult.models import googlesearchresult, googlesearchresultData
# Create your views here.
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import os
import csv

def download_report_file(request):
    recid = request.GET.get('recid', '')
    
    csvdata = googlesearchresult.objects.filter(pk=recid)
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    #print(timenow)

    filename = csvdata[0].file_path
    
    #dwonload file for google trend
    #filename = settings.FILES_GOOGLE_RESULT + str(filename)
    try:
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
            return response
    except Exception:
        pass


def download_keyword_file(request):
    recid = request.GET.get('recid', '')
    
    csvdata = googlesearchresultData.objects.filter(pk=recid)
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    #print(timenow)

    filename = csvdata[0].file_path
    
    #dwonload file for google trend
    #filename = settings.FILES_GOOGLE_RESULT + str(filename)
    try:
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
            return response
    except Exception:
        pass  
    

def adwords_report(request):
    from googleads import adwords
    from googleads import errors
    import time
    import datetime
    import os
    import sys
    
        
    ## initialize google adwords client object
    adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT+"credentials/google-ads.yaml")

    ## set your customer-ID
    adwords_client.SetClientCustomerId('7144855468')

    report_downloader = adwords_client.GetReportDownloader(version='v201809')

    ## get CLICK_PERFORMANCE report for yesterday as an example
    report_date = datetime.datetime.now()-datetime.timedelta(days=1)
    report_date_string = report_date.strftime("%Y%m%d")

    ## build the report query
    '''report_query = (adwords.ReportQueryBuilder()
        .Select('GclId','CampaignName', 'AdGroupName', 'CriteriaParameters')
        .From('CLICK_PERFORMANCE_REPORT')
        .During(start_date=report_date_string,end_date=report_date_string)
        .Build())'''
    report_query = (adwords.ReportQueryBuilder().Select('GclId','CampaignName', 'AdGroupName', 'CriteriaParameters').From('CLICK_PERFORMANCE_REPORT').During(start_date=report_date_string,end_date=report_date_string).Build())

    ## download the report as CSV into string
    csv_report = report_downloader.DownloadReportWithAwql( report_query,'CSV', skip_report_header=True, skip_column_header=True, skip_report_summary=True,include_zero_impressions=False)
    
    return HttpResponse('g')

        
