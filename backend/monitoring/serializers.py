from rest_framework import serializers
from .models import Camera, Zone, VideoFile, Violation
from .services import extract_video_metadata


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = "__all__"
        read_only_fields = ["original_name", "size_bytes", "duration_sec", "fps",
                            "frame_count", "width", "height", "uploaded_at"]

    def create(self, validated_data):
        f = validated_data["file"]
        validated_data["original_name"] = f.name
        validated_data["size_bytes"] = f.size
        obj = super().create(validated_data)
        try:
            meta = extract_video_metadata(obj.file.path)
        except ValueError as e:
            obj.file.delete(save=False)
            obj.delete()
            raise serializers.ValidationError({"file": str(e)})
        for k, v in meta.items():
            setattr(obj, k, v)
        obj.save()
        return obj


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = "__all__"


class DetectionSerializer(serializers.Serializer):
    bbox = serializers.ListField(child=serializers.FloatField(), min_length=4, max_length=4)
    confidence = serializers.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # в JSON ключ "class" (зарезервированное слово в Python)
        self.fields["class"] = serializers.CharField()


class IngestSerializer(serializers.Serializer):
    camera_id = serializers.IntegerField()
    video_id = serializers.IntegerField(required=False, allow_null=True)
    zone_id = serializers.IntegerField(required=False, allow_null=True)
    frame_number = serializers.IntegerField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False)
    detections = DetectionSerializer(many=True)