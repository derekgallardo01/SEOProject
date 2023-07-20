from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    
    url(r'^keyword-analysis/bad-to-ok/$', views.badtook, name="badtook"),
    url(r'^keyword-analysis/no-conversion/$', views.noconv, name="noconv"),
    url(r'^keyword-analysis/converted-found/$', views.convertedfound, name="convertedfound"),
    url(r'^keyword-analysis/converted-not-found/$', views.convertednotfound, name="convertednotfound"),


]

