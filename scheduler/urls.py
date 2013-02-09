'''
Created on Nov 14, 2012

@author: Stuart Long
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^scheduler/$', 'course_scheduler.views.schedule', name='base'),
    url(r'^scheduler/add/$', 'course_scheduler.views.add', name='add'),
    url(r'^scheduler/info$', 'course_scheduler.views.info', name='info'),
    url(r'^scheduler/instructor$', 'course_scheduler.views.instructor', name='instructor'),
    url(r'^scheduler/login', 'course_scheduler.views.login', name='login'),
    url(r'^scheduler/inscourse$', 'course_scheduler.views.inscourse', name='inscourse'),
    url(r'^scheduler/inssearch$', 'course_scheduler.views.inssearch', name='insearch'),
    url(r'^scheduler/addcourse$', 'course_scheduler.views.addcourse', name='addcourse'),
    url(r'^scheduler/removecourse$', 'course_scheduler.views.removecourse', name='removecourse'),
    url(r'^scheduler/mycourses$', 'course_scheduler.views.mycourses', name='mycourses'),
    url(r'^scheduler/customevent$', 'course_scheduler.views.customevent', name='customevent'),
    url(r'^scheduler/about$', 'course_scheduler.views.about', name='about'),
)
