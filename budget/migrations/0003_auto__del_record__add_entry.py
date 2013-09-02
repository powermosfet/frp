# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Record'
        db.delete_table(u'budget_record')

        # Adding model 'Entry'
        db.create_table(u'budget_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('payments_per_year', self.gf('django.db.models.fields.IntegerField')()),
            ('budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Budget'])),
        ))
        db.send_create_signal(u'budget', ['Entry'])


    def backwards(self, orm):
        # Adding model 'Record'
        db.create_table(u'budget_record', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Category'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Budget'], null=True, blank=True)),
            ('payments_per_year', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'budget', ['Record'])

        # Deleting model 'Entry'
        db.delete_table(u'budget_entry')


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
        }
    }

    complete_apps = ['budget']