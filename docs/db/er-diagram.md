# ER-диаграмма БД (PPE Monitor)

Приложение Django `monitoring`, СУБД PostgreSQL 16.

```mermaid
erDiagram
    CAMERA ||--o{ ZONE : has
    CAMERA ||--o{ VIDEO_FILE : records
    CAMERA ||--o{ FRAME : produces
    CAMERA ||--o{ VIOLATION : "detected on"
    ZONE ||--o{ PPE_RULE : requires
    ZONE ||--o{ VIOLATION : "occurred in"
    VIDEO_FILE ||--o{ FRAME : contains
    VIDEO_FILE ||--o{ VIOLATION : "found in"
    FRAME ||--o{ VIOLATION : "evidence for"
    EMPLOYEE ||--o{ VIOLATION : commits

    CAMERA {
        bigint id PK
        varchar name
        varchar source_type "file | rtp"
        varchar source_uri
        varchar location
        bool is_active
        timestamptz created_at
    }
    ZONE {
        bigint id PK
        bigint camera_id FK
        varchar name
        jsonb required_ppe "legacy, см. PPE_RULE"
        bool is_active
    }
    EMPLOYEE {
        bigint id PK
        varchar full_name
        varchar personnel_number "idx"
        varchar position
        varchar department
        varchar external_id UK "ID в СКУД, nullable"
        bool is_active
        timestamptz created_at
        timestamptz updated_at
    }
    PPE_RULE {
        bigint id PK
        bigint zone_id FK
        varchar ppe_class "helmet|gloves|vest|goggles|mask|boots"
        bool is_required
        float min_confidence "0..1"
        bool is_active
        timestamptz created_at
    }
    VIDEO_FILE {
        bigint id PK
        bigint camera_id FK "nullable"
        varchar file
        varchar original_name
        bigint size_bytes
        float duration_sec
        float fps
        int frame_count
        int width
        int height
        timestamptz uploaded_at
    }
    FRAME {
        bigint id PK
        bigint camera_id FK
        bigint video_id FK "nullable (RTP)"
        int frame_number
        timestamptz timestamp "idx"
        int width
        int height
        varchar image "снапшот, optional"
        jsonb detections "сырые детекции ML"
        int persons_count
        timestamptz created_at
    }
    VIOLATION {
        bigint id PK
        bigint camera_id FK
        bigint zone_id FK "nullable"
        bigint video_id FK "nullable"
        bigint frame_id FK "nullable"
        bigint employee_id FK "nullable"
        jsonb missing_ppe
        int frame_number
        timestamptz timestamp "idx"
        float bbox_x1
        float bbox_y1
        float bbox_x2
        float bbox_y2
        float confidence "0..1"
        varchar external_id "idx"
        timestamptz created_at
    }
```

## Индексы и ограничения

| Таблица | Индекс / ограничение | Зачем |
|---|---|---|
| `monitoring_violation` | `timestamp`, `(camera_id, timestamp DESC)`, `(zone_id, timestamp DESC)`, `(employee_id, timestamp DESC)` | фильтры журнала нарушений по времени, камере, зоне, сотруднику |
| `monitoring_violation` | `CHECK 0 <= confidence <= 1` | валидность score от ML |
| `monitoring_frame` | `timestamp`, `(camera_id, timestamp DESC)` | выборка кадров по камере и времени |
| `monitoring_frame` | `UNIQUE (video_id, frame_number)` при `video_id`/`frame_number` NOT NULL | нет дублей кадров одного видео; для RTP (`video_id IS NULL`) не действует |
| `monitoring_ppe_rule` | `UNIQUE (zone_id, ppe_class)`, `CHECK 0 <= min_confidence <= 1` | одно правило на класс СИЗ в зоне |
| `monitoring_employee` | `UNIQUE external_id` (NULL допускается многократно), индекс `personnel_number` | сопоставление с СКУД |

## Интеграция со СКУД

`Employee.external_id` — идентификатор сотрудника во внешней СКУД (номер пропуска/карты).
Поле nullable и уникальное: сотрудники заводятся до интеграции без него, а при синхронизации
сопоставляются по `external_id`. `Violation.employee` заполняется, когда нарушителя удаётся
идентифицировать (СКУД / распознавание), иначе остаётся `NULL`.

## Миграции

| Файл | Что делает |
|---|---|
| `0001_initial` | Camera, Zone, VideoFile, Violation (ветка backend) |
| `0002_employees_ppe_rules_frames` | Employee, PPE_Rules, Frames; `Violation.frame`, `Violation.employee`; индексы и ограничения |
| `0003_fill_ppe_rules_from_zones` | data-миграция: переносит `Zone.required_ppe` в PPE_Rules |

```bash
cd backend
python manage.py migrate                 # применить
python manage.py migrate monitoring 0001 # откатить изменения этой ветки
```
