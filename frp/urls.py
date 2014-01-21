from django.conf.urls import patterns, include, url
from wishlist.urls import *
from budget.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wishlist.views.mainView', name='home'),
    url(r'^$', include('wishlist.urls')),
    url(r'^wishlist/', include('wishlist.urls')),
    url(r'^budget/', include('budget.urls')),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name = 'login'),
    url(r'^logout/', 'django.contrib.auth.views.logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
