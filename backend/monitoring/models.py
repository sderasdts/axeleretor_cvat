from django.db import models


class Camera(models.Model):
    class SourceType(models.TextChoices):
        FILE = "file", "Видеофайл"
        RTP = "rtp", "RTP-поток"

    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=10, choices=SourceType.choices, default=SourceType.FILE)
    source_uri = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=100)
    required_ppe = models.JSONField(default=list)  # ["helmet", "gloves", "vest"]
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.camera.name} / {self.name}"


class VideoFile(models.Model):
    camera = models.ForeignKey(Camera, null=True, blank=True, on_delete=models.SET_NULL, related_name="videos")
    file = models.FileField(upload_to="videos/%Y/%m/%d/")
    original_name = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(default=0)
    duration_sec = models.FloatField(null=True, blank=True)
    fps = models.FloatField(null=True, blank=True)
    frame_count = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name


class Violation(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="violations")
    zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL, related_name="violations")
    video = models.ForeignKey(VideoFile, null=True, blank=True, on_delete=models.SET_NULL, related_name="violations")
    missing_ppe = models.JSONField(default=list)
    frame_number = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(db_index=True)
    bbox_x1 = models.FloatField()
    bbox_y1 = models.FloatField()
    bbox_x2 = models.FloatField()
    bbox_y2 = models.FloatField()
    confidence = models.FloatField()
    external_id = models.CharField(max_length=100, blank=True, db_index=True)  # для СКУД/1С
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [models.Index(fields=["camera", "-timestamp"])]