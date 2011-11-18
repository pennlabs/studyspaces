# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RoomKind.reserve_url'
        db.add_column('app_roomkind', 'reserve_url', self.gf('django.db.models.fields.CharField')(default='', max_length=512), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RoomKind.reserve_url'
        db.delete_column('app_roomkind', 'reserve_url')


    models = {
        'app.building': {
            'Meta': {'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '13.369999999999999'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '42'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'app.fetchedavailability': {
            'Meta': {'object_name': 'FetchedAvailability'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Room']"})
        },
        'app.freetimerange': {
            'Meta': {'object_name': 'FreeTimeRange'},
            'availability': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.FetchedAvailability']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('studyspaces.app.TimeRange.TimeRangeField', [], {})
        },
        'app.room': {
            'Meta': {'object_name': 'Room'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.RoomKind']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'app.roomkind': {
            'Meta': {'object_name': 'RoomKind'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Building']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'contact_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'has_big_screen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_computer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_whiteboard': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reserve_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reserve_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        },
        'app.weeklyavailability': {
            'Meta': {'object_name': 'WeeklyAvailability'},
            'friday': ('studyspaces.app.TimeRange.TimeRangeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('studyspaces.app.TimeRange.TimeRangeField', [], {}),
            'room_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.RoomKind']"}),
            'saturday': ('studyspaces.app.TimeRange.TimeRangeField', [], {}),
            'sunday': ('studyspaces.app.TimeRange.TimeRangeField', [], {}),
            'thursday': ('studyspaces.app.TimeRange.TimeRangeField', [], {}),
            'tuesday': ('studyspaces.app.TimeRange.TimeRangeField', [], {}),
            'wednesday': ('studyspaces.app.TimeRange.TimeRangeField', [], {})
        }
    }

    complete_apps = ['app']
