from django.utils import timezone
from django.utils.dateparse import parse_datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Camera, Zone, VideoFile, Violation
from .serializers import (CameraSerializer, ZoneSerializer, VideoFileSerializer,
                          ViolationSerializer, IngestSerializer)
from .services import find_missing_ppe


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all().order_by("id")
    serializer_class = CameraSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    serializer_class = ZoneSerializer

    def get_queryset(self):
        qs = Zone.objects.all().order_by("id")
        camera = self.request.query_params.get("camera")
        return qs.filter(camera_id=camera) if camera else qs


class VideoFileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = VideoFile.objects.all().order_by("-uploaded_at")
    serializer_class = VideoFileSerializer
    parser_classes = [MultiPartParser, FormParser]


class ViolationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViolationSerializer

    @extend_schema(parameters=[
        OpenApiParameter("camera", int), OpenApiParameter("zone", int),
        OpenApiParameter("video", int),
        OpenApiParameter("date_from", str, description="ISO datetime"),
        OpenApiParameter("date_to", str, description="ISO datetime"),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Violation.objects.all()
        p = self.request.query_params
        for param, field in (("camera", "camera_id"), ("zone", "zone_id"), ("video", "video_id")):
            if p.get(param):
                qs = qs.filter(**{field: p[param]})
        if p.get("date_from") and parse_datetime(p["date_from"]):
            qs = qs.filter(timestamp__gte=parse_datetime(p["date_from"]))
        if p.get("date_to") and parse_datetime(p["date_to"]):
            qs = qs.filter(timestamp__lte=parse_datetime(p["date_to"]))
        return qs


class IngestDetectionsView(APIView):
    """Приём результатов детекции от ML-модуля."""

    @extend_schema(request=IngestSerializer, responses={201: dict})
    def post(self, request):
        s = IngestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data

        try:
            camera = Camera.objects.get(pk=d["camera_id"])
        except Camera.DoesNotExist:
            return Response({"detail": "Камера не найдена"}, status=status.HTTP_404_NOT_FOUND)

        zones = Zone.objects.filter(camera=camera, is_active=True)
        zone = zones.filter(pk=d["zone_id"]).first() if d.get("zone_id") else zones.first()
        if not zone:
            return Response({"persons": 0, "violations": 0, "detail": "Нет активной зоны"},
                            status=status.HTTP_201_CREATED)

        dets = d["detections"]
        persons = [x for x in dets if x["class"] == "person"]
        ppe = [x for x in dets if x["class"] != "person"]
        ts = d.get("timestamp") or timezone.now()

        violations = []
        for p in persons:
            missing = find_missing_ppe(p["bbox"], ppe, zone.required_ppe)
            if missing:
                x1, y1, x2, y2 = p["bbox"]
                violations.append(Violation(
                    camera=camera, zone=zone, video_id=d.get("video_id"),
                    missing_ppe=missing, frame_number=d.get("frame_number"),
                    timestamp=ts, bbox_x1=x1, bbox_y1=y1, bbox_x2=x2, bbox_y2=y2,
                    confidence=p["confidence"],
                ))
        Violation.objects.bulk_create(violations)
        return Response({"persons": len(persons), "violations": len(violations)},
                        status=status.HTTP_201_CREATED)