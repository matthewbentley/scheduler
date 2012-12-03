'''
Created on Nov 14, 2012

@author: Stuart Long
'''

from django.conf.urls import patterns, url

urlpatterns = patterns('',
   # url(r'^$',
   #     ListView.as_view(
   #         queryset=Poll.objects.order_by('-pub_date')[:5],
   #         context_object_name='latest_poll_list',
   #         template_name='schedule.html'),
   #     name='index'),
   # url(r'^(?P<pk>\d+)/$',
   #     DetailView.as_view(
   #         model=Poll,
   #         template_name='schedule.html'),
   #     name='detail'),
   # url(r'^$',
   #     DetailView.as_view(
   #         model=Poll,
   #         template_name='schedule.html'),
   #     name='results'),
    url(r'^scheduler/$', 'poll.views.schedule', name='base'),
    url(r'^scheduler/add/$', 'poll.views.add', name='add'),
    url(r'^scheduler/info$', 'poll.views.info', name='info'),
)