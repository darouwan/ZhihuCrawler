from django.conf.urls import patterns, url

from input_user import views  # pycharm shows an import error, but actually it is correct

__author__ = 'Junfeng'

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^record$', views.record, name='record'),

)