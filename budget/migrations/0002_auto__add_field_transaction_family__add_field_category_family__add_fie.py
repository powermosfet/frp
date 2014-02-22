# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Transaction.family'
        db.add_column(u'budget_transaction', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['family.Family']),
                      keep_default=False)

        # Adding field 'Category.family'
        db.add_column(u'budget_category', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['family.Family']),
                      keep_default=False)

        # Adding field 'Budget.family'
        db.add_column(u'budget_budget', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['family.Family']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Transaction.family'
        db.delete_column(u'budget_transaction', 'family_id')

        # Deleting field 'Category.family'
        db.delete_column(u'budget_category', 'family_id')

        # Deleting field 'Budget.family'
        db.delete_column(u'budget_budget', 'family_id')


    models = {
        u'budget.budget': {
            'Meta': {'object_name': 'Budget'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['family.Family']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'budget.category': {
            'Meta': {'ordering': "['string']", 'object_name': 'Category'},
            'factor': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['family.Family']"}),
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
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['family.Family']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'family.family': {
            'Meta': {'object_name': 'Family'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['budget']