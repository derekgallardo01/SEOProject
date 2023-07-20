from django.shortcuts import render
#from .models import Categories

from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import json
from django.conf import settings
import pytrends
from pytrends.request import TrendReq
from googleads import adwords
from googleads import errors

from google.ads.google_ads.client import GoogleAdsClient

from datetime import datetime, date, time
import datetime
import time
import pandas as pd
import numpy as np
import os
import csv
from django.conf import settings
import matplotlib.pyplot as plt
import seaborn as sns
from django.utils import timezone
from googleTrend.models import googleTrend


def trends(request):
    cat = request.GET.get('cat', '')
    recid = request.GET.get('recid', '')
    datalist = request.GET.get('datalist', '')

    csvdata = googleTrend.objects.filter(pk=recid)
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    #print(timenow)

    filename = csvdata[0].filename
    #return HttpResponse('dddd')

    data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
    searches = [x for x in data["Keywords"]]
    pytrend = TrendReq()
    groupkeywords = list(zip(*[iter(searches)]*1))
    groupkeywords = [list(x) for x in groupkeywords]
    
    dicti = {}
    i = 1
    for trending in groupkeywords:
        pytrend.build_payload(trending, timeframe = 'today 3-m', geo = 'GB')
        dicti[i] = pytrend.interest_over_time()
        i+=1

    result = pd.concat(dicti, axis=1)
    result.columns = result.columns.droplevel(0)
    trenddata = result.drop('isPartial', axis = 1)
    if(type=='full_data'):
        return HttpResponse(trenddata.to_html())

    trenddata.reset_index(level=0, inplace=True)
    result = pd.melt(trenddata, id_vars='date', value_vars=searches)

    try:
        os.unlink(settings.FILES_ROOT +'trends.csv')
    except:
        pass
    
    #dwonload file for google trend
    filename = settings.FILES_ROOT +'google-trend-data'+ str(timenow)+'.csv'
    
    #wks = connect_google_sheet()
    #pandas_to_sheets(trenddata, wks)
    
    result.to_csv(filename)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response
        
    return HttpResponse(result.to_html())

# write sheet with top keywords or sheet second
def relatedquery(request):
    pytrend = TrendReq()
    #, cat = 44

    #searches = ['detox', 'water fasting', 'benefits of fasting', 'fasting benefits', 'acidic', 'water diet']
    keylist = ['foundation', 'eyeliner', 'concealer', 'lipstick']
    
    dg = []
    i = 0
    for keyw in keylist:
        pytrend.build_payload(kw_list = [keyw], geo = 'US', timeframe = 'today 3-m')
        related_queries = pytrend.related_queries()
        related_queries = related_queries[keyw]["top"]
        dg.append(related_queries)
        #dg.append(pd.DataFrame.from_dict(listdata))
        i+=1

    result = pd.concat(dg)
    #wks = openmysheet('Sheet2')
    #pandas_to_sheets(result, wks)
    
    #dwonload file for google trend
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = settings.FILES_ROOT +'keyword-top-related-data'+ str(timenow)+'.csv'
    
    #wks = connect_google_sheet()
    #pandas_to_sheets(trenddata, wks)
    
    result.to_csv(filename)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response

    '''pytrend.build_payload(kw_list=['foundation'], geo = 'US', timeframe = 'today 3-m')
    related_queries= pytrend.related_queries()
    result= pd.DataFrame.from_dict(related_queries)'''

    return HttpResponse(result.to_html())


def risingfromfile(request):
    cat = request.GET.get('cat', '')
    recid = request.GET.get('recid', '')
    datalist = request.GET.get('datalist', '')
    pytrend = TrendReq()
    csvdata = googleTrend.objects.filter(pk=recid)
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    #print(timenow)

    filename = csvdata[0].filename
    #return HttpResponse('dddd')

    data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
    searches = [x for x in data["Keywords"]]
    print(searches)
    i = 0
    dg = {}
    for trending in searches:
        keyw=[trending]
        pytrend.build_payload(kw_list=keyw, timeframe = 'today 3-m', geo = 'GB')
        listdata = pytrend.related_queries()
        print(listdata)
        dg[i] = pd.DataFrame.from_dict(listdata)
        i+=1

    result = pd.concat(dg, axis=1)
    print(result)

    #, cat = 44
    #pytrend.build_payload(kw_list=searches, geo = 'US', timeframe = 'today 3-m')
    #related_queries= pytrend.related_queries()

    #dg= pd.DataFrame.from_dict(related_queries)
    wks = openmysheet('Sheet2')
    pandas_to_sheets(result, wks)
    return HttpResponse('test')

def suggestionskeyword(request):
    pytrend = TrendReq()
    keylist = ['foundation', 'eyeliner', 'concealer', 'lipstick', 'amazon']
    dg = []
    i = 0
    for keyw in keylist:
        suggested = pytrend.suggestions(keyword=keyw)
        print(suggested)
        
        #dg.append(related_queries.get(keyw).get('rising'))
        dg.append(pd.DataFrame.from_dict(suggested))
        i+=1

    
    result = pd.concat(dg)
    #return HttpResponse(result.to_html())
    #wks = openmysheet('Sheet1')
    #pandas_to_sheets(result, wks)
    #dwonload file for google trend
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = settings.FILES_ROOT +'keyword-suggestion-data'+ str(timenow)+'.csv'

    result.to_csv(filename)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response
    return HttpResponse(result.to_html())

    
    setdata= pd.DataFrame.from_dict(suggested)
    return HttpResponse(setdata.to_html())

    print('j')

def trendsStatic(request):
    cat = request.GET.get('cat', '')
    datalist = request.GET.get('datalist', '')
    #return HttpResponse(cat)
    pytrend = TrendReq()
    #trend data of your keywords in that category
    pytrend.build_payload(kw_list=['tea', 'coffee', 'coke', 'milk', 'water'], timeframe='today 12-m', geo = 'GB', cat = int(cat) )
    interest_over_time_df = pytrend.interest_over_time() 
    if(datalist=='trend'):
        return HttpResponse(interest_over_time_df.to_html())
        
    sns.set(color_codes=True)
    dx = interest_over_time_df.plot.line(figsize = (9,6), title = "Interest Over Time")
    dx.set_xlabel('Date')
    dx.set_ylabel('Trends Index')
    dx.tick_params(axis='both', which='major', labelsize=13)
    #return HttpResponse(interest_over_time_df.to_html())

    print(pytrend.suggestions(keyword='search engine land'), '\n')
    print(pytrend.suggestions(keyword='amazon'), '\n')
    print(pytrend.suggestions(keyword='cats'), '\n')
    print(pytrend.suggestions(keyword='macbook pro'), '\n')
    print(pytrend.suggestions(keyword='beer'), '\n')
    print(pytrend.suggestions(keyword='ikea'), '\n')

    setdata = {}
    setdata['index1'] = pytrend.suggestions(keyword='cats')
    setdata['index2'] = pytrend.suggestions(keyword='amazon')

    setdata= pd.DataFrame.from_dict(setdata)
    #return HttpResponse(setdata.to_html())

    pytrend.build_payload(kw_list=['foundation'], geo = 'US', timeframe = 'today 3-m', cat = 44)
    related_queries= pytrend.related_queries()

    related_queries= pd.DataFrame.from_dict(related_queries)
    return HttpResponse(related_queries.to_html())

    print(interest_over_time_df.head())
    return HttpResponse(interest_over_time_df.to_html())





def googleads_report(request):
    ## initialize google adwords client object
    adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT +"googleAds.yaml")
    #return HttpResponse(adwords_client)
    ## set your customer-ID
    adwords_client.SetClientCustomerId('561-563-8203')

    report_downloader = adwords_client.GetReportDownloader(version='v201809')

    ## get CLICK_PERFORMANCE report for yesterday as an example
    report_date = datetime.datetime.now()-datetime.timedelta(days=1)
    report_date_string = report_date.strftime("%Y%m%d")

    ## build the report query
    report_query = (adwords.ReportQueryBuilder()
        .Select('GclId','CampaignName', 'AdGroupName', 'CriteriaParameters')
        .From('CLICK_PERFORMANCE_REPORT')
        .During(start_date=report_date_string,end_date=report_date_string)
        .Build())

    ## download the report as CSV into string
    csv_report = report_downloader.DownloadReportWithAwql(
        report_query, 'CSV', skip_report_header=True,
        skip_column_header=True, skip_report_summary=True,
        include_zero_impressions=False)



def googleads_report2(request):
    #Derek Account detail
    #1//0abcdefghijklABCDEF
    #mine detail
    '''credentials = {
    'developer_token': 'q4QiPbtYwtaV4ZqcLRJ58Q',
    'refresh_token': '1//0abcdefghijklABCDEF',
    'client_id': '266173227311-9nvngetht268a6941jv4i8tvjpl3rds1.apps.googleusercontent.com',
    'client_secret': 'aHJUqc0DqSHpyYm_OqU6U9KO'}'''

    #Derek Account detail
    credentials = {
    'developer_token': 'XZlthKvO76APVnuBzu4vPw',
    'refresh_token': '1//0abcdefghijklABCDEF',
    'client_id': '578771087938-4oba58fd7vdk2u2rl3mpfotj7gol8sp1.apps.googleusercontent.com',
    'client_secret': 'knttL5yFdnJ6SfkCGackdOZO'}


    adwords_client = GoogleAdsClient.load_from_dict(credentials)

    ## initialize google adwords client object
    #adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT +"googleAds.yaml")
    #return HttpResponse(adwords_client)
    ## set your customer-ID
    adwords_client.SetClientCustomerId('168-398-7678')
    #561-563-8203

    report_downloader = adwords_client.GetReportDownloader(version='v201809')

    ## get CLICK_PERFORMANCE report for yesterday as an example
    report_date = datetime.datetime.now()-datetime.timedelta(days=1)
    report_date_string = report_date.strftime("%Y%m%d")

    ## build the report query
    report_query = (adwords.ReportQueryBuilder()
        .Select('GclId','CampaignName', 'AdGroupName', 'CriteriaParameters')
        .From('CLICK_PERFORMANCE_REPORT')
        .During(start_date=report_date_string,end_date=report_date_string)
        .Build())

    ## download the report as CSV into string
    csv_report = report_downloader.DownloadReportWithAwql(
        report_query, 'CSV', skip_report_header=True,
        skip_column_header=True, skip_report_summary=True,
        include_zero_impressions=False)


def trackkeywords(request):
    pytrend = TrendReq()
    type = request.GET.get('type', '')

    searches = ['detox', 'water fasting', 'benefits of fasting', 'fasting benefits', 'acidic', 'water diet']
    
    #searches = ['detox', 'water fasting', 'benefits of fasting', 'fasting benefits', 'acidic', 'water diet', 'ozone therapy', 'colon hydrotherapy', 'water fast', 'reflexology', 'balance', 'deep tissue massage', 'cryo', 'healthy body', 'what is detox','the truth about cancer', 'dieta', 'reverse diabetes', 'how to reverse diabetes', 'water cleanse', 'can you drink water when fasting', 'water fasting benefits', 'glycemic load', 'anti ageing', 'how to water fast', 'ozone treatment', 'healthy mind', 'can you reverse diabetes', 'anti aging', 'health benefits of fasting', 'hydrocolonic', 'shiatsu massage', 'seaweed wrap', 'shiatsu', 'can you get rid of diabetes', 'how to get rid of diabetes', 'healthy body healthy mind', 'colonic hydrotherapy', 'green detox', 'what is water fasting', '21 day water fast', 'benefits of water fasting', 'cellulite', 'ty bollinger', 'detox diet', 'detox program', 'anti aging treatments', 'ketogenic', 'glycemic index', 'water fasting weight loss', 'keto diet plan', 'acidic symptoms', 'alkaline diet', 'water fasting diet', 'laser therapy', 'anti cellulite massage', 'swedish massage', 'benefit of fasting', 'detox your body', 'colon therapy', 'reversing diabetes', 'detoxing', 'truth about cancer', 'how to remove acidity from body', '21 day water fast results', 'colon cleanse', 'fasting health benefits', 'antiaging', 'aromatheraphy massage']

    groupkeywords = list(zip(*[iter(searches)]*1))
    groupkeywords = [list(x) for x in groupkeywords]

    dicti = {}
    i = 1
    for trending in groupkeywords:
        pytrend.build_payload(trending, timeframe = 'today 3-m', geo = 'GB')
        dicti[i] = pytrend.interest_over_time()
        i+=1
    
    result = pd.concat(dicti, axis=1)
    #return HttpResponse(result.to_html())
    result.columns = result.columns.droplevel(0)
    trenddata = result.drop('isPartial', axis = 1)
    if(type=='full_data'):
        return HttpResponse(trenddata.to_html())

    trenddata.reset_index(level=0, inplace=True)
    result = pd.melt(trenddata, id_vars='date', value_vars=searches)
    #return HttpResponse(result.to_html())

    try:
        os.unlink(settings.FILES_ROOT +'trends.csv')
    except:
        pass

    #wks = connect_google_sheet()
    wks = openmysheet('Sheet2')
    pandas_to_sheets(result, wks)
    result.to_csv(settings.FILES_ROOT +'trends.csv')
    return HttpResponse(result.to_html())


def keywordrising(request):
    pytrend = TrendReq()
    keylist = ['foundation', 'eyeliner', 'concealer', 'lipstick']
    '''pytrend.build_payload(kw_list=['foundation', 'eyeliner', 'concealer', 'lipstick'], geo = 'US', timeframe = 'today 3-m')
    related_queries= pytrend.related_queries()
    dg=related_queries.get('lipstick').get('rising')
    print(type(dg))
    return HttpResponse(dg.to_html())'''

    dg = []
    i = 0
    for keyw in keylist:
        pytrend.build_payload(kw_list = [keyw], geo = 'US', timeframe = 'today 3-m')
        related_queries = pytrend.related_queries()
        dg.append(related_queries.get(keyw).get('rising'))
        #dg.append(pd.DataFrame.from_dict(listdata))
        i+=1

    result = pd.concat(dg)
    #wks = openmysheet('Sheet1')
    #pandas_to_sheets(result, wks)
    #dwonload file for google trend
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = settings.FILES_ROOT +'keyword-rising-data'+ str(timenow)+'.csv'
    
    #wks = connect_google_sheet()
    #pandas_to_sheets(trenddata, wks)
    
    result.to_csv(filename)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response
    return HttpResponse(result.to_html())

def connect_google_sheet():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    links = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    credentials =  ServiceAccountCredentials.from_json_keyfile_name(settings.FILES_ROOT +'potent-ripple-277316-336c280867a3.json', links)
    gc = gspread.authorize(credentials)
    sh = gc.create('Mycoolspreadsheet')
    wks = gc.open("Mycoolspreadsheet").sheet1
    return wks

def openmysheet(sheetnum = 'Sheet1'):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    links = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    
    credentials =  ServiceAccountCredentials.from_json_keyfile_name(settings.FILES_ROOT +'realestate-8799e55163f5.json', links)
    credentials =  ServiceAccountCredentials.from_json_keyfile_name(settings.FILES_ROOT +'derek_potent-ripple-277316-83a3eb52f746.json', links)
    gc = gspread.authorize(credentials)
    #wks = gc.open("mustwatch").sheet1
    #wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/12qgcZgfXs8cnhvruGndUpwlx-d5bLSy3k__a0e3xsTU/edit#gid=0").sheet1
    # Govind
    wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/12qgcZgfXs8cnhvruGndUpwlx-d5bLSy3k__a0e3xsTU/edit#gid=1381289192")
    # Derek
    wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1dBfjVnuLJiyKrjbzp4dvpLtchACAN4hCh0Uz6P_gZZo/edit?usp=drivesdk")
    wks = wks.worksheet(sheetnum)
    print(wks)
    return wks

def write_data_in_googlesheet(request):
    wks = openmysheet()
    return HttpResponse(wks)
    return wks
    


def authenticate_google_docs():
    f = file(os.path.join('your-key-file.p12'), 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    credentials = SignedJwtAssertionCredentials('username@gmail.com', SIGNED_KEY, scope)

    data = {
        'refresh_token' : '<refresh-token-copied>',
        'client_id' : '<client-id-copied>',
        'client_secret' : '<client-secret-copied>',
        'grant_type' : 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc




def gspreadsheet(request):
    wks = connect_google_sheet()
    #df = pd.read_csv(settings.FILES_ROOT +"train.csv")
    #pandas_to_sheets(df, wks)
    wks.to_csv(settings.FILES_ROOT +'gspreadsheet.csv', index = False)
    return HttpResponse(wks.to_html())

def iter_pd(df):
    for val in list(df.columns):
        yield val
    for row in df.values:
        for val in list(row):
            if pd.isna(val):
                yield ""
            else:
                yield val


def pandas_to_sheets(pandas_df, sheet, clear = True):
    import gspread
    print(sheet)
    # Updates all values in a workbook to match a pandas dataframe 
    if clear:
        sheet.clear()
    (row, col) = pandas_df.shape
    cells = sheet.range("A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col)))
    f = 1
    for cell, val in zip(cells, iter_pd(pandas_df)):
        #print(str(val).find('00:'))
        if(str(val).find('00:') >=0 ):
            dtstr = str(val).split(' ')
            cell.value = dtstr[0]
            #cell.value = val.strftime('%Y-%m-%d')
        else:
            cell.value = val
        
        
        print(val)
        f += 1
        sheet.update_cells(cells)
        #
    

def getcsv():
    df = pd.read_csv("train.csv")
    pandas_to_sheets(df, wks)