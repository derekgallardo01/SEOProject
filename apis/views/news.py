# Create your views here.
from django.shortcuts import render
#from .models import Categories
from categories.models import Category
from news.models import News, NewsAssoc, NewsImages
from videos.models import Videos, VideoAssoc
from images.models import Images
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import http.client, urllib.request, urllib.parse, urllib.error, base64
from django.db.models import CharField, Value as V
from django.db.models import OuterRef, Subquery, Prefetch
from django.db.models.functions import Concat
from django.db import connection
from datetime import datetime
from django.db.models import Q
import numpy as np
from functools import reduce
import operator
from django.core import serializers 
from django.db.models import Q
import json

user_pk = 1
category_pk = 1  #some times None

'''f = Q( user__pk = user_pk, date=now() )
if category_pk is not None:
  f &= Q( category__pk = category_pk )

todays_items = Item.objects.filter( f  )


qs = Users.objects.filter(
                    p_id=parent_id,
                    status=True
                ).all()

if user_id>0:
    qs = qs.filter( ~Q(id=user_id) )

'''

def Merge(dict1, dict2): 
    return(dict2.update(dict1)) 
      

def dictma(request):
    dict1 = {'a': {'r':10}, 'b': 8} 
    dict2 = {'d': 6, 'c': 4} 
    
    # This return None 
    print(Merge(dict1, dict2)) 
    
    # changes made in dict2 
    print(dict2) 
    return HttpResponse(dict2)

# Create your views here.

def caturl(slug):
    return slug+'/0'


def catdata(request):
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    #casas = Casa.objects.filter(nome_fantasia__contains='green', nome_fantasia__iexact='green')
    
    fielddata = Category.objects.filter(slug = id ).values()
    '''for cdata in fielddata:
        print(cdata)
    json_res = serializers.serialize('json',fielddata)
    return json_res'''
    vdata = []
    
    #return JsonResponse({'catdata':list(fielddata) }, safe=False)
    if(fielddata and fielddata[0]["id"]):
        vimages = Images.objects.filter(type_id = fielddata[0]["id"], type = 'news', status = 'A' )
        vdata = list(vimages)

    return JsonResponse({'catdata':list(fielddata), 'img_data':list(vdata) }, safe=False)
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

def newsdata(request):
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    #casas = Casa.objects.filter(nome_fantasia__contains='green', nome_fantasia__iexact='green')
    vdata = []
    fielddata = News.objects.filter(slug = id ).values()
    if(fielddata and fielddata[0]["id"]):
        vimages = Images.objects.filter(type_id = fielddata[0]["id"], type = 'news', status = 'A' )
        vdata = list(vimages)
    
    return JsonResponse({'newsdata':list(fielddata), 'img_data':vdata }, safe=False)
    

def listvideo(request):
    newsname = request.GET.get('newssearch', '')
    page = request.GET.get('page', 1)
    #return HttpResponse(newsname)

    #newsname = request.GET['newsname']
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    #casas = Casa.objects.filter(nome_fantasia__contains='green', nome_fantasia__iexact='green')
    vdata = {}
    fielddata = Category.objects.filter(slug = id )
    if(fielddata and fielddata[0].id):
        
        dynamiclimit = fielddata[0].excelNumberOfRec_summary.split(',')
        if(len(dynamiclimit)>0):
            nlimit = int(dynamiclimit[0])
        else:
            nlimit = 10
        
        if(len(dynamiclimit)>1):
            vlimit = int(dynamiclimit[1])
        else:
            vlimit = 10
        
        #return HttpResponse(nlimit)
        if(page <= 1):
            noffset = 0
            voffset = 0
        else:
            noffset = (int(page)-1)*nlimit
            voffset = (int(page)-1)*vlimit
        

        vdata = getvideos(fielddata[0], newsname, voffset, vlimit )
    
    return JsonResponse(vdata)


def getvideos(catdata, videosearch, voffset, vlimit):
    fields = []
    searchfields = {}
    if(catdata and catdata.video_tlp_column):
        dynamicdata = vdatavideo_tlp_column.split('||||')
        for ndata in dynamicdata:
            if('video_api_Listing_field' in ndata):
                fields = ndata.replace('video_api_Listing_field','').split(',')
            
            if('video_data_search_field_1' in ndata):
                searchfields = ndata.replace('video_data_search_field_1','').split(',')

    if(len(fields)==0):
        dynamicf_data = Category.objects.filter(catname = 'dynamic_field_video_section')
        dynamicdata = dynamicf_data[0].catdes.split('||||')
        for ndata in dynamicdata:
            if('video_api_Listing_field' in ndata):
                fields = ndata.replace('video_api_Listing_field','').split(',')

            if('video_data_search_field_1' in ndata):
                searchfields = ndata.replace('video_data_search_field_1','').split(',')

    list2 = ['video__' + x.strip() for x in fields]
    list2.insert(0,'cat_id')
    #fields = ['cat__news_name','cat__news_desc']
    #news.id, news_name, news_desc
    #nwdata = News.objects.raw("select %s from news left join news_assoc on news_assoc.cat_id = news.id where news_assoc.assoc_id = 36 ", fields)



    videodata = {}
    if(catdata and catdata.id):
        nwdata = VideoAssoc.objects.filter(cat_id= catdata.id ).select_related('video').values_list(*list2)
        current_date = datetime.today()
        nwdata = nwdata.filter(video__activate__lte=current_date, video__expiry__gte=current_date, video__date_display__gte='1991-01-01')


        if videosearch:
            #nwdata = nwdata.filter(assoc_id= 36)
            q_list = []
            for sfield in searchfields:
                print(sfield)
                filter = 'cat__' +sfield.strip() + '__icontains'
                q_list.append(Q(**{filter:videosearch}))
                #nwdata = nwdata.filter(Q(**{filter:newsname}) | )
            
            #return HttpResponse(q_list)
            #q_list = [Q(cat__news_name__icontains=newsname), Q(cat__news_desc__icontains=newsname)]
            #nwdata = nwdata.filter(reduce(operator.or_, q_list))

        totalrec= len(nwdata)
        nwdata = nwdata.order_by('-video__id')[voffset:voffset+vlimit]

        i = -1
        for bt in nwdata:
            li = 0
            i += 1
            bt2 = {}
            for fld in fields:
                li += 1
                #newsdata[i] = {'newsname':bt.cat.news_name,'catid':bt.assoc_id,'newsdesc':bt.cat.news_desc}
                bt2.update({fld.strip():bt[li]})
            
            vimages = Images.objects.filter(type_id = bt[0], type = 'news', status = 'A' )
            imgdata = {}
            ii = -1
            for idata in vimages:
                ii += 1
                imgdata[ii] = {'name':idata.name, 'top_caption':idata.top_caption, 'bottom_caption':idata.bottom_caption, 'path':idata.path }

            videodata[i] = {'rec':bt2, 'images':imgdata }

        videodata = {'records':totalrec, 'news_data':videodata }
        return videodata



def newsvideo(request):
    newsname = request.GET.get('newssearch', '')
    page = request.GET.get('page', 1)
    #return HttpResponse(newsname)

    #newsname = request.GET['newsname']
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    fielddata = Category.objects.filter(slug = id )

    newsdata = {}
    data = {}
    searchquery = 'where news.status = "A"'
    li = -1
    query = '''select ne_ass.cat_id as cat_id, news.news_name as news_name, news.news_desc as news_desc, news.id as id, news.slug as nslug from news_assoc ne_ass LEFT JOIN news ON news.id=ne_ass.cat_id LEFT JOIN news_read ON news_read.news_id=news.id where news.status = "A" and news.column_scroller = 'A'  GROUP BY news.id order by news.date_display desc, news.ord desc limit 10'''
    cursor  = connection.cursor()
    cursor.execute(query)
    data['results'] = cursor.fetchall()
    return JsonResponse(data)

    for p in NewsAssoc.objects.raw(query):
        li += 1
        newsdata[li] = {'ndata':p}

    return JsonResponse(newsdata)

def newslist(request):
    #cursor = connection.cursor()
    
    newsname = request.GET.get('newssearch', '')
    page = request.GET.get('page', 1)
    #return HttpResponse(newsname)

    #newsname = request.GET['newsname']
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    #casas = Casa.objects.filter(nome_fantasia__contains='green', nome_fantasia__iexact='green')
    
    fielddata = Category.objects.filter(slug = id )

    fields = []
    searchfields = []
    if(fielddata and fielddata[0].news_tlp_column):
        dynamicdata = fielddata[0].news_tlp_column.split('||||')
        for ndata in dynamicdata:
            if('news_api_Listing_field' in ndata):
                fields = ndata.replace('news_api_Listing_field','').split(',')
            
            if('news_data_search_field_1' in ndata):
                searchfields = ndata.replace('news_data_search_field_1','').split(',')

    if(len(fields)==0):
        dynamicf_data = Category.objects.filter(catname = 'dynamic_field_news_section')
        dynamicdata = dynamicf_data[0].catdes.split('||||')
        for ndata in dynamicdata:
            if('news_api_Listing_field' in ndata):
                fields = ndata.replace('news_api_Listing_field','').split(',')

            if('news_data_search_field_1' in ndata):
                searchfields = ndata.replace('news_data_search_field_1','').split(',')

    list2 = ['cat__' + x.strip() for x in fields]
    list2.insert(0,'assoc_id')
    #fields = ['cat__news_name','cat__news_desc']
    #news.id, news_name, news_desc
    #nwdata = News.objects.raw("select %s from news left join news_assoc on news_assoc.cat_id = news.id where news_assoc.assoc_id = 36 ", fields)

    newsdata = {}


    if(fielddata and fielddata[0].id):
        
        dynamiclimit = fielddata[0].excelNumberOfRec_summary.split(',')
        if(len(dynamiclimit)>0):
            nlimit = int(dynamiclimit[0])
        else:
            nlimit = 10
        
        if(len(dynamiclimit)>1):
            vlimit = int(dynamiclimit[1])
        else:
            vlimit = 10
        
        #return HttpResponse(nlimit)
        if( int(page) <= int(1) ):
            noffset = 0
            voffset = 0
        else:
            noffset = (int(page)-1)*nlimit
            voffset = (int(page)-1)*vlimit
        

        #vdata = getvideos(fielddata[0], newsname, voffset, vlimit )

        nwdata = NewsAssoc.objects.filter(assoc_id= fielddata[0].id ).select_related('cat').values_list(*list2)
        #nwdata = NewsAssoc.objects.all().prefetch_related(Prefetch('cat', queryset=News.objects.order_by('-id')[:10]))
        #return HttpResponse(nwdata)
        current_date = datetime.today()
        nwdata = nwdata.filter(cat__activate__lte=current_date, cat__expiry__gte=current_date, cat__date_display__gte='1991-01-01')
        #nwdata = nwdata.filter()

        #.prefetch_related(
        #Prefetch('msg_sent', queryset=UserMsg.objects.order_by('-created')[:10]))


        if newsname:
            #nwdata = nwdata.filter(assoc_id= 36)
            q_list = []
            for sfield in searchfields:
                print(sfield)
                filter = 'cat__' +sfield.strip() + '__icontains'
                q_list.append(Q(**{filter:newsname}))
                #nwdata = nwdata.filter(Q(**{filter:newsname}) | ) 
            
            #q_list = [Q(cat__news_name__icontains=newsname), Q(cat__news_desc__icontains=newsname)]
            nwdata = nwdata.filter(reduce(operator.or_, q_list))
            #nwdata = nwdata.filter(Q(cat__news_name__icontains=newsname) | Q(cat__news_desc__icontains=newsname) | Q(cat__source__icontains=newsname) | Q(cat__title__icontains=newsname) | Q(cat__meta__icontains=newsname) | Q(cat__keyword__icontains=newsname) )

        totalrec= len(nwdata)
        
        #nwdata1 = News.objects.filter(pk__in = nwdata)[10:2]
        
        #(noffset+nlimit)
        nwdata = nwdata.order_by('-cat__id')[noffset:noffset+nlimit]

        i = -1
        for bt in nwdata:
            li = 0
            i += 1
            bt2 = {}
            for fld in fields:
                li += 1
                #newsdata[i] = {'newsname':bt.cat.news_name,'catid':bt.assoc_id,'newsdesc':bt.cat.news_desc}
                bt2.update({fld.strip():bt[li]})
            
            newsimages = ''
            #newsimages = NewsImages.objects.filter(type_id = bt[0], type = 'news', status = 'A' )
            newsimages = NewsImages.objects.filter(type_id = bt[0], type = 'news', status = 'A' )
            imgdata = {}
            ii = -1
            for idata in newsimages:
                ii += 1
                imgdata[ii] = {'name':idata.name, 'top_caption':idata.top_caption, 'bottom_caption':idata.bottom_caption, 'path':idata.path }

            #,'images':newsimages
            newsdata[9999+i] = {'rec':bt2, 'images':imgdata }

    '''if(len(vdata)>0):
        totalrec = totalrec+int(vdata["records"])'''

    #vdata["news_data"] = {'f':'s'}

    #newsdata = vdata["news_data"].update(newsdata)
    #newsdata = vdata["news_data"]
    return JsonResponse(newsdata)
    #newsdata = {'records':totalrec, 'news_data':newsdata }
    newsdata = {'records':totalrec, 'news_data':newsdata }
    #return JsonResponse(vdata)
    return JsonResponse(newsdata)
    #print(nwdata.query)
    #dictat = dict(nwdata)
    #return JsonResponse(dictat)
    
    user = User.objects.get(pk=1)
    #category = Category.objects.get(pk=1)
    #qs = Item.objects.filter(user=user, date=now())


def getnewsbycat(request):

    #fields = ['news_name', 'news_desc']
    
    newsname = request.GET['newsname']
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']

    fielddata = Category.objects.filter(slug = id )

    fields = "news_name, news_desc"
    
    #print(list(fielddata[0].field1))
    #return 'yy'
    #.all().order_by('id')
    #print(fielddata[0].field1.split(','))
    news_data = {}

    total_news = News.objects.filter(member_id = 5 ).all().count()
    news_data['count'] = total_news
    news_data['records'] = {}

    #if():
    #_categories__slug = 'hariyana'
    
    search = ""
    if(newsname):
        search = "news_name like %s% ",newsname
        

    
    # where news_assoc.assoc_id = 36
    #nwdata = News.objects.filter(news_assoc__assoc_id = 36 )#.values(*fields)
    nwdata = News.objects.raw("select news.id, news_name, news_desc from news left join news_assoc on news_assoc.cat_id = news.id ")
    

    '''for newsrec in nwdata:
        return HttpResponse(newsrec)'''
    

    #nwdata = News.objects.filter(member_id = 5 ).values(*fields)
    
    li = -1
    for newsrec in nwdata:
        li+=1
        print(newsrec.news_name)
        #news_data['records'][li] = newsrec["news_name"]
        news_data['records'][li] = dict(newsrec)
        return HttpResponse(news_data['records'][li])

    return HttpResponse(news_data)
    return JsonResponse(news_data)



def checklpnews(request):
    x = 5
    y = 5
    z = {}
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    if(id!=""):
        users = Exceluser.objects.filter(slug = id ).all().order_by('id')
        
        if(users[0].id):
            #users = Exceluser.objects.filter(slug = id ).all().order_by('id')
            idsdata = Category.objects.filter(excelid = users[0].id ).all().order_by('id')
            #idsdata = Category.objects.annotate(personid=Concat('personid', V(' ('), 'goes_by', V(')'), output_field=CharField() ) ).get() 
            usercar = []
            for it in idsdata:
                usercar.append(it.id)
            
            return HttpResponse(usercar)

    print(code)
    if(isinstance(z,dict)):
        print('ddddd')
    finallist=[[0 for row in range(0,x)] for col in range(0,y)]
    return HttpResponse(finallist)