# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TempModel'
        db.delete_table('app_tempmodel')


    def backwards(self, orm):
        
        # Adding model 'TempModel'
        db.create_table('app_tempmodel', (
            ('foo', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('app', ['TempModel'])


    models = {
        'app.building': {
            'Meta': {'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'reserve_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
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
