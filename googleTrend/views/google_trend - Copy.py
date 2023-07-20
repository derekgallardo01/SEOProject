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

#http://74.208.120.160:8080/google/trends?recid=1
def trends(request):
    cat = request.GET.get('cat', '')
    recid = request.GET.get('recid', '')
    datalist = request.GET.get('datalist', '')

    csvdata = googleTrend.objects.filter(pk=recid)
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    #print(timenow)

    filename = csvdata[0].filename
    #return HttpResponse('dddd')

    querycontent = csvdata[0].query_content
    keylist = []
    keylist_text = []

    if(querycontent and querycontent!=''):
        keylist_text = querycontent.split("\n")

    if(filename and filename!=''):
        data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
        keylist = [x for x in data["Keywords"]]
    
    searches = keylist_text+keylist
    searches = [i.strip() for i in searches]
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
    
    result.to_csv(filename, index = False)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response
        
    return HttpResponse(result.to_html())

# write sheet with top keywords or sheet second
#http://74.208.120.160:8080/google/related-query/
def relatedquery(request):
    pytrend = TrendReq()
    #, cat = 44

    #searches = ['detox', 'water fasting', 'benefits of fasting', 'fasting benefits', 'acidic', 'water diet']
    #keylist = ['foundation', 'eyeliner', 'concealer', 'lipstick']
    cat = request.GET.get('cat', '')
    recid = request.GET.get('recid', '')
    datalist = request.GET.get('datalist', '')

    csvdata = googleTrend.objects.filter(pk=recid)
    filename = csvdata[0].filename

    querycontent = csvdata[0].query_content
    keylist = []
    keylist_text = []

    if(querycontent and querycontent!=''):
        keylist_text = querycontent.split("\n")

    if(filename and filename!=''):
        data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
        keylist = [x for x in data["Keywords"]]
    
    searches = keylist_text+keylist
    searches = [i.strip() for i in searches]
    dg = []
    i = 0
    for keyw in searches:
        pytrend.build_payload(kw_list = [keyw], geo = 'US', timeframe = 'today 3-m')
        related_queries = pytrend.related_queries()
        related_queries = related_queries[keyw]["top"]
        print(type(related_queries))
        print(related_queries)
        if(type(related_queries)=='pandas.core.frame.DataFrame' and len(related_queries)>0):
            dg.append(related_queries)
        #dg.append(pd.DataFrame.from_dict(listdata))
        i+=1

    #result = pd.concat(dg)
    #wks = openmysheet('Sheet2')
    #pandas_to_sheets(result, wks)
    
    
    #dwonload file for google trend
    filename = settings.FILES_ROOT +'keyword-top-related-data'+ str(recid)+'.csv'
    try:
        os.unlink(filename)
    except:
        pass
    
    print(len(dg))
    if(len(dg)>0):
        result = pd.concat(dg)
        result.to_csv(filename, index = False)
    else:
        dg = []
        result = pd.DataFrame(dg)
        result.to_csv(filename, index = False)
    #wks = connect_google_sheet()
    #pandas_to_sheets(trenddata, wks)
    
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response

    '''pytrend.build_payload(kw_list=['foundation'], geo = 'US', timeframe = 'today 3-m')
    related_queries= pytrend.related_queries()
    result= pd.DataFrame.from_dict(related_queries)'''

    return HttpResponse(result.to_html())

#google/rising-from-file
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

    querycontent = csvdata[0].query_content
    keylist = []
    keylist_text = []

    if(querycontent and querycontent!=''):
        keylist_text = querycontent.split("\n")

    if(filename and filename!=''):
        data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
        keylist = [x for x in data["Keywords"]]
    
    searches = keylist_text+keylist
    searches = [i.strip() for i in searches]
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

#google/suggestions-keyword
def suggestionskeyword(request):
    pytrend = TrendReq()
    #keylist = ['foundation', 'eyeliner', 'concealer', 'lipstick', 'amazon']
    cat = request.GET.get('cat', '')
    recid = request.GET.get('recid', '')
    datalist = request.GET.get('datalist', '')
    
    csvdata = googleTrend.objects.filter(pk=recid)
    filename = csvdata[0].filename
    querycontent = csvdata[0].query_content
    keylist = []
    keylist_text = []

    if(querycontent and querycontent!=''):
        keylist_text = querycontent.split("\n")

    if(filename and filename!=''):
        data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
        keylist = [x for x in data["Keywords"]]
    
    final_list = keylist_text+keylist
    final_list = [i.strip() for i in final_list]
    dg = []
    i = 0
    for keyw in final_list:
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

    result.to_csv(filename, index = False)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
        return response
    return HttpResponse(result.to_html())

    
    setdata= pd.DataFrame.from_dict(suggested)
    return HttpResponse(setdata.to_html())

    print('j')




#http://74.208.120.160:8080/google/keyword-rising
def keywordrising(request):
    pytrend = TrendReq()
    cat = request.GET.get('cat', '')
    recid = request.GET.get('recid', '')
    datalist = request.GET.get('datalist', '')

    csvdata = googleTrend.objects.filter(pk=recid)
    filename = csvdata[0].filename
    
    querycontent = csvdata[0].query_content
    keylist = []
    keylist_text = []

    if(querycontent and querycontent!=''):
        keylist_text = querycontent.split("\n")

    if(filename and filename!=''):
        data = pd.read_csv(settings.MEDIA_ROOT + str(filename),  usecols=['Keywords'] )
        keylist = [x for x in data["Keywords"]]
    
    final_list = keylist_text+keylist
    final_list = [i.strip() for i in final_list]

    dg = []
    i = 0
    for keyw in final_list:
        pytrend.build_payload(kw_list = [keyw], geo = 'US', timeframe = 'today 3-m')
        related_queries = pytrend.related_queries()
        risingkeyw = related_queries.get(keyw).get('rising')
        if(risingkeyw and len(risingkeyw)>0):
            dg.append(risingkeyw)
        #dg.append(pd.DataFrame.from_dict(listdata))
        i+=1

    print(dg)
    #wks = openmysheet('Sheet1')
    #pandas_to_sheets(result, wks)
    #dwonload file for google trend
    timenow = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = settings.FILES_ROOT +'keyword-rising-data'+ str(timenow)+'.csv'
    
    #wks = connect_google_sheet()
    #pandas_to_sheets(trenddata, wks)
    if(len(dg)>0):
        result = pd.concat(dg)
        result.to_csv(filename, index = False)
    else:
        dg = []
        result = pd.DataFrame(dg)
        result.to_csv(filename, index = False)

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