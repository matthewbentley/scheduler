from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scheduler.views.home', name='home'),
    # url(r'^scheduler/', include('scheduler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	
	url(r'^scheduler/$', 'course_scheduler.views.schedule', name='base'),
    url(r'^scheduler/add/$', 'course_scheduler.views.add', name='add'),
    #url(r'^scheduler/add/search/$', 'course_scheduler.views.search', name='search'),
)
