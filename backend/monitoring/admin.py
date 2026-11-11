from django.contrib import admin
from .models import Camera, Zone, VideoFile, Violation

for m in (Camera, Zone, VideoFile, Violation):
    admin.site.register(m)