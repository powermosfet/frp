# Create your views here.
from wishlist.models import *
from django.views.generic import *

class WishItemList(ListView):
    model = WishItem

class WishItemDetail(DetailView):
    model = WishItem
