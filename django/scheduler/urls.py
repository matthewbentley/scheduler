'''
Created on Nov 14, 2012

@author: Stuart Long
'''

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^scheduler/$', 'course_scheduler.views.schedule', name='base'),
    url(r'^scheduler/add/$', 'course_scheduler.views.add', name='add'),
    url(r'^scheduler/info$', 'course_scheduler.views.info', name='info'),
    url(r'^scheduler/login', 'course_scheduler.views.login', name='login'),
)
