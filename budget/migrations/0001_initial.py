# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Budget'
        db.create_table(u'budget_budget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'budget', ['Budget'])

        # Adding model 'Entry'
        db.create_table(u'budget_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'])),
            ('amount_abs', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('payments_per_year', self.gf('django.db.models.fields.IntegerField')()),
            ('budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Budget'])),
        ))
        db.send_create_signal(u'budget', ['Entry'])

        # Adding model 'Category'
        db.create_table(u'budget_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('factor', self.gf('django.db.models.fields.FloatField')(default=-1)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'], null=True, blank=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'budget', ['Category'])

        # Adding model 'Transaction'
        db.create_table(u'budget_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'budget', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Budget'
        db.delete_table(u'budget_budget')

        # Deleting model 'Entry'
        db.delete_table(u'budget_entry')

        # Deleting model 'Category'
        db.delete_table(u'budget_category')

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