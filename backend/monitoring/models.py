from django.db import models
from django.db.models import Q


class PPEClass(models.TextChoices):
    """Классы СИЗ, которые распознаёт ML-модуль."""
    HELMET = "helmet", "Каска"
    GLOVES = "gloves", "Перчатки"
    VEST = "vest", "Сигнальный жилет"
    GOGGLES = "goggles", "Защитные очки"
    MASK = "mask", "Респиратор/маска"
    BOOTS = "boots", "Защитная обувь"


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


class Employee(models.Model):
    """Сотрудник. external_id — идентификатор в СКУД для будущей интеграции."""
    full_name = models.CharField(max_length=255)
    personnel_number = models.CharField(max_length=50, blank=True, db_index=True)  # табельный номер
    position = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)
    external_id = models.CharField(max_length=100, null=True, blank=True, unique=True)  # ID в СКУД
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class PPERule(models.Model):
    """Правило: какой класс СИЗ обязателен в зоне и с каким минимальным confidence."""
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="ppe_rules")
    ppe_class = models.CharField(max_length=20, choices=PPEClass.choices)
    is_required = models.BooleanField(default=True)
    min_confidence = models.FloatField(default=0.5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "monitoring_ppe_rule"
        ordering = ["zone_id", "ppe_class"]
        constraints = [
            models.UniqueConstraint(fields=["zone", "ppe_class"], name="uniq_ppe_rule_zone_class"),
            models.CheckConstraint(condition=Q(min_confidence__gte=0) & Q(min_confidence__lte=1),
                                   name="ppe_rule_min_confidence_0_1"),
        ]

    def __str__(self):
        return f"{self.zone} — {self.get_ppe_class_display()}"


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


class Frame(models.Model):
    """Обработанный кадр видеопотока с сырыми детекциями ML."""
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="frames")
    video = models.ForeignKey(VideoFile, null=True, blank=True, on_delete=models.CASCADE, related_name="frames")
    frame_number = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(db_index=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to="frames/%Y/%m/%d/", blank=True)  # снапшот кадра (опционально)
    detections = models.JSONField(default=list)  # [{"class", "confidence", "bbox"}]
    persons_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [models.Index(fields=["camera", "-timestamp"], name="frame_camera_ts_idx")]
        constraints = [
            models.UniqueConstraint(fields=["video", "frame_number"], name="uniq_frame_video_number",
                                    condition=Q(video__isnull=False, frame_number__isnull=False)),
        ]

    def __str__(self):
        return f"{self.camera.name} @ {self.timestamp:%Y-%m-%d %H:%M:%S} #{self.frame_number}"


class Violation(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="violations")
    zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL, related_name="violations")
    video = models.ForeignKey(VideoFile, null=True, blank=True, on_delete=models.SET_NULL, related_name="violations")
    frame = models.ForeignKey(Frame, null=True, blank=True, on_delete=models.SET_NULL, related_name="violations")
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name="violations")
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
        indexes = [
            models.Index(fields=["camera", "-timestamp"]),
            models.Index(fields=["zone", "-timestamp"], name="violation_zone_ts_idx"),
            models.Index(fields=["employee", "-timestamp"], name="violation_employee_ts_idx"),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(confidence__gte=0) & Q(confidence__lte=1),
                                   name="violation_confidence_0_1"),
        ]

    def __str__(self):
        return f"{self.camera.name} @ {self.timestamp:%Y-%m-%d %H:%M:%S}: {', '.join(self.missing_ppe)}"
