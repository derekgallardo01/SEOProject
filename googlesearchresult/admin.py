from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import googlesearchresult, googlesearchresultData, keywordDensity
from django.utils.html import format_html
# Register your models here.

from googleads import adwords
from datetime import datetime, date, time
import datetime

import pandas as pd
from googlesearch import search 
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import ssl
import urllib
import json
import requests
import os
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
import xlsxwriter
import pdfkit as pdf

from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Sum


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')




class GoogleSearchResultAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ( 'created_at','search_query', 'custom_url', 'search_result', 'show_report')
    search_fields = ('search_query', )
    #list_display_links = ('all_actions',)
    
    fieldsets = (
        (None, {
            'fields': ('search_query', 'custom_url', ),
            'description': "<h3>Enter a single search query OR multiple search queries separated by a new line. <br> Note: A Search Query Report takes a few minutes to create. <br>Multiple Search Queries take longer than a single Search Query KD report for example. <br /> Note: Sometimes the API will return a 30 second Rate limit if a query is submitted quickly after a recent lookup. </h3>."
        }),
    )


    
        
    #def show_report(self, obj):
    #    return format_html("<a target='_blank' href='{url}'>Download Trending Report</a>", url='/google/trends?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Rising Report</a>", url='/google/keyword-rising?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Top Related Report</a>", url='/google/related-query/?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Suggestions Report</a>", url='/google/suggestions-keyword?recid='+str(obj.id))
    
    '''def my_view(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           key=value,
        )
        return TemplateResponse(request, "sometemplate.html", context)'''

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def getbodycontent(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def auth_suggest(self):
        adwords_client = adwords.AdWordsClient.LoadFromStorage(settings.FILES_ROOT +"credentials/googleads_derek.yaml")
        adwords_client.SetClientCustomerId('714-485-5468')
        report_downloader = adwords_client.GetReportDownloader(version='v201809')
        targeting_idea_service = adwords_client.GetService('TargetingIdeaService', version='v201809')

        ## get CLICK_PERFORMANCE report for yesterday as an example
        report_date = datetime.datetime.now()-datetime.timedelta(days=1)
        report_date_string = report_date.strftime("%Y%m%d")
        return targeting_idea_service

    def get_suggestions(self, keyword, targeting_idea_service):
        
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
        sep = ''
        page = targeting_idea_service.get(selector)
        for result in page['entries']:
            attributes = {}
            
            for attribute in result['data']:
                attributes[attribute['key']] = getattr(
                    attribute['value'], 'value', '0')
            keyw += sep+' '+attributes['KEYWORD_TEXT']
            sep = ','
        
        return keyw

    def save_model(self, request, obj, form, change):
        #print(request.POST['search_query'])
        query_post = request.POST['search_query']
        custom_url = request.POST['custom_url']
        timenow = timezone.now().strftime('%Y%m%d%H%M%S')
        #files = request.FILES.getlist('file_field')

        targeting_idea_service = self.auth_suggest()
    
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,} 
        request_data = urllib.request.Request(custom_url,None,headers) #The assembled request
        html = urllib.request.urlopen(request_data).read()

        #html = urllib.request.urlopen(custom_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        custom_url_text = u" ".join(t.strip() for t in visible_texts)

        title_meta = soup.find("title")
        custom_url_title = title_meta.text

        custom_url_mata = ''
        for tag in soup.find_all(["meta"]):
            if tag.get("name", None) == "description":
                custom_url_mata = tag.get("content", None)
        

        
        querylist = query_post.split("\n")
        print(querylist)
        #return
        for query_item in querylist:
            query = query_item.strip()
            if(query and query!=''):
                my_results_list = []
                title_h1 = []
                title_h2 = []
                title_h3 = []
                title_h4 = []
                title_h5 = []
                title_h6 = []
                text_content = []
                keyword_density = []
                custom_url_density = []
                all_keyword_density = []
                Nkr = []
                Tkn = []
                Difference = []
                total_density = 0
                url_title_list = []
                url_meta_list = []
                search_position = []
                full_content_arr = []
                body_content_arr = []

                title_density_arr = []
                total_title_density_arr = []
                bodytext_density_arr = []
                tagstatus_dict = []
                wikipedia_ar = []
                ii = 0

                custom_textarray = len(re.findall(query.lower(), custom_url_text.lower() ))
                #len(custom_url_text.split(query))
                custom_textarray_tkn = len(custom_url_text.split())
                custom_density_flt = 0
                if(custom_textarray_tkn>2):
                    custom_density_flt = round(custom_textarray*100/custom_textarray_tkn, 2)

                newdoc = googlesearchresult.objects.create(search_query = query, custom_url = custom_url)
                #newdoc = googlesearchresult(search_query = query)
                newdoc.save()
                #print(newdoc.pk)

                # Get keyword separate
                sentences = nltk.sent_tokenize(query) #tokenize sentences
                nouns = [] #empty to array to hold all nouns

                for sentence in sentences:
                    for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
                        if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'VBG'):
                            nouns.append(word)

                #GET result for single query

                for i in search(query,        # The query you want to run
                                tld = 'com',  # The top level domain
                                lang = 'en',  # The language
                                num = 10,     # Number of results per page
                                start = 0,    # First result to retrieve
                                stop = None,  # Last result to retrieve
                                pause = 0,  # Lapse between HTTP requests
                            ):
                    my_results_list.append(i)
                    
                    if 'wikipedia' in i:
                        wikipedia_ar.append(ii)

                    ii+=1
                    #print(newdoc.pk)
                    texts = ''
                    #print(i)
                    tagstatus = 1

                    try:
                        reqs = requests.get(i,stream=True, timeout=10, headers=headers)
                        reqs.raise_for_status()
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        #print("List of all the h1, h2, h3 :")
                        texts = soup.findAll(text=True)

                        titles = soup.find_all(['h1', 'h2','h3','h4','h5','h6'])
                        finalnumber = 0
                        
                        #print(titles)
                        for d in titles:
                            ser = int(d.name.replace('h',''))
                            if(ser >= finalnumber):
                                finalnumber =  ser
                            else:
                                tagstatus = 0

                    except:
                        pass
                    
                    
                    visible_texts = filter(self.tag_visible, texts) 
                    finaltext = u" ".join(t.strip() for t in visible_texts)
                    finaltext = finaltext.lstrip().rstrip()

                    visible_body_texts = filter(self.getbodycontent, texts) 
                    bodytext = u" ".join(t.strip() for t in visible_body_texts)
                    bodytext = bodytext.lstrip().rstrip()
                    
                    textarray = len(re.findall(query.lower(), finaltext.lower() )) 
                    #len(finaltext.split(query))
                    
                    textarray_tkn = len(finaltext.split())

                    newurl = googlesearchresultData.objects.create(result_id = newdoc.pk)
                    newurl.save()

                    #density for each keywords
                    totalwordcount = 0
                    keycounts = []
                    keydensity = []
                    # getting each word data
                    for eachword in nouns:
                        wordcount = len(re.findall(eachword.lower(), finaltext.lower() ))
                        totalwordcount += wordcount
                        keycounts.append(wordcount)
                        if(textarray_tkn>2):
                            keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'
                            keydensity.append(keydenc)
                        else:
                            keydensity.append('0%')

                        newresult = keywordDensity(rec_id = newurl.pk, keyword = eachword, count = wordcount, keyword_density = keydenc )
                        newresult.save()


                    url_data = {'Keywords': nouns, 'Count': keycounts, 'Keyword Density':keydensity }  
                    urlfilename = settings.FILES_GOOGLE_RESULT+'keyword_density'+ str(newurl.pk)+'.xlsx'
                    try:
                        os.unlink(urlfilename)
                    except:
                        pass

                    df = pd.DataFrame(url_data) 
                    #return HttpResponse(df.to_html())
                    #with ExcelWriter(urlfilename) as writer:
                    #    df.to_excel(writer)
                    
                    writer = pd.ExcelWriter(urlfilename, engine='xlsxwriter')
                    # Convert the dataframe to an XlsxWriter Excel object.
                    df.to_excel(writer, sheet_name='Sheet1')
                    
                    




                    # Close the pd Excel writer and output the Excel file.
                    writer.save()

                    #df.to_csv(urlfilename)

                    Nkr.append(textarray)
                    Tkn.append(textarray_tkn)
                    if(textarray_tkn>10):
                        realdensity = round(textarray*100/textarray_tkn, 2)
                        keyword_density.append(realdensity)
                        individual_key_density = str(round(totalwordcount*100/textarray_tkn, 2))+'%'
                        all_keyword_density.append(individual_key_density)
                    else:
                        realdensity = 0
                        individual_key_density = 0
                        keyword_density.append(0.0)
                        all_keyword_density.append(0)
                    
                    if(realdensity>0):
                        realdensity = realdensity
                    else:
                        realdensity = 0
                    difference_dencity = (custom_density_flt) - (realdensity)

                    Difference.append(difference_dencity)

                    total_density += realdensity
                    custom_density = str(custom_density_flt)+'%'
                    
                    full_content_arr.append(finaltext)
                    body_content_arr.append(bodytext)

                    tags_h1 = ''
                    for heading in soup.find_all(["h1"]):
                        tags_h1 += heading.text.strip()+' '
                    
                    tags_h2 = ''
                    for heading in soup.find_all(["h2"]):
                        tags_h2 += heading.text.strip()+' '

                    tags_h3 = ''
                    for heading in soup.find_all(["h3"]):
                        tags_h3 += heading.text.strip()+' '

                    tags_h4 = ''
                    for heading in soup.find_all(["h4"]):
                        tags_h4  += heading.text.strip()+' '

                    tags_h5 = ''
                    for heading in soup.find_all(["h5"]):
                        tags_h5 += heading.text.strip()+' '

                    tags_h6 = ''
                    for heading in soup.find_all(["h6"]):
                        tags_h6 += heading.text.strip()+' '
                    
                    title_meta_file = soup.find("title")
                    title_meta = ''
                    if(title_meta_file):
                        title_meta = title_meta_file.text
                        url_title_list.append(title_meta)
                    else:
                        url_title_list.append('')

                    url_mata = ''
                    for tag in soup.find_all(["meta"]):
                        if tag.get("name", None) == "description":
                            url_mata = tag.get("content", None)
                    
                    url_meta_list.append(url_mata)

                    totalkeycount_for_h1 = 0
                    totalkeycount_for_h2 = 0
                    totalkeycount_for_h3 = 0
                    totalkeycount_for_h4 = 0
                    totalkeycount_for_h5 = 0
                    totalkeycount_for_h6 = 0
                    totalkeycount_for_title = 0
                    totalkeycount_for_alltitle = 0
                    totalkeycount_for_bodytext = 0
                    totalkeycount_for_suggested_keyword = 0

                    total_head = tags_h1+' '+tags_h2+' '+tags_h3+' '+tags_h4+' '+tags_h5+' '+tags_h6
                    
                    suggested_keyword = self.get_suggestions(query, targeting_idea_service)
                    
                    

                    for eachword in nouns:
                        wordcount = len(re.findall(eachword.lower() , tags_h1.lower() ))
                        totalkeycount_for_h1 += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'

                        wordcount = len(re.findall(eachword.lower() , tags_h2.lower() ))
                        totalkeycount_for_h2 += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'

                        wordcount = len(re.findall(eachword.lower() +' ', tags_h3.lower() ))
                        totalkeycount_for_h3 += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'

                        wordcount = len(re.findall(eachword.lower() +' ', tags_h4.lower() ))
                        totalkeycount_for_h4 += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'

                        wordcount = len(re.findall(eachword.lower() , tags_h5.lower() ))
                        totalkeycount_for_h5 += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'

                        wordcount = len(re.findall(eachword.lower() , tags_h6.lower() ))
                        totalkeycount_for_h6 += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'

                        wordcount = len(re.findall(eachword.lower(), title_meta.lower() ))
                        totalkeycount_for_title += wordcount
                        #keycounts.append(wordcount)
                        #keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'
                        wordcount = len(re.findall(eachword.lower(), total_head.lower() ))
                        totalkeycount_for_alltitle += wordcount

                        wordcount = len(re.findall(eachword.lower(), bodytext.lower() ))
                        totalkeycount_for_bodytext += wordcount

                        wordcount = len(re.findall(eachword.lower(), suggested_keyword.lower() ))
                        totalkeycount_for_suggested_keyword += wordcount



                    tags_h1_word_count = len(tags_h1.split())
                    tags_h2_word_count = len(tags_h2.split())
                    tags_h3_word_count = len(tags_h3.split())
                    tags_h4_word_count = len(tags_h4.split())
                    tags_h5_word_count = len(tags_h5.split())
                    tags_h6_word_count = len(tags_h6.split())
                    title_word_count = len(title_meta.split())
                    total_title_word_count = len(total_head.split())
                    bodytext_word_count = len(bodytext.split())
                    suggested_keyword_word_count = len(suggested_keyword.split())


                    if(totalkeycount_for_h1>0 and tags_h1_word_count>0):
                        h1_density = round(totalkeycount_for_h1*100/tags_h1_word_count, 2)
                    else:
                        h1_density = 0
                    
                    if(totalkeycount_for_h2>0 and tags_h2_word_count>0):
                        h2_density = round(totalkeycount_for_h2*100/tags_h2_word_count, 2)
                    else:
                        h2_density = 0

                    if(totalkeycount_for_h3>0 and tags_h3_word_count>0):
                        h3_density = round(totalkeycount_for_h3*100/tags_h3_word_count, 2)
                    else:
                        h3_density = 0

                    if(totalkeycount_for_h4>0 and tags_h4_word_count>0):
                        h4_density = round(totalkeycount_for_h4*100/tags_h4_word_count, 2)
                    else:
                        h4_density = 0

                    if(totalkeycount_for_h5>0 and tags_h5_word_count>0):
                        h5_density = round(totalkeycount_for_h5*100/tags_h5_word_count, 2)
                    else:
                        h5_density = 0

                    if(totalkeycount_for_h6>0 and tags_h6_word_count>0):
                        h6_density = round(totalkeycount_for_h6*100/tags_h6_word_count, 2)
                    else:
                        h6_density = 0

                    if(totalkeycount_for_title>0 and title_word_count>0):
                        title_density = round(totalkeycount_for_title*100/title_word_count, 2)
                    else:
                        title_density = 0
                    
                    if(totalkeycount_for_alltitle>0 and total_title_word_count>0):
                        total_title_density = round(totalkeycount_for_alltitle*100/total_title_word_count, 2)
                    else:
                        total_title_density = 0


                    if(totalkeycount_for_bodytext>0 and bodytext_word_count>0):
                        bodytext_density = round(totalkeycount_for_bodytext*100/bodytext_word_count, 2)
                    else:
                        bodytext_density = 0

                    if(totalkeycount_for_suggested_keyword>0 and suggested_keyword_word_count>0):
                        suggested_keyword_density =  round(totalkeycount_for_suggested_keyword*100/suggested_keyword_word_count, 2)
                    else:
                        suggested_keyword_density =  0    


                    custom_url_density.append(custom_density)

                    title_h1.append(str(h1_density)+'%')
                    title_h2.append(str(h2_density)+'%')
                    title_h3.append(str(h3_density)+'%')
                    title_h4.append(str(h4_density)+'%')
                    title_h5.append(str(h5_density)+'%')
                    title_h6.append(str(h6_density)+'%')

                    title_density_arr.append(str(title_density)+'%')
                    total_title_density_arr.append(str(total_title_density)+'%')
                    bodytext_density_arr.append(str(bodytext_density)+'%')

                    if(tagstatus==1):
                        tagstatus_dict.append('Sequenced')
                    else:
                        tagstatus_dict.append('Not Sequenced')
                    
                    #saving data in list data
                    

                    newresult = googlesearchresultData(id = newurl.pk, result_id = newdoc.pk, search_url = i, keyword_density = realdensity, url_keyword_density = custom_density, individual_keyword_density = individual_key_density, file_path = urlfilename, search_position = ii, h1_tag = h1_density, h2_tag = h2_density, h3_tag = h3_density, h4_tag = h4_density, h5_tag = h5_density, h6_tag = h6_density, url_title = title_density, all_title = total_title_density, bodytext = bodytext_density, suggest_key = suggested_keyword, suggest_key_density = suggested_keyword_density, tagstatus = tagstatus )
                    newresult.save()
                    search_position.append(ii)
                    if(ii>19):
                        break
                        #print(heading.name + ' ' + heading.text.strip())
                    #print(i)

                
                
                # Create report for each Query ------------------------------------------
                #dict1 = {'Search Position':search_position, 'Search Query': query, 'Keyword Density': keyword_density, 'Custom URL Density': custom_url_density, 'Difference':Difference, 'H1 tag':title_h1, 'H2 tag':title_h2, 'H3 tag':title_h3, 'H4 tag':title_h4, 'H5 tag':title_h5, 'H6 tag':title_h6, 'URL title':url_title_list, 'URL Meta': url_meta_list, 'Custom URL Title': custom_url_title, 'Custom URL Meta':custom_url_mata, 'url': my_results_list }  
                #dict1 = {'Search Position':search_position, 'Search Query': query, 'Keyword Density': keyword_density, 'Custom URL Density': custom_url_density, 'Difference':Difference, 'H1 tag':title_h1, 'H2 tag':title_h2, 'H3 tag':title_h3, 'H4 tag':title_h4, 'H5 tag':title_h5, 'H6 tag':title_h6, 'URL title':url_title_list, 'URL Meta': url_meta_list, 'Custom URL Title': custom_url_title, 'Custom URL Meta':custom_url_mata, 'url': my_results_list, 'full_content_arr':full_content_arr,'body_content_arr': body_content_arr }  
                
                
                lstexcludezero  = list(filter(lambda a: a !=0, keyword_density))
                print('rrrrrrrrrrrrrrrr')
                print(lstexcludezero)
                listdiffrece = 0
                if(lstexcludezero):
                    listdiffrece = max(lstexcludezero) - min(lstexcludezero)
                print(listdiffrece)
                print('00000000000')
                if(suggested_keyword_density):
                    suggest_keydensity = str(suggested_keyword_density)+'%'
                else:
                    suggest_keydensity = '0%'
                
                #suggest_keydensity
                dict1 = {'Search Position':search_position, 'URL': my_results_list, 'Total Keyword Density': keyword_density, 'Individual Keyword Density':all_keyword_density,  'Client URL Keyword Density': custom_url_density, 'Difference':Difference, 'Recommended Keywords': suggested_keyword, 'Recommended Keyword Density': (str(listdiffrece)+'%'), 'H1 Tag Density':title_h1, 'H2 Tag Density':title_h2, 'H3 Tag Density':title_h3, 'H4 Tag Density':title_h4, 'H5 Tag Density':title_h5, 'H6 Tag Density':title_h6, 'Header Sequence':tagstatus_dict, 'Meta title Density':title_density_arr, 'All Header Density': total_title_density_arr, 'Body Text Density': bodytext_density_arr }  
                dict2 = {'Total Keyword Density': keyword_density}
                
                df2 = pd.DataFrame(dict2) 
                denpos = 0
                densityorder = df2.sort_values(by ='Total Keyword Density',  ascending=False, ignore_index=True )
                #print(densityorder)
                for index, row in densityorder.iterrows():
                    denpos += 1
                    #print(row['Total Keyword Density'])
                    if(row['Total Keyword Density']>0):
                        seq_num = row['Total Keyword Density']
                    else:
                        seq_num = 0
                    nested_q = googlesearchresultData.objects.filter(keyword_density=seq_num, result_id = newdoc.pk, density_position__isnull=True)[0:1]
                    #print(nested_q)
                    if(len(nested_q)>0 and nested_q[0] and nested_q[0].id>0):
                        if('wikipedia' in nested_q[0].search_url):
                            googlesearchresultData.objects.filter(pk=nested_q[0].id).update(density_position=21, suggest_key_density = listdiffrece)
                        else:
                            googlesearchresultData.objects.filter(pk=nested_q[0].id).update(density_position=denpos, suggest_key_density = listdiffrece)
                    

                filename = settings.FILES_GOOGLE_RESULT+'google_search_result'+ str(newdoc.pk)+'.xlsx'
                try:
                    os.unlink(filename)
                except:
                    pass

                df = pd.DataFrame(dict1) 
                #df = df.sort_values(by ='Total Keyword Density', ascending=False, ignore_index=True )
                df['Total Keyword Density'] = df['Total Keyword Density'].apply( lambda x : str(x) + '%')
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)

                # Get workbook
                workbook = writer.book
                # Get Sheet1
                worksheet = writer.sheets['Sheet1']

                '''cell_format = workbook.add_format()
                cell_format.set_bold()
                cell_format.set_font_color('blue')

                worksheet.set_column('B:B', None, cell_format)'''
                colors = ['#FF0000','#FF3400','#FF4600','#FF6900','#FF7B00','#FF8C00','#FF9E00','#FFC100','#FFE400','#FFF600','#F7FF00','#E5FF00','#D4FF00','#C2FF00','#9FFF00','#7CFF00','#6AFF00','#47FF00','#35FF00','#00FF00']
                colors.reverse()
                for io in range(20): # integer odd-even alternation 
                    if io in wikipedia_ar:
                        bg_format1 = workbook.add_format({'bg_color': '#A9A9A9'})
                    else:
                        bg_format1 = workbook.add_format({'bg_color': colors[io]})

                    worksheet.set_row(io+1, cell_format=(bg_format1 ))

                #exldata = pd.read_excel(fn, header=None)
                minusvalue = workbook.add_format({'bg_color': '#FFFFFF', 'font_color': '#ff0000', 'bold': True })
                '''for it in range(20):
                    for io in range(18):
                        cell_value = worksheet.cell(row_number, column_number).value
                        if(cell_value and int(cell_value)<0):
                            worksheet.write_string(it, io, cell_value, minusvalue)'''


                worksheet.conditional_format('A2:R21',
                                                    {
                                                        'type'     : 'cell',
                                                        'criteria' : '<',
                                                        'value'    : 0,
                                                        'format'   : minusvalue
                                                    }
                                                )
                                            
                worksheet.write(22, 3, "Average: "+str(round(total_density/20,2))+"%") 
                workbook.close()

                # Create PDF for each query -------------------------------
                #, sheetname='Sheet1'
                data_frame_excel = pd.ExcelFile(filename)
                df = data_frame_excel.parse('Sheet1')
                htmlfile = filename.replace('.xlsx','.html')
                df.to_html(htmlfile)
                #pdf.from_file(htmlfile, filename.replace('.xlsx','.pdf'))

                #writer.save()
                #df.to_csv(filename)
                #
                

                
                updatedoc = googlesearchresult(id = newdoc.pk, file_path = filename, search_query = query, custom_url = custom_url)
                updatedoc.save()


        #return HttpResponse('ggg')
        '''for afile in request.FILES.getlist('files_multiple'):
            newdoc = ReportFiles(filename = afile, name = afile, section = request.POST["section"])
            newdoc.save()'''

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>Excel Download </a>", url='/google-report-file/download?recid='+str(obj.id))


    def search_result(self, obj):
        return format_html("<a target='_blank' href='{url}' >Query Result", url='/admin/googlesearchresult/googlesearchresultdata/?q='+str(obj.id))


    
    def all_actions(self,obj):
        return False
        return format_html('<span class="changelink"><a href="{url}">Edit</a></span>', url='/admin/posts/help/'+str(obj.id)+'/change')
    all_actions.short_description = 'actions'

#from advanced_filters.admin import AdminAdvancedFiltersMixin



class MyChangeList(ChangeList):
    #print(ChangeList)
    def get_results(self, *args, **kwargs):
        print(args[0].GET)
        print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        super(MyChangeList, self).get_results(*args, **kwargs)
        
        self.paramq = args[0].GET['q']
        print(self.paramq)
        print(args[0].GET)
        #print(args[0].REQUEST)
        #print(self.result_list)

        #if(args[0] and args[0].GET['density']):
        #    self.result_list = self.result_list[:args[0].GET['density']]
        #density = request.GET.pop('density', None)
        #if(density):
        #    self.result_list = self.result_list[:density]
        #if(self.result_list[0].keyword_density == 1.2):
        #if():
        for getlink in self.result_list:
            print(getlink)

        q = self.result_list.aggregate(density_sum=Sum('keyword_density'))
        #print(self.result_list)
        #self.densityvar = request.query_params.get('status', None)
        #print(self)
        
        if(q['density_sum']):
            self.density_count = str(round(q['density_sum']/20,2))+'%'



class googleResultAdmin( admin.ModelAdmin):
    parameter_name = '_afilter'
    #print(GET('density', None))
    #requests.pop('_cfilter', None)
    #'result_search_query',  'search_result',
    #, 'h1_tag', 'h2_tag', 'h3_tag', 'h4_tag', 'h5_tag', 'h6_tag', 'url_title', 'url_meta'
    list_display = ( 'My_keyword_density', 'My_individual_keyword_density', 'My_url_keyword_density', 'show_report', 'search_url', 'search_position', 'density_position', 'my_suggest_key', 'my_suggest_key_density', 'My_h1_tag', 'My_h2_tag', 'My_h3_tag', 'My_h4_tag', 'My_h5_tag', 'My_h6_tag', 'my_tagstatus', 'My_url_title', 'My_all_title', 'My_bodytext' )
    list_per_page = 20
    #list_filter  = ('result__search_query',)
    search_fields = ('result__search_query', 'result__id', )
    #search_fields = ('result__search_query','keyword_density')
    #ordering = ['-keyword_density']
    ordering = ['search_position']
    #change_list_template = 'change_list_graph.html'

    
    '''def lookups___________hhhhhhhhh(self, request, model_admin):
        list_per_page = 2
        if not model_admin:
            raise Exception('Cannot use AdvancedListFilters without a '
                            'model_admin')
        model_name = "%s.%s" % (model_admin.model._meta.app_label,
                                model_admin.model._meta.object_name)
        return AdvancedFilter.objects.filter_by_user(request.user).filter(
            model=model_name).values_list('id', 'title')'''

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        request.GET = request.GET.copy()
        density = request.GET.pop('density', None)
        qs = super(googleResultAdmin, self).get_queryset(request)
        
        showperpage = 0
        if(density):
            
            #request.user.is_superuser:
            densityvar = density[0]
            googlerecid = request.GET['q']
            #return qs.filter(keyword_density__gte = densityvar).order_by('-keyword_density')
            qs =  qs.filter(result__id = googlerecid).order_by('search_position')

            qs2 = qs[:int(densityvar)]
            #print(type(qs2))

            #http://192.168.43.77:8080/admin/googlesearchresult/googlesearchresultdata/?q=158&density=2
            #qs =  qs[:2]
            querydata = []
            for items in qs2:
                #print(items.id)
                querydata.append( items.id )

            #print(qs)
            #qs =  qs.filter(result__id = googlerecid).order_by('keyword_density')
            qs1 = googlesearchresultData.objects.filter(pk__in=querydata)
            #this was the main list which show 
            #return qs.filter(keyword_density=density)
            print('gogogoggogo')
            #print(qs)
            
            return qs1
        
        return qs
        
        '''queryset = queryset.in_distance(
                radius[0], fields=['location__latitude', 'location__longitude'],
                points=[lat, lon])
        return queryset'''
    
    #self.request

    def getparams():
        return self.request

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqa')
        print(request)

        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '80s':
            return queryset.filter()

    #this is not calling by default
    def get_changelist(self, request, **kwargs):
        print('lllllllllllllllllllllllggggggggggggggggggggggggg')
        class SortedChangeList(ChangeList):
            def get_query_set(self, *args, **kwargs):
                qs = super(SortedChangeList, self).get_query_set(*args, **kwargs)
                return qs.annotate(amt=Sum('entry__amount')).order_by('-amt')
                 
        if request.GET.get('density'):
            return ChangeList
             
        return SortedChangeList

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = 'asfsfdsfdgdgsdgfdsg'
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_averate(self):
        #functions to calculate whatever you want...
        total = googlesearchresultData.objects.all().aggregate(tot=Sum('total'))['tot']
        return total

    def get_changelist(self, request):
        #self.request = request
        print(MyChangeList)
        #listdata = MyChangeList[0:3]
        return MyChangeList

    #calling by default
    def changelist_view(self, request, extra_context=None):
        print('jjjjjjjjjjjjjjjjjjjjjjjjjj')
        
        ChangeList = self.get_changelist(request)

        

        self.request = request
        extra_context = extra_context or {}
        '''my_context = {
            'total': self.get_averate(),
        }'''
        print(self)

        extra_context['density_count1'] = 8098
        print('reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        if request.GET.get('from_date') is not None:
            extra_context['from_date'] = request.GET.get('from_date')
        else:
            extra_context['from_date'] = ''

        return super(googleResultAdmin, self).changelist_view(request, extra_context=extra_context)

    

    def queryset1000000(self, request, queryset):
        if self.value():
            filters = AdvancedFilter.objects.filter(id=self.value())
            if hasattr(filters, 'first'):
                advfilter = filters.first()
            if not advfilter:
                logger.error("AdvancedListFilters.queryset: Invalid filter id")
                return queryset
            query = advfilter.query
            logger.debug(query.__dict__)
            return queryset.filter(query).distinct()
        return queryset

    def change_v__kshfkjsdhfjkdshfk_iew(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['asf'] = 'akshfasfkhafhsakhflkasfklshfl'
        return super(googleResultAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def changelist__wyrwyriwy_view(self, request, *args, **kwargs):
        self.request = request
        return super().changelist_____kjashdjhsajkd_view(request, *args, **kwargs)
    
    #get field data 
    def My_url_keyword_density(self, instance):
        return instance.url_keyword_density
        #Total Keyword Density
    My_url_keyword_density.short_description = 'Client URL Keyword Density'


    def My_individual_keyword_density(self, instance):
        return instance.individual_keyword_density
        #Total Keyword Density
    My_individual_keyword_density.short_description = format_html('<span class="table_head" >Individual Keyword Density<span class="table_head_tooltip" data-toggle="tooltip" data-placement="bottom" title="Individual keyword is the density of the individual words in the keyword phrase included in the body content and headers." ><img src="/static/img/tooltip.png" width="25px" /> </span></span>')
    My_individual_keyword_density.admin_order_field   = 'individual_keyword_density'

    def My_keyword_density(self, instance):
        return instance.keyword_density+'%'
        #Total Keyword Density
    My_keyword_density.short_description = format_html('<span class="table_head" >Total Keyword Density<span class="table_head_tooltip" data-toggle="tooltip" data-placement="bottom" title="Total Keyword Density is the density of the keyword phrase included in the body content and headers." ><img src="/static/img/tooltip.png" width="25px" /> </span></span>')
    My_keyword_density.admin_order_field   = 'keyword_density'

    def My_h1_tag(self, instance):
        return str(instance.h1_tag)+'%'
    My_h1_tag.short_description = 'H1 tag Density'
    #My_h1_tag.short_description = format_html('<span class="table_head" >H1 tag Density<span class="table_head_tooltip" data-toggle="tooltip" data-placement="bottom" title="Total Keyword Density is the density of the keyword phrase included in the body content and headers." ><img src="/static/img/tooltip.png" width="25px" /> </span></span>')

    def My_h2_tag(self, instance):
        return str(instance.h2_tag)+'%'
    My_h2_tag.short_description = 'H2 tag Density'

    def My_h3_tag(self, instance):
        return str(instance.h3_tag)+'%'
    My_h3_tag.short_description = 'H3 tag Density'

    def My_h4_tag(self, instance):
        return str(instance.h4_tag)+'%'
    My_h4_tag.short_description = 'H4 tag Density'

    def My_h5_tag(self, instance):
        return str(instance.h5_tag)+'%'
    My_h5_tag.short_description = 'H5 tag Density'

    def My_h6_tag(self, instance):
        return str(instance.h6_tag)+'%'
    My_h6_tag.short_description = 'H6 tag Density'

    def my_tagstatus(self, instance):
        if(instance.tagstatus==1):
            return 'Sequenced'
        else:
            return 'Not Squenced'
    my_tagstatus.short_description = 'Header Sequence'

    def My_url_title(self, instance):
        return str(instance.url_title)+'%'
    My_url_title.short_description = 'Meta Title Density'

    def My_all_title(self, instance):
        return str(instance.all_title)+'%'
    My_all_title.short_description = 'All Header Density'

    def My_bodytext(self, instance):
        return str(instance.bodytext)+'%'
    My_bodytext.short_description = 'Body Text Density'

    def my_suggest_key(self, instance):
        if(instance.suggest_key):
            return str(instance.suggest_key)
        else:
            pass

    my_suggest_key.short_description = 'Recommended Keywords'
    
    def my_suggest_key_density(self, instance):
        if(instance.suggest_key_density):
            return str(instance.suggest_key_density)+'%'
        else:
            pass
    my_suggest_key_density.short_description = 'Recommended Keyword Density'

    #My_keyword_density.short_description = '<a href="">Total Keyword Density</a>'
        
    def result_search_query(self, instance):
        return instance.result.search_query

    def has_add_permission(self, request):
        return False

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>Excel Download </a>", url='/google-report-file/keyword-density-download?recid='+str(obj.id))


    def search_result(self, obj):
        return format_html("<a target='_blank' href='{url}'>Keyword Density", url='/admin/googlesearchresult/keyworddensity/?q='+str(obj.id))


class keywordDensityAdmin(admin.ModelAdmin):
    list_display = ('result_search_query', 'keyword', 'count', 'keyword_density' )
    list_per_page = 100
    search_fields = ('rec__id',)

    def result_search_query(self, instance):
        return instance.rec.search_url

    def has_add_permission(self, request):
        return False
        

admin.site.register(googlesearchresult, GoogleSearchResultAdmin)

admin.site.register(googlesearchresultData, googleResultAdmin )
admin.site.register(keywordDensity, keywordDensityAdmin )