# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Foo'
        db.create_table(u'fig_codelab_foo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_bar', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'fig_codelab', ['Foo'])


    def backwards(self, orm):
        # Deleting model 'Foo'
        db.delete_table(u'fig_codelab_foo')


    models = {
        u'fig_codelab.foo': {
            'Meta': {'object_name': 'Foo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_bar': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fig_codelab']