from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import googlesearchresult, googlesearchresultData, keywordDensity
from django.utils.html import format_html
# Register your models here.

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

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class GoogleSearchResultAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ( 'id','search_query', 'custom_url', 'search_result', 'show_report', 'all_actions')
    search_fields = ('search_query', )
    list_display_links = ('all_actions',)
    
    fieldsets = (
        (None, {
            'fields': ('search_query', 'custom_url', 'status'),
            'description': "<h3>Enter a single search query OR multiple search queries separated by a new line. <br> Note: A Search Query Report takes a few minutes to create. <br>Multiple Search Queries take longer than a single Search Query KD report for example. </h3>."
        }),
    )

    #def show_report(self, obj):
    #    return format_html("<a target='_blank' href='{url}'>Download Trending Report</a>", url='/google/trends?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Rising Report</a>", url='/google/keyword-rising?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Top Related Report</a>", url='/google/related-query/?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Suggestions Report</a>", url='/google/suggestions-keyword?recid='+str(obj.id))
    

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def save_model(self, request, obj, form, change):
        #print(request.POST['search_query'])
        query_post = request.POST['search_query']
        custom_url = request.POST['custom_url']
        timenow = timezone.now().strftime('%Y%m%d%H%M%S')
        #files = request.FILES.getlist('file_field')
    
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,} 
        request_data = urllib.request.Request(custom_url,None,headers) #The assembled request
        html = urllib.request.urlopen(request_data).read()

        #html = urllib.request.urlopen(custom_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        custom_url_text = u" ".join(t.strip() for t in visible_texts)

        #print(text_from_html(html))


        
        querylist = query_post.split("\n")
        print(querylist)
        #return
        for query_item in querylist:
            query = query_item.strip()
            if(query and query!=''):
                my_results_list = []
                title = []
                text_content = []
                keyword_density = []
                custom_url_density = []
                all_keyword_density = []
                Nkr = []
                Tkn = []
                ii = 0

                custom_textarray = len(custom_url_text.split(query))
                custom_textarray_tkn = len(custom_url_text.split(' '))

                custom_density = str(round(custom_textarray*100/custom_textarray_tkn, 2))+'%';
                newdoc = googlesearchresult.objects.create(search_query = query, custom_url = custom_url, status = 'A')
                #newdoc = googlesearchresult(search_query = query, status = 'A')
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
                    ii+=1
                    #print(newdoc.pk)
                    texts = ''
                    #print(i)

                    try:
                        reqs = requests.get(i,stream=True, timeout=10, headers=headers)
                        reqs.raise_for_status()
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        #print("List of all the h1, h2, h3 :")
                        texts = soup.findAll(text=True)

                    except:
                        pass
                    
                    
                    visible_texts = filter(self.tag_visible, texts) 
                    finaltext = u" ".join(t.strip() for t in visible_texts)
                    finaltext = finaltext.lstrip().rstrip()
                    textarray = len(finaltext.split(query))
                    textarray_tkn = len(finaltext.split(' '))

                    newurl = googlesearchresultData.objects.create(result_id = newdoc.pk)
                    newurl.save()

                    #density for each keywords
                    totalwordcount = 0
                    keycounts = []
                    keydensity = []
                    for eachword in nouns:
                        wordcount = len(re.findall(eachword.lower() +' ', finaltext.lower() ))
                        totalwordcount += wordcount
                        keycounts.append(wordcount)
                        keydenc = str(round(wordcount*100/textarray_tkn, 2))+'%'
                        keydensity.append(keydenc)

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
                        query_density = str(round(textarray*100/textarray_tkn, 2))+'%'
                        keyword_density.append(round(textarray*100/textarray_tkn, 2))
                        individual_key_density = str(round(totalwordcount*100/textarray_tkn, 2))+'%'
                        all_keyword_density.append(individual_key_density)
                    else:
                        query_density = 0
                        individual_key_density = 0
                        keyword_density.append(0)
                        all_keyword_density.append(0)

                    tags = []
                    textnum = 0
                    for heading in soup.find_all(["h1", "h2", "h3"]):
                        tags.append(heading.text.strip())
                        textnum+=1
                        if(textnum>9):
                            break
                    
                    text_dict = []
                    textnum = 0
                    total_content = ''
                    for detail in soup.find_all(["p"]):
                        text_dict.append(detail.text.strip())
                        textnum+=1
                        total_content 
                        if(textnum>9):
                            break

                    #title.append(heading)
                    title.append(tags)
                    text_content.append(text_dict)
                    custom_url_density.append(custom_density)

                    newresult = googlesearchresultData(id = newurl.pk, result_id = newdoc.pk, search_url = i, keyword_density = query_density, url_keyword_density = custom_density, individual_keyword_density = individual_key_density, file_path = urlfilename )
                    newresult.save()

                    if(ii>19):
                        break
                        #print(heading.name + ' ' + heading.text.strip())
                    #print(i)

                    

                #, 'text_content': text_content,
                dict1 = {'keys': query, 'url': my_results_list, 'titles':title, 'Nkr': Nkr, 'Tkn':Tkn, 'Keyword Density': keyword_density, 'Custom URL Density': custom_url_density, 'text_content': text_content }  
                filename = settings.FILES_GOOGLE_RESULT+'google_search_result'+ str(newdoc.pk)+'.xlsx'
                try:
                    os.unlink(filename)
                except:
                    pass

                df = pd.DataFrame(dict1) 
                df = df.sort_values(by ='Keyword Density', ascending=False )
                df['Keyword Density'] = df['Keyword Density'].apply( lambda x : str(x) + '%')
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1')

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
                for i in range(20): # integer odd-even alternation 
                    bg_format1 = workbook.add_format({'bg_color': colors[i]})
                    worksheet.set_row(i+1, cell_format=(bg_format1 ))

                #writer.save()
                #df.to_csv(filename)
                #
                

                workbook.close()
                updatedoc = googlesearchresult(id = newdoc.pk, file_path = filename, search_query = query, custom_url = custom_url, status = 'A')
                updatedoc.save()


        #return HttpResponse('ggg')
        '''for afile in request.FILES.getlist('files_multiple'):
            newdoc = ReportFiles(filename = afile, name = afile, section = request.POST["section"])
            newdoc.save()'''

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>CSV Download </a>", url='/google-report-file/download?recid='+str(obj.id))


    def search_result(self, obj):
        return format_html("<a target='_blank' href='{url}'>Query Result", url='/admin/googlesearchresult/googlesearchresultdata/?q='+str(obj.search_query))


    
    def all_actions(self,obj):
        return format_html('<span class="changelink"><a href="{url}">Edit</a></span>', url='/admin/posts/help/'+str(obj.id)+'/change')
    all_actions.short_description = 'actions'



class googleResultAdmin(admin.ModelAdmin):
    list_display = ('result_search_query', 'keyword_density', 'individual_keyword_density', 'url_keyword_density', 'show_report', 'search_result', 'search_url')
    list_per_page = 100
    list_filter  = ('keyword_density',)
    #search_fields = ('result__search_query',)
    search_fields = ('result_search_query','keyword_density')

    def result_search_query(self, instance):
        return instance.result.search_query

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>CSV Download </a>", url='/google-report-file/keyword-density-download?recid='+str(obj.id))


    def search_result(self, obj):
        return format_html("<a target='_blank' href='{url}'>Keyword Density", url='/admin/googlesearchresult/keyworddensity/?q='+str(obj.id))


class keywordDensityAdmin(admin.ModelAdmin):
    list_display = ('result_search_query', 'keyword', 'count', 'keyword_density' )
    list_per_page = 100
    search_fields = ('rec__id',)

    def result_search_query(self, instance):
        return instance.rec.search_url
        

admin.site.register(googlesearchresult, GoogleSearchResultAdmin)

admin.site.register(googlesearchresultData, googleResultAdmin )
admin.site.register(keywordDensity, keywordDensityAdmin )