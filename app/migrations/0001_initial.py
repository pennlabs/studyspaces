# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Building'
        db.create_table('app_building', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('app', ['Building'])

        # Adding model 'RoomKind'
        db.create_table('app_roomkind', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Building'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('reserve_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('max_occupancy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('has_computer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_big_screen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_whiteboard', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('contact_phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('app', ['RoomKind'])

        # Adding model 'Room'
        db.create_table('app_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.RoomKind'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('app', ['Room'])

        # Adding model 'FetchedAvailability'
        db.create_table('app_fetchedavailability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Room'])),
        ))
        db.send_create_signal('app', ['FetchedAvailability'])

        # Adding model 'FreeTimeRange'
        db.create_table('app_freetimerange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('availability', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.FetchedAvailability'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
        ))
        db.send_create_signal('app', ['FreeTimeRange'])

        # Adding model 'WeeklyAvailability'
        db.create_table('app_weeklyavailability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.RoomKind'])),
            ('monday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
            ('tuesday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
            ('wednesday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
            ('thursday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
            ('friday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
            ('saturday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
            ('sunday', self.gf('studyspaces.app.TimeRange.TimeRangeField')()),
        ))
        db.send_create_signal('app', ['WeeklyAvailability'])


    def backwards(self, orm):
        
        # Deleting model 'Building'
        db.delete_table('app_building')

        # Deleting model 'RoomKind'
        db.delete_table('app_roomkind')

        # Deleting model 'Room'
        db.delete_table('app_room')

        # Deleting model 'FetchedAvailability'
        db.delete_table('app_fetchedavailability')

        # Deleting model 'FreeTimeRange'
        db.delete_table('app_freetimerange')

        # Deleting model 'WeeklyAvailability'
        db.delete_table('app_weeklyavailability')


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
