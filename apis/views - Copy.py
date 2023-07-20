# Create your views here.
from django.shortcuts import render
#from .models import Categories
from categories.models import Category
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
# Create your views here.

def caturl(slug):
    return slug+'/0'


def checklp(request):
    x = 5
    y = 5
    finallist=[[0 for row in range(0,x)] for col in range(0,y)]
    return HttpResponse(finallist)


def topmenu(request):
    code = request.POST.get('code', False)
    id = request.POST.get('id', False)
    tab = request.POST.get('tab', False)
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

    finallist = []
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

            
            itemlist = {"link":link,"catname":item1[0].catname}
            #finallist.append({i:itemlist})
            #print( item1[0].top_mega_menu_column )
            if(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) > 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    for cid in datacol1:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'1':itemlist}}})

                if(item1[0].topmenu_mega_col2):
                    datacol2 = item1[0].topmenu_mega_col2.split(',')
                    for cid in datacol2:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'2':itemlist}}})

                if(item1[0].topmenu_mega_col3):
                    datacol3 = item1[0].topmenu_mega_col3.split(',')
                    for cid in datacol3:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'3':itemlist}}})

                if(item1[0].topmenu_mega_col4):
                    datacol4 = item1[0].topmenu_mega_col2.split(',')
                    for cid in datacol4:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'4':itemlist}}})

                if(item1[0].topmenu_mega_col5):
                    datacol5 = item1[0].topmenu_mega_col5.split(',')
                    for cid in datacol5:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'5':itemlist}}})
                
                if(item1[0].topmenu_mega_col6):
                    datacol6 = item1[0].topmenu_mega_col2.split(',')
                    for cid in datacol6:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'6':itemlist}}})

            elif(item1[0].top_mega_menu_column and int(item1[0].top_mega_menu_column) == 1):
                if(item1[0].topmenu_mega_col1):
                    datacol1 = item1[0].topmenu_mega_col1.split(',')
                    for cid in datacol1:
                        #print(cid.strip())
                        if((cid.strip()) and int(cid.strip()) > 0 ):
                            item1 = Category.objects.filter(id = cid ).all().order_by('id')
                            if(item1[0].link):
                                link = item1[0].link
                            else:
                                link = item1[0].link2
                            
                            if(link):
                                pass
                            else:
                                link = caturl(item1[0].slug)

                            itemlist = {"link":link,"catname":item1[0].catname}
                            finallist.append({i:{'sub':{'1':itemlist}}})   

    print(finallist)
    #return HttpResponse(finallist)    
    return JsonResponse(finallist, safe=False)    

