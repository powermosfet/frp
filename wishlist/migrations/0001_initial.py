# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WishItem'
        db.create_table(u'wishlist_wishitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('added_by', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'wishlist', ['WishItem'])

        # Adding model 'Product'
        db.create_table(u'wishlist_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('wishItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wishlist.WishItem'])),
        ))
        db.send_create_signal(u'wishlist', ['Product'])


    def backwards(self, orm):
        # Deleting model 'WishItem'
        db.delete_table(u'wishlist_wishitem')

        # Deleting model 'Product'
        db.delete_table(u'wishlist_product')


    models = {
        u'wishlist.product': {
            'Meta': {'object_name': 'Product'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'supplier': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'wishItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wishlist.WishItem']"})
        },
        u'wishlist.wishitem': {
            'Meta': {'object_name': 'WishItem'},
            'added_by': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['wishlist']