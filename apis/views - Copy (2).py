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


def topmenu(request):
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']

    if(code=='cat' or code=='news_detail'):
        if(code=='news_detail'):
            rssite = Category.objects.filter(slug = id ).all().order_by('id')
        else:
            rssite = Category.objects.filter(id = tab ).all().order_by('id')
        
        rssitede = Category.objects.filter(id = rssite[0].id ).all().order_by('id')
        rssitedetail = rssitede[0].top_menu_ids.split(',')
        
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
    #print(rssitedetail)
    for cid in rssitedetail:
        i += 1
        cid = int(cid)
        if(cid > 0 ):
            item1 = Category.objects.filter(id = cid ).all().order_by('id')
            if(item1[0].link):
                link = item1[0].link
            else:
                link = item1[0].link2
            
            if(link):
                pass
            else:
                link = caturl(item1[0].slug)

            
            mainitemlist = {"link":link,"catname":item1[0].catname}
            
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
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item11 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item11[0].link):
                                link = item11[0].link
                            else:
                                link = item11[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item11[0].slug)

                            itemlist = {"link":link,"catname":item11[0].catname}
                            
                            finallist1["sub"][fl] = itemlist
                            #finallist.update({i:{'sub':{'1':itemlist}}})

                if(item1[0].topmenu_mega_col2):
                    datacol2 = item1[0].topmenu_mega_col2.split(',')
                    finallist2["sub"] = {}
                    fl = -1
                    for cid in datacol2:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item12 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item12[0].link):
                                link = item12[0].link
                            else:
                                link = item12[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item12[0].slug)

                            itemlist = {"link":link,"catname":item12[0].catname}
                            finallist2["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col3):
                    datacol3 = item1[0].topmenu_mega_col3.split(',')
                    finallist3["sub"] = {}
                    fl = -1
                    for cid in datacol3:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item13 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item13[0].link):
                                link = item13[0].link
                            else:
                                link = item13[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item13[0].slug)

                            itemlist = {"link":link,"catname":item13[0].catname}
                            finallist3["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col4):
                    datacol4 = item1[0].topmenu_mega_col2.split(',')
                    finallist4["sub"] = {}
                    fl = -1
                    for cid in datacol4:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item14 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item14[0].link):
                                link = item14[0].link
                            else:
                                link = item14[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item14[0].slug)

                            itemlist = {"link":link,"catname":item14[0].catname}
                            finallist4["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col5):
                    datacol5 = item1[0].topmenu_mega_col5.split(',')
                    finallist5["sub"] = {}
                    fl = -1
                    for cid in datacol5:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item15 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item15[0].link):
                                link = item15[0].link
                            else:
                                link = item15[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item15[0].slug)

                            itemlist = {"link":link,"catname":item15[0].catname}
                            finallist5["sub"][fl] = itemlist
                
                if(item1[0].topmenu_mega_col6):
                    datacol6 = item1[0].topmenu_mega_col2.split(',')
                    finallist6["sub"] = {}
                    fl = -1
                    for cid in datacol6:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()>0) and int(cid.strip()) > 0 ):
                            item16 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item16[0].link):
                                link = item16[0].link
                            else:
                                link = item16[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item16[0].slug)

                            itemlist = {"link":link,"catname":item16[0].catname}
                            finallist6["sub"][fl] = itemlist

            elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    finallist1["sub"] = {}
                    fl = -1
                    for cid in datacol1:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item11 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item11[0].link):
                                link = item11[0].link
                            else:
                                link = item11[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item11[0].slug)

                            itemlist = {"link":link,"catname":item11[0].catname}
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
    if(id!=False):
        users = Exceluser.objects.filter(slug = id ).all().order_by('id')
        
        if(users and users[0].id):
            rssitedetail = getuserids(users[0].id)
  
  
    if(not rssitedetail):
        if(code=='cat' or code=='news_detail'):
            if(code=='news_detail'):
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
            if(item1[0].link):
                link = item1[0].link
            else:
                link = item1[0].link2
            
            if(link):
                pass
            else:
                link = caturl(item1[0].slug)

            
            mainitemlist = {"link":link,"catname":item1[0].catname}
            
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
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item11 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item11[0].link):
                                link = item11[0].link
                            else:
                                link = item11[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item11[0].slug)

                            itemlist = {"link":link,"catname":item11[0].catname}
                            
                            finallist1["sub"][fl] = itemlist
                            #finallist.update({i:{'sub':{'1':itemlist}}})

                if(item1[0].topmenu_mega_col2):
                    datacol2 = item1[0].topmenu_mega_col2.split(',')
                    finallist2["sub"] = {}
                    fl = -1
                    for cid in datacol2:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item12 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item12[0].link):
                                link = item12[0].link
                            else:
                                link = item12[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item12[0].slug)

                            itemlist = {"link":link,"catname":item12[0].catname}
                            finallist2["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col3):
                    datacol3 = item1[0].topmenu_mega_col3.split(',')
                    finallist3["sub"] = {}
                    fl = -1
                    for cid in datacol3:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item13 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item13[0].link):
                                link = item13[0].link
                            else:
                                link = item13[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item13[0].slug)

                            itemlist = {"link":link,"catname":item13[0].catname}
                            finallist3["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col4):
                    datacol4 = item1[0].topmenu_mega_col2.split(',')
                    finallist4["sub"] = {}
                    fl = -1
                    for cid in datacol4:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item14 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item14[0].link):
                                link = item14[0].link
                            else:
                                link = item14[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item14[0].slug)

                            itemlist = {"link":link,"catname":item14[0].catname}
                            finallist4["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col5):
                    datacol5 = item1[0].topmenu_mega_col5.split(',')
                    finallist5["sub"] = {}
                    fl = -1
                    for cid in datacol5:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item15 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item15[0].link):
                                link = item15[0].link
                            else:
                                link = item15[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item15[0].slug)

                            itemlist = {"link":link,"catname":item15[0].catname}
                            finallist5["sub"][fl] = itemlist
                
                if(item1[0].topmenu_mega_col6):
                    datacol6 = item1[0].topmenu_mega_col2.split(',')
                    finallist6["sub"] = {}
                    fl = -1
                    for cid in datacol6:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()>0) and int(cid.strip()) > 0 ):
                            item16 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item16[0].link):
                                link = item16[0].link
                            else:
                                link = item16[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item16[0].slug)

                            itemlist = {"link":link,"catname":item16[0].catname}
                            finallist6["sub"][fl] = itemlist

            elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    finallist1["sub"] = {}
                    fl = -1
                    for cid in datacol1:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item11 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item11[0].link):
                                link = item11[0].link
                            else:
                                link = item11[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item11[0].slug)

                            itemlist = {"link":link,"catname":item11[0].catname}
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



def footermenu(request):
    #code = request.POST.get('code')
    #id = request.POST.get('id')
    #tab = request.POST.get('tab')
    code = request.GET['code']
    id = request.GET['id']
    tab = request.GET['tab']
    
    rssitedetail = []
    if(id!=False):
        users = Exceluser.objects.filter(slug = id ).all().order_by('id')
        
        if(users and users[0].id):
            rssitedetail = getuserids(users[0].id)
  
  
    if(not rssitedetail):
        if(code=='cat' or code=='news_detail'):
            if(code=='news_detail'):
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
            if(item1[0].link):
                link = item1[0].link
            else:
                link = item1[0].link2
            
            if(link):
                pass
            else:
                link = caturl(item1[0].slug)

            
            mainitemlist = {"link":link,"catname":item1[0].catname}
            
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
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item11 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item11[0].link):
                                link = item11[0].link
                            else:
                                link = item11[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item11[0].slug)

                            itemlist = {"link":link,"catname":item11[0].catname}
                            
                            finallist1["sub"][fl] = itemlist
                            #finallist.update({i:{'sub':{'1':itemlist}}})

                if(item1[0].topmenu_mega_col2):
                    datacol2 = item1[0].topmenu_mega_col2.split(',')
                    finallist2["sub"] = {}
                    fl = -1
                    for cid in datacol2:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item12 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item12[0].link):
                                link = item12[0].link
                            else:
                                link = item12[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item12[0].slug)

                            itemlist = {"link":link,"catname":item12[0].catname}
                            finallist2["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col3):
                    datacol3 = item1[0].topmenu_mega_col3.split(',')
                    finallist3["sub"] = {}
                    fl = -1
                    for cid in datacol3:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item13 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item13[0].link):
                                link = item13[0].link
                            else:
                                link = item13[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item13[0].slug)

                            itemlist = {"link":link,"catname":item13[0].catname}
                            finallist3["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col4):
                    datacol4 = item1[0].topmenu_mega_col2.split(',')
                    finallist4["sub"] = {}
                    fl = -1
                    for cid in datacol4:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item14 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item14[0].link):
                                link = item14[0].link
                            else:
                                link = item14[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item14[0].slug)

                            itemlist = {"link":link,"catname":item14[0].catname}
                            finallist4["sub"][fl] = itemlist

                if(item1[0].topmenu_mega_col5):
                    datacol5 = item1[0].topmenu_mega_col5.split(',')
                    finallist5["sub"] = {}
                    fl = -1
                    for cid in datacol5:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item15 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item15[0].link):
                                link = item15[0].link
                            else:
                                link = item15[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item15[0].slug)

                            itemlist = {"link":link,"catname":item15[0].catname}
                            finallist5["sub"][fl] = itemlist
                
                if(item1[0].topmenu_mega_col6):
                    datacol6 = item1[0].topmenu_mega_col2.split(',')
                    finallist6["sub"] = {}
                    fl = -1
                    for cid in datacol6:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()>0) and int(cid.strip()) > 0 ):
                            item16 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item16[0].link):
                                link = item16[0].link
                            else:
                                link = item16[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item16[0].slug)

                            itemlist = {"link":link,"catname":item16[0].catname}
                            finallist6["sub"][fl] = itemlist

            elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    finallist1["sub"] = {}
                    fl = -1
                    for cid in datacol1:
                        fl +=1
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item11 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item11[0].link):
                                link = item11[0].link
                            else:
                                link = item11[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item11[0].slug)

                            itemlist = {"link":link,"catname":item11[0].catname}
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

