# Create your views here.
from django.shortcuts import render
#from .models import Categories
from categories.models import Category
from exceluser.models import Exceluser
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import http.client, urllib.request, urllib.parse, urllib.error, base64
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat

import numpy as np


# Create your views here.

def caturl(slug):
    return slug+'/0'


def checklp(request):
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

def getdataitem(item11):
    if(item11[0].link):
        link = item11[0].link
    else:
        link = item11[0].link2
    
    if(link):
        pass
    else:
        link = caturl(item11[0].slug)

    return {"link":link,"catname":item11[0].catname,"display_name":item11[0].display_name}

def getitemlist(cid):
    if((cid.strip()) and int(cid.strip()) > 0 ):
        item11 = Category.objects.filter(id = cid ).all().order_by('id')
        itemlist = getdataitem(item11)
        return itemlist


def topmenu(request):
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']

    if(code=='cat' or code=='news_detail'):
        if(code=='news_detail' and tab):
            rssite = Category.objects.filter(id = int(tab.strip()) ).all().order_by('id')
        else:
            rssite = Category.objects.filter(slug = id ).all().order_by('id')
        
        
        if(rssite and rssite[0].top_menu_ids!=''):
            rssitedetail = rssitede[0].top_menu_ids.split(',')
        else:
            menu3 = Category.objects.filter(catname = 'top_menu_ids').all().order_by('id')
            rssitedetail = menu3[0].catdes.split(',')
        
    else:
        menu = Category.objects.filter(catname = 'site_index_page_id').all().order_by('id')
        #print(menu[0].catdes)
        if(menu[0].catdes):
            menu1 = Category.objects.filter(id = menu[0].catdes ).all().order_by('id')
            #print(menu1[0].top_menu_ids)
            if(menu1[0].top_menu_ids):
                rssitedetail = menu1[0].top_menu_ids.split(',')
            else:
                menu2 = Category.objects.filter(catname = 'top_menu_ids').all().order_by('id')
                rssitedetail = menu2[0].catdes.split(',')
        else:
            menu3 = Category.objects.filter(catname = 'top_menu_ids').all().order_by('id')
            rssitedetail = menu3[0].catdes.split(',')

    finallist = {}
    finalmainitemlist = {}
    i=0
    print(rssitedetail)
    for cid in rssitedetail:
        i += 1
        if(cid!='' and int(cid) > 0 ):
            item1 = Category.objects.filter(id = int(cid) ).all().order_by('id')
            mainitemlist = getdataitem(item1)
            #finallist[i] = itemlist

            finallist1 = {}
            finallist2 = {}
            finallist3 = {}
            finallist4 = {}
            finallist5 = {}
            finallist6 = {}

            #print( item1[0].top_mega_menu_column )
            if(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) > 1):
                if(item1[0].topmenu_mega_col1):
                    
                    finallist1["sub"] = {}
                    fl = -1
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    for cid in datacol1:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist1["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col2):
                    datacol2 = item1[0].topmenu_mega_col2.split(',')
                    finallist2["sub"] = {}
                    fl = -1
                    for cid in datacol2:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist2["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col3):
                    datacol3 = item1[0].topmenu_mega_col3.split(',')
                    finallist3["sub"] = {}
                    fl = -1
                    for cid in datacol3:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist3["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col4):
                    datacol4 = item1[0].topmenu_mega_col2.split(',')
                    finallist4["sub"] = {}
                    fl = -1
                    for cid in datacol4:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist4["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col5):
                    datacol5 = item1[0].topmenu_mega_col5.split(',')
                    finallist5["sub"] = {}
                    fl = -1
                    for cid in datacol5:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist5["sub"][fl] = itemlist
                
                if(item1[0].topmenu_mega_col6):
                    datacol6 = item1[0].topmenu_mega_col2.split(',')
                    finallist6["sub"] = {}
                    fl = -1
                    for cid in datacol6:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist6["sub"][fl] = itemlist

            elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    finallist1["sub"] = {}
                    fl = -1
                    for cid in datacol1:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist1["sub"][fl] = itemlist   

            if(mainitemlist):
                #finalmainitemlist[i]["sub"] = {}
                #finalmainitemlist[i][]
                #finalmainitemlist[i] = {i:mainitemlist,'sub':{1:finallist1, 2:finallist2, 3:finallist3, 4:finallist4, 5:finallist5, 6:finallist6}}
                finalmainitemlist[i] = mainitemlist
                if(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) > 1):
                    finalmainitemlist[i].update({'sub':{1:finallist1, 2:finallist2, 3:finallist3, 4:finallist4, 5:finallist5, 6:finallist6}})
                elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                    finalmainitemlist[i].update({'sub':{1:finallist1}})
                #finalmainitemlist[i]["sub"] = {1:finallist1, 2:finallist2, 3:finallist3, 4:finallist4, 5:finallist5, 6:finallist6}
    
    return JsonResponse(finalmainitemlist, safe=False)    

def getuserids(excelid):
    rssitedetail = []
    idsdata = Category.objects.filter(excelid = excelid ).all().order_by('id')
    for it in idsdata:
            rssitedetail.append(it.id)

    return rssitedetail

def mainmenu(request):
    #code = request.POST.get('code')
    #id = request.POST.get('id')
    #tab = request.POST.get('tab')
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    
    rssitedetail = []
    if(code=='profile' and id!=False):
        users = Exceluser.objects.filter(slug = id ).all().order_by('id')
        
        if(users and users[0].id):
            rssitedetail = getuserids(users[0].id)
  
  
    if(not rssitedetail):
        if(code=='cat' or code=='news_detail'):
            if(code=='news_detail' and tab.isnumeric() ):
                rssite = Category.objects.filter(id = int(tab) ).all().order_by('id')
                if(rssite and rssite[0].excelid):
                    rssitedetail = getuserids(rssite[0].excelid)
                else:
                    rssite = Category.objects.filter(slug = id ).all().order_by('id')
            else:
                #rssite = Category.objects.filter(id = tab ).all().order_by('id')
                rssite = Category.objects.filter(slug = id ).all().order_by('id')
                if(rssite and rssite[0].excelid):
                    rssitedetail = getuserids(rssite[0].excelid)
                elif(rssite and rssite[0].main_menu_ids):
                    rssitedetail = rssite[0].main_menu_ids.split(',')
                else:
                    menu3 = Category.objects.filter(catname = 'main_menu_ids').all().order_by('id')
                    rssitedetail = menu3[0].catdes.split(',')
            
        else:
            menu = Category.objects.filter(catname = 'site_index_page_id').all().order_by('id')
            #print(menu[0].catdes)
            if(menu[0].catdes):
                menu1 = Category.objects.filter(id = menu[0].catdes ).all().order_by('id')
                #print(menu1[0].top_menu_ids)
                if(menu1[0].top_menu_ids):
                    rssitedetail = menu1[0].top_menu_ids.split(',')
                else:
                    menu2 = Category.objects.filter(catname = 'main_menu_ids').all().order_by('id')
                    rssitedetail = menu2[0].catdes.split(',')
            else:
                menu3 = Category.objects.filter(catname = 'main_menu_ids').all().order_by('id')
                rssitedetail = menu3[0].catdes.split(',')

    finallist = {}
    finalmainitemlist = {}
    i=0
    print(rssitedetail)
    for cid in rssitedetail:
        i += 1
        cid = int(cid)
        if(cid > 0 ):
            item1 = Category.objects.filter(id = cid ).all().order_by('id')
            mainitemlist  = getdataitem(item1)
            
            #finallist[i] = itemlist

            finallist1 = {}
            finallist2 = {}
            finallist3 = {}
            finallist4 = {}
            finallist5 = {}
            finallist6 = {}

            #print( item1[0].top_mega_menu_column )
            if(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) > 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    finallist1["sub"] = {}
                    fl = -1
                    for cid in datacol1:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist1["sub"][fl] = itemlist
                            #finallist.update({i:{'sub':{'1':itemlist}}})

                if(item1[0].topmenu_mega_col2):
                    datacol2 = item1[0].topmenu_mega_col2.split(',')
                    finallist2["sub"] = {}
                    fl = -1
                    for cid in datacol2:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist2["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col3):
                    datacol3 = item1[0].topmenu_mega_col3.split(',')
                    finallist3["sub"] = {}
                    fl = -1
                    for cid in datacol3:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist3["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col4):
                    datacol4 = item1[0].topmenu_mega_col2.split(',')
                    finallist4["sub"] = {}
                    fl = -1
                    for cid in datacol4:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist4["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col5):
                    datacol5 = item1[0].topmenu_mega_col5.split(',')
                    finallist5["sub"] = {}
                    fl = -1
                    for cid in datacol5:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist5["sub"][fl] = itemlist
                
                if(item1[0].topmenu_mega_col6):
                    datacol6 = item1[0].topmenu_mega_col2.split(',')
                    finallist6["sub"] = {}
                    fl = -1
                    for cid in datacol6:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist6["sub"][fl] = itemlist

            elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    finallist1["sub"] = {}
                    fl = -1
                    for cid in datacol1:
                        fl +=1
                        itemlist = getitemlist(cid)
                        finallist1["sub"][fl] = itemlist   

            if(mainitemlist):
                #finalmainitemlist[i]["sub"] = {}
                #finalmainitemlist[i][]
                #finalmainitemlist[i] = {i:mainitemlist,'sub':{1:finallist1, 2:finallist2, 3:finallist3, 4:finallist4, 5:finallist5, 6:finallist6}}
                finalmainitemlist[i] = mainitemlist
                if(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) > 1):
                    finalmainitemlist[i].update({'sub':{1:finallist1, 2:finallist2, 3:finallist3, 4:finallist4, 5:finallist5, 6:finallist6}})
                elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                    finalmainitemlist[i].update({'sub':{1:finallist1}})
                #finalmainitemlist[i]["sub"] = {1:finallist1, 2:finallist2, 3:finallist3, 4:finallist4, 5:finallist5, 6:finallist6}
    
    return JsonResponse(finalmainitemlist, safe=False)    



def makechunk(firstpart, listdataidwise, chunk):
    chunk_size = 4
    del firstpart[0:2]
    #chunked_data = [[k, v] for k, v in listdataidwise['toppart'].items()]
    if(chunk=='yes'):
        chunked_data = np.array_split(listdataidwise, chunk_size)
        list1 = list(chunked_data[0])
        list2 = list(chunked_data[1])
        list3 = list(chunked_data[2])
        list4 = list(chunked_data[3])
        
        fi = 0
        for cids in firstpart:
            add = cids.strip().split(',')
            for cid in add:
                fi +=1
                if(fi==1):
                    list1.append(getitemlist(cid))
                
                if(fi==2):
                    list2.append(getitemlist(cid))

                if(fi==3):
                    list3.append(getitemlist(cid))

                if(fi==4):
                    list4.append(getitemlist(cid))
        return {'1':list1, '2':list2, '3':list3, '4':list4 }
    else:
        for cids in firstpart:
            add = cids.strip().split(',')
            for cid in add:
                listdataidwise.append(getitemlist(cid))
            
        return {'1':listdataidwise }

    


def getdatabyobj(footersite, listdataidwise):
    
    li = -1
    for fid in footersite:
        li += 1
        if(fid.link):
            link = fid.link
        else:
            link = fid.link2
        
        if(link):
            pass
        else:
            link = caturl(fid.slug)
        listdataidwise.append({"id":fid.id,"link":link,"catname":fid.catname,"display_name":fid.display_name})

    return listdataidwise


def dataforonepart(dpart, chunk):
    firstpart = dpart.replace('topfootercategoryid:','').split('||||')
    
    listdataidwise = []
    getidwise = firstpart[0].replace('categorytypeid:','').strip()
    if(getidwise):
        listid = list(getidwise.split(','))
        print(listid)
        #return listid
        
        footersite = Category.objects.filter(typeid__in = listid ).all().order_by('id')
        listdataidwise = getdatabyobj(footersite, listdataidwise)
            
    
    getidwise = firstpart[1].replace('categorytype:','').strip()
    if(getidwise):
        listid = list(getidwise.split(','))
        print(listid)
        #return listid
        footersite = Category.objects.filter(typed__in = listid ).all().order_by('id')
        listdataidwise = getdatabyobj(footersite, listdataidwise)
        #listdataidwise['count'] = len(listdataidwise['toppart'])
        if(chunk=='yes'):
            listdataidwise = makechunk(firstpart, listdataidwise,chunk)

    return listdataidwise    


def getfooterdatafromcategory(id):
    rssite = Category.objects.filter(id = int(id) ).all().order_by('id')

    return getfooterdata(rssite[0].footer_menu_ids)

def getfooterdata(data):
    print(data)
    listpartone = []
    listparttwo = []
    rsdata = data.split('bottomfooter:')
    ki = 0
    if(rsdata ):
        print(rsdata)
        for ldata in rsdata:
            if(ldata ):
                ki += 1
                if(ki==1):
                    listpartone = dataforonepart(ldata, 'yes')
                else:
                    listparttwo = dataforonepart(ldata, 'no')
    
    return {'topfooter':listpartone, 'bottomfooter':listparttwo}
    

######################################################### FOOTER MENU #################################################

def footermenu(request):
    #code = request.POST.get('code')
    #id = request.POST.get('id')
    #tab = request.POST.get('tab')
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    footdata = {}

    rssitedetail = []
    if(code=='profile' and id!=False):
        users = Exceluser.objects.filter(slug = id ).all().order_by('id')
        
        if(users and users[0].footercatid):
            footdata = getfooterdatafromcategory(users[0].footercatid)
    
    if(code=='cat' or code=='news_detail'):
        if(code=='news_detail' and tab):
            if(int(tab.strip())):
                profilenews = Category.objects.filter(id = int(tab.strip())).all().order_by('id')
                print(profilenews[0].excelid)
                if(profilenews and profilenews[0].excelid):
                    footdata = getfooterdatafromcategory(tab)
                else:
                    fmenudata = Category.objects.filter(catname = 'footer_menu_ids').all().order_by('id')
                    footdata = getfooterdata(fmenudata[0].catdes)
        else:
            #rssite = Category.objects.filter(id = tab ).all().order_by('id')
            rssite = Category.objects.filter(slug = id ).all().order_by('id')
            if(rssite and rssite[0].excelid):
                footdata = getfooterdata(rssite[0].footer_menu_ids)
            elif(rssite[0].footer_menu_ids):
                footdata = getfooterdata(rssite[0].footer_menu_ids)
            else:
                fmenudata = Category.objects.filter(catname = 'footer_menu_ids').all().order_by('id')
                footdata = getfooterdata(fmenudata[0].catdes)
    else:
        fmenudata = Category.objects.filter(catname = 'footer_menu_ids').all().order_by('id')
        footdata = getfooterdata(fmenudata[0].catdes)

    return JsonResponse(footdata)

    

