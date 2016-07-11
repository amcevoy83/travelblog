from django.conf.urls import url
import views
from . import views
from accounts.views import *

urlpatterns =[
              # url(r'^blog/$', views.post_list, name='post_list'),
              url(r'^$', views.home, name='home'),
              url(r'^blog/(?P<id>\d+)/$', views.post_detail),
              url(r'^blog/$', views.melbourne,  name='melbourne'),
              url(r'^post/new/$', views.new_post, name='new_post'),
              url(r'^gallery/$', views.gallery, name='gallery'),
              url(r'^suggestion/$', views.suggestion_post, name='suggestion_post'),
              url(r'^register/$','accounts.views.register', name='register'),
              url(r'^login/$','accounts.views.login', name='login'),
              url(r'^logout/$','accounts.views.logout', name='logout'), ##removed two // at the start of the logout regex
              url(r'^profile/$', 'accounts.views.profile', name='profile'),
            #  url(r'^post/new/$', views.new_post, name='new_post'),

]

          # url(r'^blog/(?P<creation_date>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$])/$', views.post_detail),
              #url(r'^blog/(?P<post_title>\w)/$', views.post_detail),
           #url(r'^blog/(?P<content>\[a-zA-Z]+)/$', views.post_detail),

            # url (r'^blog/(?P<time>/^(?:Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])$/')
