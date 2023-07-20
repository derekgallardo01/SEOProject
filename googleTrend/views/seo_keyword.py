from django.shortcuts import render
#from .models import Categories
from django.apps import apps
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import http.client, urllib.request, urllib.parse, urllib.error, base64
from django.db.models import CharField, Value as V
from django.db.models import OuterRef, Subquery, Prefetch
from django.db import connection
from functools import reduce
import operator
from django.core import serializers 
from django.db.models import Q
import json
from django.conf import settings
import pandas as pd
import numpy as np
import os
import csv


def lookup_words_no_convsfn():
    with open(settings.FILES_ROOT +'lookup_words_no_convs.csv', 'r') as file:
        reader = csv.reader(file)
        lookup_words_no_convs = list(reader)
        lookup_words_no_convs_words = [item[0] for item in lookup_words_no_convs]
    
    '''data = pd.read_csv("static/input_data.csv", skiprows=[i for i in range(0,6)])
    data = data.loc[0:25]
    numrec = data["Form Completion (Goal 2 Completions)"] == 0
    data = data[numrec]'''
    return lookup_words_no_convs_words

def noconv(request):
    #os.chdir('files')
    #filepath = os.path.join()
    data = pd.read_csv(settings.FILES_ROOT + 'input_data.csv', skiprows=[i for i in range(0,6)])
    data = data.loc[0:25]
    numrec = data["Form Completion (Goal 2 Completions)"] == 0
    data = data[numrec]
    os.unlink(settings.FILES_ROOT +'lookup_words_no_convs.csv')
    data.to_csv(settings.FILES_ROOT +'lookup_words_no_convs.csv', index = False)

    return HttpResponse(data.to_html())

    print(data.head(3))
    
    #numrec = data["treter"] >0
    #data = data[numrec]

def getKeywordsFrom(keywords):
    result = ""
    lookup_words_no_convs_words = lookup_words_no_convsfn()
    
    #return HttpResponse(data.to_html())
    #print(lookup_words_no_convs_words)

    for keyword in keywords.split():
        for lookup_keyword in lookup_words_no_convs_words:
            #result = keyword + "--" + lookup_keyword+ "+++++"
            if keyword == lookup_keyword:
                result = result + " " + keyword
    return result
#print(getKeywordsFrom('insurance for computer programmer'))


def badtook(request):
    
    header_list = ["keyword_phrases", "clicks", "cost", "cpc", "users", "sessions", "bounce_rate", "pages", "form_completon_rate", "form_completon", "form_completon_val" ]
    data = pd.read_csv(settings.FILES_ROOT +"input_data.csv", skiprows=[i for i in range(0,6)], names = header_list )
    
    data = data.loc[0:25]
    #return HttpResponse(data.to_html())
    #numrec = data["Form Completion (Goal 2 Completions)"] == 0
    my_ads_pool = data
    #data.to_csv('static/lookup_words_no_convs.csv', index = False)
    #return HttpResponse(my_ads_pool.to_html())
    my_ads_pool['bounce_rate'] = pd.to_numeric(my_ads_pool['bounce_rate'].astype(str).str.strip('%'), errors='coerce')

    my_ads_pool['bad_to_ok_keywords'] = my_ads_pool['keyword_phrases'].apply(
    lambda keywords: getKeywordsFrom(keywords)
    )
    fitered_df = my_ads_pool.sort_values(by='bad_to_ok_keywords')
    #return HttpResponse(fitered_df.to_html())
    final_no_convs = fitered_df[fitered_df.bad_to_ok_keywords.str.contains(' ')]
    #final_no_convs = fitered_df
    #return HttpResponse(final_no_convs.to_html())
    #################################################################
    #, 'transactions'
    final_df_avg = final_no_convs.groupby(["bad_to_ok_keywords"]).mean()
    
    #.drop(['clicks', 'cost'], axis=1)
    final_df_avg.reset_index(inplace=True)
    final_df_avg_sorted = final_df_avg.sort_values(by='bad_to_ok_keywords', ascending=True)

    #return HttpResponse(final_df_avg_sorted.to_html())
    ###############################################################

    final_df_sum = final_no_convs.groupby(["bad_to_ok_keywords"]).sum()
    final_df_sum.reset_index(inplace=True)
    #return HttpResponse(final_df_sum.to_html())
    final_df_sum_sorted = final_df_sum.sort_values(by='bad_to_ok_keywords', ascending=True)
    #return HttpResponse(final_df_sum_sorted.to_html())
    final_sums_and_avgs = pd.merge(final_df_sum_sorted, final_df_avg_sorted, on='bad_to_ok_keywords')
    #return HttpResponse(final_sums_and_avgs.to_html())
    #final_sums_and_avgs.columns = ['bad_to_ok_keywords', 'clicks_sum',  'cost_sum', 'transactions_sum', 'bounce_rate_avg']
    final_sums_and_avgs.columns = ['bad_to_ok_keywords', 'bounce_rate', 'bounce_rate_avg']


    #return HttpResponse(final_sums_and_avgs.to_html())

    final_sums_and_avgs['category'] = np.where(final_sums_and_avgs['bounce_rate_avg']<100, 'ok', 'bad')
    #return HttpResponse(final_sums_and_avgs.to_html())

    final_sums_and_avgs['bounce_rate_avg'] = pd.to_numeric(final_sums_and_avgs['bounce_rate_avg'].astype(int))
    
    #return HttpResponse(final_sums_and_avgs.to_html())
    final_no_convs_pool = final_no_convs.reset_index(drop=True)

    #return HttpResponse(final_no_convs_pool.to_html())

    final_result = pd.merge(final_no_convs_pool, final_sums_and_avgs, on='bad_to_ok_keywords')
    final_result_drop_columns = final_result
    #.drop(['transactions_sum','bounce_rate'], axis=1)
    try:
        os.unlink(settings.FILES_ROOT +'2-ppc_bad_to_ok.csv')
    except:
        pass
    
    final_result_drop_columns.to_csv(settings.FILES_ROOT +'2-ppc_bad_to_ok.csv', index = False)

    #return HttpResponse(fitered_df.to_html())
    return HttpResponse(final_result_drop_columns.to_html())
    #numrec = data["treter"] >0
    #data = data[numrec]

def convdata():
    header_list = ["keyword_phrases", "clicks", "cost", "cpc", "users", "sessions", "bounce_rate", "pages", "form_completon_rate", "transactions", "form_completon_val" ]
    data = pd.read_csv(settings.FILES_ROOT +"input_data.csv", skiprows=[i for i in range(0,7)], names = header_list )
    
    data = data.loc[0:24]
    numrec = data["transactions"] > 0
    data = data[numrec]
    return data

def convertedfound(request):
    inputData_with_convs = convdata()
    inputData_with_convs = inputData_with_convs.drop(['cpc', 'users','sessions','pages','form_completon_rate','form_completon_val'], axis=1)
    #return HttpResponse(inputData_with_convs.to_html())
    #["keyword_phrases", "clicks", "cost", "transactions", "bounce_rate"]
    inputData_with_convs = inputData_with_convs.reindex(columns=["keyword_phrases", "clicks", "cost", "transactions", "bounce_rate"])
    searchConsole = pd.read_csv(settings.FILES_ROOT +'search_console_data.csv',names = ["keyword_phrases", "clicks", "impressions", "ctr", "position"])
    vlookup = pd.merge(inputData_with_convs, searchConsole, on='keyword_phrases')
    vlookup_new = vlookup.drop(['clicks_y','impressions','ctr','position'], axis=1)
    vlookup_new.columns = ['keyword_phrases','clicks', 'cost','transactions','bounce_rate']
    #return HttpResponse(vlookup_new.to_html())
    try:
        os.unlink(settings.FILES_ROOT +'3-converted_found_in_search_console.csv')
    except:
        pass
    
    
    vlookup_new.to_csv(settings.FILES_ROOT +'3-converted_found_in_search_console.csv', index = False)
    joined_frames = vlookup_new.append(inputData_with_convs).sort_values(by='keyword_phrases', ascending=False)
    # HttpResponse(joined_frames.to_html())
    not_found_in_search_console_but_converted = joined_frames.drop_duplicates(keep=False)
    
    try:
        os.unlink(settings.FILES_ROOT +'4-converted_not_found_in_search_console.csv')
    except:
        pass
    not_found_in_search_console_but_converted.to_csv(settings.FILES_ROOT +'4-converted_not_found_in_search_console.csv', index = False)
    return HttpResponse(not_found_in_search_console_but_converted.to_html())