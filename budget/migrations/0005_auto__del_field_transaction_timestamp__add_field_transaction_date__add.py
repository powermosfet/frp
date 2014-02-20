# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Transaction.timestamp'
        db.delete_column(u'budget_transaction', 'timestamp')

        # Adding field 'Transaction.date'
        db.add_column(u'budget_transaction', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1900, 1, 1, 0, 0)),
                      keep_default=False)

        # Adding field 'Category.factor'
        db.add_column(u'budget_category', 'factor',
                      self.gf('django.db.models.fields.FloatField')(default=-1),
                      keep_default=False)

        # Adding field 'Category.string'
        db.add_column(u'budget_category', 'string',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250),
                      keep_default=False)

        # Deleting field 'Entry.amount'
        db.delete_column(u'budget_entry', 'amount')

        # Adding field 'Entry.amount_abs'
        db.add_column(u'budget_entry', 'amount_abs',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Transaction.timestamp'
        db.add_column(u'budget_transaction', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 23, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Transaction.date'
        db.delete_column(u'budget_transaction', 'date')

        # Deleting field 'Category.factor'
        db.delete_column(u'budget_category', 'factor')

        # Deleting field 'Category.string'
        db.delete_column(u'budget_category', 'string')

        # Adding field 'Entry.amount'
        db.add_column(u'budget_entry', 'amount',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Deleting field 'Entry.amount_abs'
        db.delete_column(u'budget_entry', 'amount_abs')


    models = {
        u'budget.budget': {
            'Meta': {'object_name': 'Budget'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'budget.category': {
            'Meta': {'ordering': "['string']", 'object_name': 'Category'},
            'factor': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']", 'null': 'True', 'blank': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'budget.entry': {
            'Meta': {'object_name': 'Entry'},
            'amount_abs': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'budget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Budget']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payments_per_year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'budget.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['budget']