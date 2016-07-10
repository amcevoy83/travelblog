from django.conf.urls import url
import views
from . import views

urlpatterns =[
              # url(r'^blog/$', views.post_list, name='post_list'),
              url(r'^$', views.home, name='home'),
              url(r'^blog/(?P<id>\d+)/$', views.post_detail),
              url(r'^blog/$', views.home,  name='home'),
              url(r'^post/new/$', views.new_post, name='new_post'),
              url(r'^gallery/$', views.gallery, name='gallery'),
              url(r'^suggestion/$', views.suggestion_post, name='suggestion_post'),

]

