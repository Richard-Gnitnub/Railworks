from django.contrib import admin
from .models import (
    Gauge,
    BullheadChairs,
    BullheadJawSection,
    BullheadKey,
    BullheadBossAndFerrule,
    Track,
    Timber,
    UserProfile,
    STLDownloadLog
)


@admin.register(Gauge)
class GaugeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'description')
    search_fields = ('name',)


@admin.register(BullheadChairs)
class BullheadChairsAdmin(admin.ModelAdmin):
    list_display = ('type', 'plinth_thickness', 'edge_thickness', 'seat_thickness')
    search_fields = ('type',)


@admin.register(BullheadJawSection)
class BullheadJawSectionAdmin(admin.ModelAdmin):
    list_display = ('chair', 'jaw_type', 'section', 'rib_depth', 'rib_width')
    search_fields = ('chair__type', 'jaw_type', 'section')


@admin.register(BullheadKey)
class BullheadKeyAdmin(admin.ModelAdmin):
    list_display = ('chair', 'type', 'length', 'pad_length', 'deformation')
    search_fields = ('chair__type', 'type')


@admin.register(BullheadBossAndFerrule)
class BullheadBossAndFerruleAdmin(admin.ModelAdmin):
    list_display = ('chair', 'component', 'height', 'diameter')
    search_fields = ('chair__type', 'component')


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'gauge', 'total_length', 'timber_spacing', 'chair_alignment', 'is_straight')
    search_fields = ('gauge__name',)


@admin.register(Timber)
class TimberAdmin(admin.ModelAdmin):
    list_display = ('track', 'length', 'width', 'depth', 'position')
    search_fields = ('track__id',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    search_fields = ('user__username', 'role')


@admin.register(STLDownloadLog)
class STLDownloadLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'chair', 'track', 'timestamp', 'file_path')
    search_fields = ('user__username', 'file_path')
