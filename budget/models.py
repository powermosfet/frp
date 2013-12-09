from django.db import models
from decimal import Decimal

class Budget(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True)
    description = models.CharField(max_length = 30)

    def result(self):
        return Decimal(sum(x.amount_per_month() for x in self.entry_set.all()))

    def __unicode__(self):
        return u"[{0}] {1}".format(self.timestamp.date(), self.description)

FACTOR_CHOICES = [ (-1, 'Expense'),
                   ( 1, 'Income' ) ]

class Entry(models.Model):
    category = models.ForeignKey('Category')
    amount_abs = models.DecimalField(max_digits = 10, decimal_places = 2)
    payments_per_year = models.IntegerField()
    budget = models.ForeignKey('Budget')

    def amount(self):
        return Decimal(float(self.amount_abs) * float(self.category.factor))

    def amount_per_month(self):
        return self.amount() * Decimal(self.payments_per_year / 12.0 )

    def __unicode__(self):
        return u"{0}: {1} [{2}x]".format(self.category,
                                        self.amount(),
                                        self.payments_per_year)

class Category(models.Model):
    name = models.CharField(max_length = 30)
    factor = models.FloatField(help_text = 'Type', default = -1, choices = FACTOR_CHOICES)
    parent = models.ForeignKey('Category', blank = True, null = True)
    string = models.CharField(max_length = 250, editable = False)

    class Meta:
        ordering = ['string']

    def save(self, *args, **kwargs):
        self.string = self.__unicode__()
        super(Category, self).save(*args, **kwargs)

    def is_or_child(self, other):
        if other.pk == self.pk: return True
        elif self.parent is None: return False
        else: return self.parent.is_or_child(other)
    
    def __unicode__(self):
        if self.parent is None:
            return u"{0}".format(self.name)
        else:
            return u"{0}/{1}".format(self.parent.__unicode__(), self.name)

class Transaction(models.Model):
    category = models.ForeignKey('Category', blank=False)
    comment = models.CharField(max_length=80, blank=True)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()

    def result(self):
        return Decimal(float(abs(self.amount)) * float(self.category.factor))

    def __unicode__(self):
        return u"{0}: {1} - {2} ({3})".format(
                self.date,
                self.category,
                self.amount, 
                self.comment)
