from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    #URls of seo_keyword file
    #url(r'^admin/my_special_link_in_admin/$', views.special_admin_page),
    url(r'^keywordreport/no-conversion/$', views.noconv, name="no-conversion"),
    url(r'^keywordreport/bad-to-ok/$', views.badtook, name="badtook"),
    url(r'^keywordreport/converted-found/$', views.convertedfound, name="convertedfound"),
    
    
    #url(r'^api/mainmenu/([a-zA-Z0-9_.-]+)/$', views.mainmenu, name="mainmenu"),
    #url(r'^api/noconvert/$', views.noconvert, name="noconvert"),
    #Google Trend report
    url(r'^google/trends/$', views.trends, name="trends"),
    url(r'^google/spread-sheet/$', views.gspreadsheet, name="gspreadsheet"),
    url(r'^google/related-query/$', views.relatedquery, name="relatedquery"),
    url(r'^google/keyword-rising/$', views.keywordrising, name="keywordrising"),
    url(r'^google/suggestions-keyword/$', views.suggestionskeyword, name="suggestionskeyword"),
    url(r'^google/write_data_in_googlesheet/$', views.write_data_in_googlesheet, name="write_data_in_googlesheet"),

    #Google Adwords API
    url(r'^google/googleads_report/$', views.googleads_report, name="googleads_report"),
    url(r'^google/ads-api-report2/$', views.googleads_report2, name="googleads_report2"),
    url(r'^google/googleads_tiwari/$', views.googleads_tiwari, name="googleads_tiwari"),
    url(r'^google/adwords_plan/$', views.adwords_plan, name="adwords_plan"),
    
    url(r'^google/rising-from-file/$', views.risingfromfile, name="risingfromfile"),
    url(r'^google/track-keywords/$', views.trackkeywords, name="trackkeywords"),


    # only to allow building dynamically
    url(r'^field_choices/(?P<model>.+)/(?P<field_name>.+)/?', views.suggestionskeyword, name='afilters_get_field_choices'),
    url(r'^field_choices/$', views.suggestionskeyword, name='afilters_get_field_choices'),


]


#http://127.0.0.1:8000/google/track-keywords/
#http://127.0.0.1:8000/google/keyword-rising/