from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import googlesearchresult, googlesearchresultData
from django.utils.html import format_html
# Register your models here.

import pandas
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

class GoogleSearchResultAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ( 'search_query', 'custom_url', 'show_report', 'all_actions')
    search_fields = ('search_query', )
    list_display_links = ('all_actions',)
    
    fieldsets = (
        (None, {
            'fields': ('search_query', 'custom_url', 'status'),
            'description': "<h3>Enter a single search query you would like to search in Google.  Note: Search Query Report takes a few minutes to create. </h3>."
        }),
    )

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>Download Trending Report</a>", url='/google/trends?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Rising Report</a>", url='/google/keyword-rising?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Top Related Report</a>", url='/google/related-query/?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Suggestions Report</a>", url='/google/suggestions-keyword?recid='+str(obj.id))
    

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

        custom_url_text = ''
        try:
            html = urllib.request.urlopen(custom_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(self.tag_visible, texts)  
            custom_url_text = u" ".join(t.strip() for t in visible_texts)
        except:
            pass
        #print(text_from_html(html))


        
        querylist = query_post.split("\n")
        print(querylist)
        #return
        for query in querylist:
            if(query and query!=''):
                my_results_list = []
                title = []
                text_content = []
                keyword_density = []
                custom_url_density = []
                
                Nkr = []
                Tkn = []
                ii = 0

                custom_textarray = len(custom_url_text.split(query))
                custom_textarray_tkn = len(custom_url_text.split(' '))
                custom_density = custom_textarray*100/custom_textarray_tkn;
                newdoc = googlesearchresult.objects.create(search_query = query, custom_url = custom_url, status = 'A')
                #newdoc = googlesearchresult(search_query = query, status = 'A')
                newdoc.save()
                #print(newdoc.pk)
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
                        reqs = requests.get(i,stream=True, timeout=10)
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

                    Nkr.append(textarray)
                    Tkn.append(textarray_tkn)
                    query_density = textarray*100/textarray_tkn
                    keyword_density.append(query_density)
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

                    newresult = googlesearchresultData(result_id = newdoc.pk, search_url = i, keyword_density = query_density, url_keyword_density = custom_density)
                    newresult.save()

                    if(ii>19):
                        break
                        #print(heading.name + ' ' + heading.text.strip())
                    #print(i)

                    

                #, 'text_content': text_content,
                dict1 = {'keys': query, 'url': my_results_list, 'titles':title, 'Nkr': Nkr, 'Tkn':Tkn, 'Keyword Density': keyword_density, 'Custom URL Density': custom_url_density }  
                filename = settings.FILES_GOOGLE_RESULT+'google_search_result'+ str(timenow)+'.csv'
                try:
                    os.unlink(filename)
                except:
                    pass

                df = pandas.DataFrame(dict1) 
                df.to_csv(filename)

                updatedoc = googlesearchresult(id = newdoc.pk, file_path = filename, search_query = query, custom_url = custom_url, status = 'A')
                updatedoc.save()
            

            

        #return HttpResponse('ggg')
        '''for afile in request.FILES.getlist('files_multiple'):
            newdoc = ReportFiles(filename = afile, name = afile, section = request.POST["section"])
            newdoc.save()'''

    def show_report(self, obj):
        return format_html("<a target='_blank' href='{url}'>File Download for Report</a>", url='/google-report-file/download?recid='+str(obj.id))
    
    def all_actions(self,obj):
        return format_html('<span class="changelink"><a href="{url}">Edit</a></span>', url='/admin/posts/help/'+str(obj.id)+'/change')
    all_actions.short_description = 'actions'



class googleResultAdmin(admin.ModelAdmin):
    list_display = ('search_url', 'keyword_density', 'url_keyword_density')
    list_per_page = 20
    search_fields = ('result',)

admin.site.register(googlesearchresult, GoogleSearchResultAdmin)

admin.site.register(googlesearchresultData, googleResultAdmin )
