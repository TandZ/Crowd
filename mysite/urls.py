from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
	(r'^index/(?P<method>\w+)/$', 'sports.views.index'),
	(r'^home/$', 'sports.views.main'),
	(r'^info/$', 'sports.views.getinfo'),
	(r'^info/(?P<place_name>\w+)/$', 'sports.views.dispinfo'),
	(r'^update/$', 'sports.views.update'),
	(r'^update/create/$', 'sports.views.createentry'),
	(r'^update/add/(?P<place_name>\w+)/$', 'sports.views.editentry'),
	(r'^results/$', 'sports.views.results'),
	(r'^update/create/redirect/$', 'sports.views.createentrycontinue'),
	(r'^admin/', include(admin.site.urls)),
)
