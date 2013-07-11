# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Budget'
        db.create_table(u'budget_budget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'budget', ['Budget'])

        # Adding model 'Record'
        db.create_table(u'budget_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('payments_per_year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'budget', ['Record'])

        # Adding model 'Category'
        db.create_table(u'budget_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'budget', ['Category'])


    def backwards(self, orm):
        # Deleting model 'Budget'
        db.delete_table(u'budget_budget')

        # Deleting model 'Record'
        db.delete_table(u'budget_record')

        # Deleting model 'Category'
        db.delete_table(u'budget_category')


    models = {
        u'budget.budget': {
            'Meta': {'object_name': 'Budget'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['budget.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payments_per_year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['budget']