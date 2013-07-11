from django.db import models
from decimal import Decimal

# Create your models here.
class WishItem(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    added_by = models.CharField(max_length=30)
    added_time = models.DateTimeField()
    def mincost(self):
        return min(x.cost for x in self.product_set.all())
    def maxcost(self):
        return max(x.cost for x in self.product_set.all())
    def __unicode__(self):
        return self.name

class Product(models.Model):
    supplier = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    wishItem = models.ForeignKey('WishItem')
    def __unicode__(self):
        return self.name
