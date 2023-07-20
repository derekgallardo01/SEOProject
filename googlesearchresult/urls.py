from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    
    url(r'^google-report-file/download/$', views.download_report_file, name="download_report_file"),
    url(r'^google-report-file/keyword-density-download/$', views.download_keyword_file, name="download_keyword_file"),
    url(r'^google-report-file/adwords_report/$', views.adwords_report, name="adwords_report"),


]
