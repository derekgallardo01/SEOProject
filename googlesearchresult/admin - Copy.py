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
import pdfkit as pdf

from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Sum

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class MyChangeList(ChangeList):

    def get_results(self, *args, **kwargs):
        super(MyChangeList, self).get_results(*args, **kwargs)
        #print(self.result_list)
        q = self.result_list.aggregate(density_sum=Sum('keyword_density'))
        self.density_count = str(round(q['density_sum']/20,2))+'%'


class GoogleSearchResultAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ( 'created_at','search_query', 'custom_url', 'search_result', 'show_report')
    search_fields = ('search_query', )
    #list_display_links = ('all_actions',)
    
    fieldsets = (
        (None, {
            'fields': ('search_query', 'custom_url', ),
            'description': "<h3>Enter a single search query OR multiple search queries separated by a new line. <br> Note: A Search Query Report takes a few minutes to create. <br>Multiple Search Queries take longer than a single Search Query KD report for example. </h3>."
        }),
    )


    
        
    #def show_report(self, obj):
    #    return format_html("<a target='_blank' href='{url}'>Download Trending Report</a>", url='/google/trends?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Rising Report</a>", url='/google/keyword-rising?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Top Related Report</a>", url='/google/related-query/?recid='+str(obj.id))+format_html("<br /><br /><a target='_blank' href='{url}'>Download Keyword Suggestions Report</a>", url='/google/suggestions-keyword?recid='+str(obj.id))
    
    def my_view(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           key=value,
        )
        return TemplateResponse(request, "sometemplate.html", context)

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
                ii = 0

                custom_textarray = len(re.findall(query.lower(), custom_url_text.lower() ))
                #len(custom_url_text.split(query))
                custom_textarray_tkn = len(custom_url_text.split())

                custom_density = str(round(custom_textarray*100/custom_textarray_tkn, 2))+'%';
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
                        keyword_density.append(0)
                        all_keyword_density.append(0)


                    total_density += realdensity
                    
                    Difference.append(round(custom_textarray*100/custom_textarray_tkn, 2)-round(textarray*100/textarray_tkn, 2) )

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

                    total_head = tags_h1+' '+tags_h2+' '+tags_h3+' '+tags_h4+' '+tags_h5+' '+tags_h6

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



                    tags_h1_word_count = len(tags_h1.split())
                    tags_h2_word_count = len(tags_h2.split())
                    tags_h3_word_count = len(tags_h3.split())
                    tags_h4_word_count = len(tags_h4.split())
                    tags_h5_word_count = len(tags_h5.split())
                    tags_h6_word_count = len(tags_h6.split())
                    title_word_count = len(title_meta.split())
                    total_title_word_count = len(total_head.split())
                    bodytext_word_count = len(bodytext.split())



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


                    #title.append(heading)
                    title_h1.append(tags_h1)
                    title_h2.append(tags_h2)
                    title_h3.append(tags_h3)
                    title_h4.append(tags_h4)
                    title_h5.append(tags_h5)
                    title_h6.append(tags_h6)

                    custom_url_density.append(custom_density)

                    
                    newresult = googlesearchresultData(id = newurl.pk, result_id = newdoc.pk, search_url = i, keyword_density = realdensity, url_keyword_density = custom_density, individual_keyword_density = individual_key_density, file_path = urlfilename, search_position = ii, h1_tag = h1_density, h2_tag = h2_density, h3_tag = h3_density, h4_tag = h4_density, h5_tag = h5_density, h6_tag = h6_density, url_title = title_density, all_title = total_title_density, bodytext = bodytext_density )
                    newresult.save()
                    search_position.append(ii)
                    if(ii>19):
                        break
                        #print(heading.name + ' ' + heading.text.strip())
                    #print(i)

                
                '''keyword_density.append("Average: "+str(total_density/20)+"%")
                search_position.append('')
                custom_url_density.append('')
                Difference.append('')
                title_h1.append('')
                title_h2.append('')
                title_h3.append('')
                title_h4.append('')
                title_h5.append('')
                title_h6.append('')
                url_title_list.append('')
                url_meta_list.append('')
                #custom_url_title.append('')
                #custom_url_mata.append('')
                my_results_list.append('')'''
                #, 'text_content': finaltext,
                #'Nkr': Nkr, 'Tkn':Tkn,
                # Create report for each Query ------------------------------------------
                #dict1 = {'Search Position':search_position, 'Search Query': query, 'Keyword Density': keyword_density, 'Custom URL Density': custom_url_density, 'Difference':Difference, 'H1 tag':title_h1, 'H2 tag':title_h2, 'H3 tag':title_h3, 'H4 tag':title_h4, 'H5 tag':title_h5, 'H6 tag':title_h6, 'URL title':url_title_list, 'URL Meta': url_meta_list, 'Custom URL Title': custom_url_title, 'Custom URL Meta':custom_url_mata, 'url': my_results_list }  
                dict1 = {'Search Position':search_position, 'Search Query': query, 'Keyword Density': keyword_density, 'Custom URL Density': custom_url_density, 'Difference':Difference, 'H1 tag':title_h1, 'H2 tag':title_h2, 'H3 tag':title_h3, 'H4 tag':title_h4, 'H5 tag':title_h5, 'H6 tag':title_h6, 'URL title':url_title_list, 'URL Meta': url_meta_list, 'Custom URL Title': custom_url_title, 'Custom URL Meta':custom_url_mata, 'url': my_results_list }  
                filename = settings.FILES_GOOGLE_RESULT+'google_search_result'+ str(newdoc.pk)+'.xlsx'
                try:
                    os.unlink(filename)
                except:
                    pass

                df = pd.DataFrame(dict1) 
                denpos = 0
                densityorder = df.sort_values(by ='Keyword Density',  ascending=False, ignore_index=True )
                for index, row in densityorder.iterrows():
                    denpos += 1
                    nested_q = googlesearchresultData.objects.filter(keyword_density=row['Keyword Density'], result_id = newdoc.pk, density_position__isnull=True)[0:1]
                    #print(nested_q)
                    googlesearchresultData.objects.filter(pk=nested_q[0].id).update(density_position=denpos)
                    #googlesearchresultData.objects.filter(keyword_density=row['Keyword Density'], result_id = newdoc.pk, density_position__isnull=True).update(density_position=denpos)
                

                df = df.sort_values(by ='Keyword Density', ascending=False, ignore_index=True )
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

                worksheet.write(22, 3, "Average: "+str(total_density/20)+"%") 
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



class googleResultAdmin(admin.ModelAdmin):
    #'result_search_query',  'search_result',
    #, 'h1_tag', 'h2_tag', 'h3_tag', 'h4_tag', 'h5_tag', 'h6_tag', 'url_title', 'url_meta'
    list_display = ( 'My_keyword_density', 'individual_keyword_density', 'My_url_keyword_density', 'show_report', 'search_url', 'search_position', 'density_position', 'My_h1_tag', 'My_h2_tag', 'My_h3_tag', 'My_h4_tag', 'My_h5_tag', 'My_h6_tag', 'My_url_title', 'My_all_title', 'My_bodytext' )
    list_per_page = 100
    #list_filter  = ('result__search_query',)
    search_fields = ('result__search_query', 'result__id', )
    #search_fields = ('result__search_query','keyword_density')
    #ordering = ['-keyword_density']
    ordering = ['search_position']
    
    def get_changelist(self, request):
        return MyChangeList

    def My_url_keyword_density(self, instance):
        return instance.url_keyword_density+'%'
        #Total Keyword Density
    My_url_keyword_density.short_description = 'Client URL Keyword Density'

    def My_keyword_density(self, instance):
        return instance.keyword_density+'%'
        #Total Keyword Density
    My_keyword_density.short_description = format_html('<span class="table_head" >Total Keyword Density<span class="table_head_tooltip" data-toggle="tooltip" data-placement="bottom" title="A much longer tooltip to demonstrate the max-width of the Bootstrap tooltip." ><img src="/static/img/tooltip.png" width="25px" /> </span></span>')
    My_keyword_density.admin_order_field   = 'keyword_density'

    def My_h1_tag(self, instance):
        return str(instance.h1_tag)+'%'
    My_h1_tag.short_description = 'H1 tag Density'

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

    def My_url_title(self, instance):
        return str(instance.url_title)+'%'
    My_url_title.short_description = 'Meta Title Density'

    def My_all_title(self, instance):
        return str(instance.all_title)+'%'
    My_all_title.short_description = 'All Header Density'

    def My_bodytext(self, instance):
        return str(instance.bodytext)+'%'
    My_bodytext.short_description = 'Body Text Density'
    
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