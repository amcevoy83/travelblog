"""travelblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blog.views import *
from settings import MEDIA_ROOT
import settings
from django.conf.urls.static import static
#from views import paypal_return, paypal_cancel, new_product
from paypal.standard.ipn import urls as paypal_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^p4yp4lur14u5e/', include(paypal_urls)),
    url(r'^paypal-return/', paypal_return),
    url(r'^product/$', new_product, name='new_product'),
    url(r'^paypal-cancel/', paypal_cancel),
    url(r'',include('blog.urls')),
    url(r'^post/new/$',new_post, name='new_post'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
