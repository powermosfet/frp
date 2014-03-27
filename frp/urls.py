from django.conf.urls import patterns, include, url
from wishlist.urls import *
from budget.urls import *
from family.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('wishlist.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^wishlist/', include('wishlist.urls')),
    url(r'^budget/', include('budget.urls')),
    url(r'^login/', 'family.views.family_login', {'template_name': 'login.html', 'authentication_form':LoginForm}, name = 'login'),
    url(r'^logout/', 'django.contrib.auth.views.logout',{'template_name': 'logout.html'}, name = 'logout'),
    url(r'^register/', Register.as_view(), name = 'register'),
    url(r'^users/(?P<slug>\w+)/', Profile.as_view(), name = 'register'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
