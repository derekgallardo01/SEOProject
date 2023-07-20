from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    url(r'^keywordreport/no-conversion/$', views.noconv, name="no-conversion"),
    url(r'^keywordreport/bad-to-ok/$', views.badtook, name="badtook"),
    url(r'^keywordreport/converted-found/$', views.convertedfound, name="convertedfound"),
    url(r'^google/trends/$', views.trends, name="trends"),
    url(r'^google/track-keywords/$', views.trackkeywords, name="trackkeywords"),
    #url(r'^api/mainmenu/([a-zA-Z0-9_.-]+)/$', views.mainmenu, name="mainmenu"),
    #url(r'^api/noconvert/$', views.noconvert, name="noconvert"),
    url(r'^google/spread-sheet/$', views.gspreadsheet, name="gspreadsheet"),
    url(r'^google/keyword-rising/$', views.keywordrising, name="keywordrising"),
    url(r'^google/ads-api-report2/$', views.googleads_report2, name="googleads_report2"),
    url(r'^google/write_data_in_googlesheet/$', views.write_data_in_googlesheet, name="write_data_in_googlesheet"),
    url(r'^google/rising-from-file/$', views.risingfromfile, name="risingfromfile"),
    url(r'^google/related-query/$', views.relatedquery, name="relatedquery"),
    
    url(r'^google/suggestions-keyword/$', views.suggestionskeyword, name="suggestionskeyword"),
]
