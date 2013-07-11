from django.conf.urls import patterns, include, url
from wishlist.views import *

urlpatterns = patterns('',
        url(r'^$', 
                WishItemList.as_view(), name='wishlist'),
        url(r'^item/(?P<pk>\d+)/$', 
                WishItemDetail.as_view(), name='view_wishitem'),
)
