from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    url(r'^api/topmenu/$', views.topmenu, name="topmenu"),
    #url(r'^api/mainmenu/([a-zA-Z0-9_.-]+)/$', views.mainmenu, name="mainmenu"),
    url(r'^api/mainmenu/$', views.mainmenu, name="mainmenu"),
    url(r'^api/footermenu/$', views.footermenu, name="footermenu"),
    url(r'^api/checklp/$', views.checklp, name="checklp"),
    url(r'^api/getnewsbycat/$', views.getnewsbycat, name="getnewsbycat"),
    url(r'^api/newslist/$', views.newslist, name="newslist"),
    url(r'^api/listvideo/$', views.listvideo, name="listvideo"),
    url(r'^api/catdata/$', views.catdata, name="catdata"),
    url(r'^api/newsdata/$', views.newsdata, name="newsdata"),
    url(r'^api/newsvideo/$', views.newsvideo, name="newsvideo"),
]
