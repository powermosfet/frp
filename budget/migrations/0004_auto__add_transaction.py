# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'budget_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'budget', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table(u'budget_transaction')


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
        u'budget.entry': {
            'Meta': {'object_name': 'Entry'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'budget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Budget']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payments_per_year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'budget.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['budget']