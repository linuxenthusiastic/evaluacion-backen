from django.contrib import admin
from .models import Conference, Track, Session, Speaker, SessionSpeaker, Registration


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    fields = ['title', 'starts_at', 'capacity']


class SessionSpeakerInline(admin.TabularInline):
    model = SessionSpeaker
    extra = 1


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'starts_at', 'ends_at', 'created']
    list_filter   = ['starts_at']
    search_fields = ['name', 'description']
    inlines       = [TrackInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display  = ['name', 'conference']
    list_filter   = ['conference']
    search_fields = ['name']
    inlines       = [SessionInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display  = ['title', 'track', 'starts_at', 'capacity']
    list_filter   = ['track__conference', 'starts_at']
    search_fields = ['title', 'description']
    inlines       = [SessionSpeakerInline]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name', 'bio']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display  = ['user', 'session', 'registered_at']
    list_filter   = ['session__track__conference']
    search_fields = ['user__username', 'session__title']
