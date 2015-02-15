from django.conf.urls import patterns, url

from input_user import views  # pytharm shows import  error, but actually it is correct

__author__ = 'Junfeng'

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
)