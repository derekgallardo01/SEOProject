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



#No using below fie
#No Using that files #############################################################################################


#No URL
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


def get_suggestions(keyword):
    adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT +"credentials/googleads_derek.yaml")
    adwords_client.SetClientCustomerId('124-513-9115')
    report_downloader = adwords_client.GetReportDownloader(version='v201809')
    targeting_idea_service = adwords_client.GetService('TargetingIdeaService', version='v201809')

    ## get CLICK_PERFORMANCE report for yesterday as an example
    report_date = datetime.datetime.now()-datetime.timedelta(days=1)
    report_date_string = report_date.strftime("%Y%m%d")

    selector = {
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS'
    }

    selector['requestedAttributeTypes'] = [
    'KEYWORD_TEXT', 'SEARCH_VOLUME', 'CATEGORY_PRODUCTS_AND_SERVICES']
    offset = 0
    selector['paging'] = {
        'startIndex': str(offset),
        'numberResults': str(5)
    }
    selector['searchParameters'] = [{
        'xsi_type': 'RelatedToQuerySearchParameter',
        'queries': [keyword]
    }]

    keyw = ''
    page = targeting_idea_service.get(selector)
    for result in page['entries']:
        attributes = {}
        sep = ''
        for attribute in result['data']:
            attributes[attribute['key']] = getattr(
                attribute['value'], 'value', '0')
        keyw += sep+' '+attributes['KEYWORD_TEXT']
        sep = ','
    
    return keyw


def googleads_report(request):
    ## initialize google adwords client object
    #adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT +"credentials/googleAds3_testing.yaml")
    adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT +"credentials/googleads_derek.yaml")
    #return HttpResponse(adwords_client)
    ## set your customer-ID    181-573-1297
    adwords_client.SetClientCustomerId('124-513-9115')

    report_downloader = adwords_client.GetReportDownloader(version='v201809')
    targeting_idea_service = adwords_client.GetService('TargetingIdeaService', version='v201809')

    ## get CLICK_PERFORMANCE report for yesterday as an example
    report_date = datetime.datetime.now()-datetime.timedelta(days=1)
    report_date_string = report_date.strftime("%Y%m%d")

    selector = {
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS'
    }

    selector['requestedAttributeTypes'] = [
    'KEYWORD_TEXT', 'SEARCH_VOLUME', 'CATEGORY_PRODUCTS_AND_SERVICES']
    offset = 0
    selector['paging'] = {
        'startIndex': str(offset),
        'numberResults': str(5)
    }
    selector['searchParameters'] = [{
        'xsi_type': 'RelatedToQuerySearchParameter',
        'queries': ['boulder seo']
    }]
    
    page = targeting_idea_service.get(selector)
    for result in page['entries']:
        attributes = {}
        for attribute in result['data']:
            attributes[attribute['key']] = getattr(
                attribute['value'], 'value', '0')

        print('Keyword with "%s" text and average monthly search volume '
                '"%s" was found with Products and Services categories: %s.'
                % (attributes['KEYWORD_TEXT'],
                    attributes['SEARCH_VOLUME'],
                    attributes['CATEGORY_PRODUCTS_AND_SERVICES']))

    #print(page)
    return HttpResponse(page)

    ## build the report query
    '''report_query = (adwords.ReportQueryBuilder()
        .Select('GclId','CampaignName', 'AdGroupName', 'CriteriaParameters')
        .From('CLICK_PERFORMANCE_REPORT')
        .During(start_date=report_date_string,end_date=report_date_string)
        .Build())

    ## download the report as CSV into string
    csv_report = report_downloader.DownloadReportWithAwql(
        report_query, 'CSV', skip_report_header=True,
        skip_column_header=True, skip_report_summary=True,
        include_zero_impressions=False)'''

def adwords_plan(request):
    selector = {
        'searchParameters': [
            {
                'xsi_type': 'RelatedToQuerySearchParameter',
                'queries': ['seo', 'adwords', 'adwords seo']
            },
            {
                'xsi_type': 'LanguageSearchParameter',
                'languages': [{'id': '1000'}]
            },
            {
                'xsi_type': 'LocationSearchParameter',
                'locations': [{'id': '2036'}]
            },
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'requestedAttributeTypes': ['KEYWORD_TEXT', 'SEARCH_VOLUME'],
    }

    for (data, selector) in paged_request('TargetingIdeaService', selector):
        print(data)

def googleads_tiwari(request):
    credentials = {
    'developer_token': '1oeKw7itSgvbhsQN4-Sc_g',
    'refresh_token': '4/2QEjEYqFnqX0X1gvUR7RaCqHZTcU50fnBwPf5xQg_t7ZyIqf0McmO8qVvr7GdSHfKHXjIFiT2QU-fzJ34eK3YEg',
    'client_id': '21546823261-p3685qpic8g4ae2tkm5c0t7f3lclipa8.apps.googleusercontent.com',
    'client_secret': 'YggkSH3mMs2opfRriRulXDoo'}


    adwords_client = GoogleAdsClient.load_from_dict(credentials)
    #adwords_client.SetClientCustomerId('104-985-4794')

    #biglearn
    adwords_client.SetClientCustomerId('797-947-2400')
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
    '''credentials = {
    'developer_token': 'XZlthKvO76APVnuBzu4vPw',
    'refresh_token': '1//0abcdefghijklABCDEF',
    'client_id': '578771087938-4oba58fd7vdk2u2rl3mpfotj7gol8sp1.apps.googleusercontent.com',
    'client_secret': 'knttL5yFdnJ6SfkCGackdOZO'}'''
    
    #this detail working fine
    #1//06cA9XJJc0KXMCgYIARAAGAYSNgF-L9IrN-KzYoMHU8mW0_k-Rew46xP-07uZAwROI0gli4TdYQtWKJQ3Fw2PXlVu1eYNN0eROA
    #h9GcGIojm1vmeMuBH_bLvg
    #qEHcXK3CM09B-VG6oXGmaw
    credentials = {
    'developer_token': 'qEHcXK3CM09B-VG6oXGmaw',
    'refresh_token': '4/2QFAANrRKfYqDMriYgGmREBAEXVh6x3NGumMCaoBHo4pf9Z0MttmLqrKHQMBNcj-8yCnhamhkfssNQtHp-ZmUQE',
    'client_id': '243161005391-0dvhtfoeq26nlcfc9fclpi2pcj25a5a0.apps.googleusercontent.com',
    'client_secret': 'ahlVIS7TdMaXIZelL-IZnyQB1'}

    adwords_client = GoogleAdsClient.load_from_dict(credentials)
    adwords_client.SetClientCustomerId('124-513-9115')

    '''report_downloader = adwords_client.GetReportDownloader(version='v201809')

    ## get CLICK_PERFORMANCE report for yesterday as an example
    report_date = datetime.datetime.now()-datetime.timedelta(days=1)
    report_date_string = report_date.strftime("%Y%m%d")'''

    ## build the report query
    '''report_query = (adwords.ReportQueryBuilder()
        .Select('GclId','CampaignName', 'AdGroupName', 'CriteriaParameters')
        .From('CLICK_PERFORMANCE_REPORT')
        .During(start_date=report_date_string,end_date=report_date_string)
        .Build())

    ## download the report as CSV into string
    csv_report = report_downloader.DownloadReportWithAwql(
        report_query, 'CSV', skip_report_header=True,
        skip_column_header=True, skip_report_summary=True,
        include_zero_impressions=False)'''
