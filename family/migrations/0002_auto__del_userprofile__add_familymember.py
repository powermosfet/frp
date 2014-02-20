# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'family_userprofile')

        # Removing M2M table for field families on 'UserProfile'
        db.delete_table(db.shorten_name(u'family_userprofile_families'))

        # Adding model 'FamilyMember'
        db.create_table(u'family_familymember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('login', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'family', ['FamilyMember'])

        # Adding M2M table for field families on 'FamilyMember'
        m2m_table_name = db.shorten_name(u'family_familymember_families')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('familymember', models.ForeignKey(orm[u'family.familymember'], null=False)),
            ('family', models.ForeignKey(orm[u'family.family'], null=False))
        ))
        db.create_unique(m2m_table_name, ['familymember_id', 'family_id'])


    def backwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'family_userprofile', (
            ('login', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'family', ['UserProfile'])

        # Adding M2M table for field families on 'UserProfile'
        m2m_table_name = db.shorten_name(u'family_userprofile_families')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'family.userprofile'], null=False)),
            ('family', models.ForeignKey(orm[u'family.family'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'family_id'])

        # Deleting model 'FamilyMember'
        db.delete_table(u'family_familymember')

        # Removing M2M table for field families on 'FamilyMember'
        db.delete_table(db.shorten_name(u'family_familymember_families'))


    models = {
        u'family.family': {
            'Meta': {'object_name': 'Family'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'family.familymember': {
            'Meta': {'object_name': 'FamilyMember'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'families': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['family.Family']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['family']