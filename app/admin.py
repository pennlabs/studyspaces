from app.models import * 
from django.contrib import admin

class WeeklyInline(admin.StackedInline):
  model = WeeklyAvailability
  extra = 1
  max_num = 1
  verbose_name_plural = "Weekly Hours of Operation" 

class RoomInstanceInline(admin.StackedInline):
  model = Room
  extra = 25
  verbose_name = """For example, for a floor lounge: 'First Floor Lounge, 
Second Floor Lounge, ..."""

class RoomKindAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Basic Info', {
      'fields' : ('building', 'name')
    }),
    ('Room Details', {
      'fields' : ('max_occupancy', 'reserve_type', 'privacy', 'has_computer',
                 'has_big_screen', 'has_whiteboard', 'reserve_url')
    }),
    ('Contact Info', {
      'fields' : ('contact_name', 'contact_phone', 'contact_email')
    }),
    (None, {
      'fields' : ('comments',)
    }),
  )
  
  list_display = ('building', 'name')

  inlines = [WeeklyInline, RoomInstanceInline]

admin.site.register(RoomKind, RoomKindAdmin)
admin.site.register(Building)
