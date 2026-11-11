from django.contrib import admin
from .models import Camera, Zone, VideoFile, Violation, Employee, PPERule, Frame

for m in (Camera, Zone, VideoFile):
    admin.site.register(m)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "personnel_number", "department", "external_id", "is_active")
    search_fields = ("full_name", "personnel_number", "external_id")
    list_filter = ("is_active", "department")


@admin.register(PPERule)
class PPERuleAdmin(admin.ModelAdmin):
    list_display = ("zone", "ppe_class", "is_required", "min_confidence", "is_active")
    list_filter = ("ppe_class", "is_active", "zone__camera")


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ("id", "camera", "video", "frame_number", "timestamp", "persons_count")
    list_filter = ("camera",)
    date_hierarchy = "timestamp"


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ("id", "camera", "zone", "employee", "missing_ppe", "confidence", "timestamp")
    list_filter = ("camera", "zone")
    date_hierarchy = "timestamp"
    raw_id_fields = ("frame", "video", "employee")
