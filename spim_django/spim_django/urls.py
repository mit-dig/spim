from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spim_django.views.home', name='home'),
    # url(r'^spim_django/', include('spim_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^spim_module/', include('spim_module.urls')),
    url(r'^openid/', include('django_openid_auth.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
