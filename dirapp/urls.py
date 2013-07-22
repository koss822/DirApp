from django.conf.urls import patterns, url
from dirapp import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView, name='index'),
    url(r'^detail/(?P<pk>\d+)/$', views.PersonDetail.as_view(), name='detail'),
    url(r'^edit_profile/$', views.EditProfile, name='edit_profile'),
    url(r'^login/$', views.mylogin, name='login'),
    url(r'^logout/$', views.mylogout, name='logout'),
    )
