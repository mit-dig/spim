from django.conf.urls import patterns, include, url

urlpatterns = patterns('spim_module.views',
	url(r'^$', 'main'),
#	url(r'results/$', 'results'),
	url(r'logout/$', 'logout'),
)
