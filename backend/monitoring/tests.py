from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import Camera, Employee, Frame, PPERule, VideoFile, Violation, Zone


class DbModelsTests(TestCase):
    def setUp(self):
        self.camera = Camera.objects.create(name="Cam 1")
        self.zone = Zone.objects.create(camera=self.camera, name="Цех", required_ppe=["helmet"])
        self.video = VideoFile.objects.create(camera=self.camera, file="videos/a.mp4", original_name="a.mp4")

    def test_employee_external_id_unique_but_optional(self):
        Employee.objects.create(full_name="A")
        Employee.objects.create(full_name="B")  # несколько сотрудников без external_id
        Employee.objects.create(full_name="C", external_id="SKUD-1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Employee.objects.create(full_name="D", external_id="SKUD-1")

    def test_ppe_rule_unique_per_zone(self):
        PPERule.objects.create(zone=self.zone, ppe_class="helmet")
        with self.assertRaises(IntegrityError), transaction.atomic():
            PPERule.objects.create(zone=self.zone, ppe_class="helmet")

    def test_ppe_rule_confidence_range(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            PPERule.objects.create(zone=self.zone, ppe_class="vest", min_confidence=1.5)

    def test_frame_unique_number_within_video(self):
        ts = timezone.now()
        Frame.objects.create(camera=self.camera, video=self.video, frame_number=1, timestamp=ts)
        Frame.objects.create(camera=self.camera, frame_number=1, timestamp=ts)  # RTP-поток без видео
        with self.assertRaises(IntegrityError), transaction.atomic():
            Frame.objects.create(camera=self.camera, video=self.video, frame_number=1, timestamp=ts)

    def test_violation_links_frame_and_employee(self):
        ts = timezone.now()
        frame = Frame.objects.create(camera=self.camera, video=self.video, frame_number=5, timestamp=ts)
        emp = Employee.objects.create(full_name="Иванов", external_id="SKUD-7")
        v = Violation.objects.create(camera=self.camera, zone=self.zone, frame=frame, employee=emp,
                                     missing_ppe=["helmet"], timestamp=ts, confidence=0.9,
                                     bbox_x1=0, bbox_y1=0, bbox_x2=10, bbox_y2=20)
        self.assertEqual(list(frame.violations.all()), [v])
        self.assertEqual(list(emp.violations.all()), [v])
        frame.delete()
        v.refresh_from_db()
        self.assertIsNone(v.frame)  # нарушение сохраняется при удалении кадра

    def test_violation_confidence_range(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Violation.objects.create(camera=self.camera, timestamp=timezone.now(), confidence=-0.1,
                                     bbox_x1=0, bbox_y1=0, bbox_x2=1, bbox_y2=1)
