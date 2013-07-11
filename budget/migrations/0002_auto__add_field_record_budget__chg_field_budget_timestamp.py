# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Record.budget'
        db.add_column(u'budget_record', 'budget',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Budget'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Budget.timestamp'
        db.alter_column(u'budget_budget', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Deleting field 'Record.budget'
        db.delete_column(u'budget_record', 'budget_id')


        # Changing field 'Budget.timestamp'
        db.alter_column(u'budget_budget', 'timestamp', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

    models = {
        u'budget.budget': {
            'Meta': {'object_name': 'Budget'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'budget.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']", 'null': 'True', 'blank': 'True'})
        },
        u'budget.record': {
            'Meta': {'object_name': 'Record'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'budget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Budget']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payments_per_year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['budget']