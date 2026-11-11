from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CameraViewSet, ZoneViewSet, VideoFileViewSet,
                    ViolationViewSet, IngestDetectionsView)

router = DefaultRouter()
router.register("cameras", CameraViewSet, basename="camera")
router.register("zones", ZoneViewSet, basename="zone")
router.register("videos", VideoFileViewSet, basename="video")
router.register("violations", ViolationViewSet, basename="violation")

urlpatterns = [
    path("", include(router.urls)),
    path("detections/", IngestDetectionsView.as_view(), name="detections"),
]