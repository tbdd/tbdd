# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Storefront.associate_tag'
        db.add_column('dhead_storefront', 'associate_tag', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Storefront.associate_tag'
        db.delete_column('dhead_storefront', 'associate_tag')


    models = {
        'dhead.category': {
            'Meta': {'ordering': "('-weight', 'title')", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'storefront': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dhead.Storefront']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'dhead.storefront': {
            'Meta': {'object_name': 'Storefront'},
            'alternate_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'amazon_category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'amazon_zone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'associate_tag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['dhead']
