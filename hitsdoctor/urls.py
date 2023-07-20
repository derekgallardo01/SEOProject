"""hitsdoctor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings



urlpatterns = [
    url(r'^tinymce /', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    #url(r'^', include ('seo.urls')),
    url(r'^', include ('googleTrend.urls')),
    url(r'^', include ('search_query_analysis.urls')),
    url(r'^', include ('googlesearchresult.urls')),
    url(r'^', include ('posts.urls')),
    #url(r'^advanced_filters/', include('advanced_filters.urls')),
    #url(r'^field_choices/(?P<model>.+)/(?P<field_name>.+)/?', views.suggestionskeyword, name='afilters_get_field_choices'),

    # only to allow building dynamically
    #url(r'^field_choices/$', views.suggestionskeyword, name='afilters_get_field_choices'),
    #url(r'^google/suggestions-keyword/$', views.suggestionskeyword, name="suggestionskeyword"),
    #url(r'^admin/my_special_link_in_admin/$', googleTrend.views.special_admin_page),
    # path('', index),
    
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Convergence Suite"
admin.site.site_title = "Convergence Suite"
admin.site.index_title = "Welcome to Convergence Suite"
