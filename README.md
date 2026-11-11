# PPE Monitor

Система распознавания СИЗ по видеопотоку.

## Запуск backend
```bash
docker compose up -d
python -m venv .venv && source .venv/Scripts/activate
pip install -r backend/requirements.txt
cp .env.example .env
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Swagger: http://127.0.0.1:8000/api/docs/  Admin: http://127.0.0.1:8000/admin/

## API (префикс /api/)
| Метод | URL | Описание |
|---|---|---|
| GET/POST | /cameras/ | камеры |
| GET/PUT/DELETE | /cameras/{id}/ | камера |
| GET/POST | /zones/?camera=ID | зоны, `required_ppe` = ["helmet","gloves","vest"] |
| GET/POST | /videos/ | загрузка видео (multipart: file, camera) |
| GET | /violations/ | фильтры: camera, zone, video, date_from, date_to |
| POST | /detections/ | приём детекций от ML |

## Формат от ML (POST /api/detections/)
```json
{
  "camera_id": 1,
  "video_id": 5,
  "frame_number": 120,
  "timestamp": "2026-11-11T12:00:00+03:00",
  "detections": [
    {"class": "person", "confidence": 0.91, "bbox": [100, 80, 320, 540]},
    {"class": "helmet", "confidence": 0.88, "bbox": [150, 80, 230, 150]}
  ]
}
```
Backend сопоставляет СИЗ с человеком (центр bbox внутри bbox человека) и сохраняет нарушение, если не хватает классов из `Zone.required_ppe`.

## Загрузка видео из консоли
```bash
python manage.py load_video path/to/video.mp4 --camera 1
```