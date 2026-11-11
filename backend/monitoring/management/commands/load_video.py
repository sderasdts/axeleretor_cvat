from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from monitoring.models import Camera, VideoFile
from monitoring.services import extract_video_metadata


class Command(BaseCommand):
    help = "Загрузить видеофайл в БД: python manage.py load_video путь.mp4 --camera 1"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--camera", type=int, default=None)

    def handle(self, *args, **opts):
        p = Path(opts["path"])
        if not p.exists():
            raise CommandError(f"Файл не найден: {p}")
        try:
            meta = extract_video_metadata(p)
        except ValueError as e:
            raise CommandError(str(e))
        camera = Camera.objects.filter(pk=opts["camera"]).first() if opts["camera"] else None
        with p.open("rb") as f:
            v = VideoFile(camera=camera, original_name=p.name, size_bytes=p.stat().st_size, **meta)
            v.file.save(p.name, File(f))
        self.stdout.write(self.style.SUCCESS(f"Загружено: id={v.id}, {meta}"))