"""Этап 2: находим людей на видео (YOLOv8n) и сохраняем результат.

Что делает скрипт:
1. Открывает видеофайл (или все видео из папки).
2. На каждом кадре ищет людей нейросетью YOLOv8n.
3. Рисует рамки и сохраняет видео с рамками.
4. Пишет результаты в файл .jsonl (одна строка = один кадр).
5. Пишет в лог скорость работы и ошибки.

Запуск:
    python detect.py --source data/videos/light_close.mp4
    python detect.py --source data/videos          (все видео из папки)
    python detect.py --source data/videos/a.mp4 --show   (показывать окно)
"""
import argparse
import json
import logging
import time
from pathlib import Path

import cv2
import yaml
from ultralytics import YOLO

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}


def load_config(path):
    """Читаем настройки из config.yaml."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging(log_file):
    """Лог пишем и в файл, и на экран."""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def collect_videos(source):
    """Из пути делаем список видеофайлов (один файл или вся папка)."""
    source = Path(source)
    if source.is_file():
        return [source]
    if source.is_dir():
        return sorted(p for p in source.iterdir() if p.suffix.lower() in VIDEO_EXTENSIONS)
    return []


def process_video(video_path, model, cfg, show=False):
    """Обрабатываем одно видео от начала до конца."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logging.error("Не удалось открыть видео: %s", video_path)
        return

    fps_in = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    expected_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out_dir = Path(cfg["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    video_out = out_dir / f"{video_path.stem}_detected.mp4"
    json_out = out_dir / f"{video_path.stem}_detections.jsonl"

    writer = cv2.VideoWriter(
        str(video_out), cv2.VideoWriter_fourcc(*"mp4v"), fps_in, (width, height)
    )

    frame_id = 0
    total_people = 0
    infer_time = 0.0
    t_start = time.perf_counter()

    with open(json_out, "w", encoding="utf-8") as jf:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            # Нейросеть смотрит на кадр. classes=[0] значит "только люди".
            t0 = time.perf_counter()
            result = model.predict(
                frame,
                classes=[0],
                conf=cfg["conf"],
                iou=cfg["iou"],
                imgsz=cfg["imgsz"],
                verbose=False,
            )[0]
            infer_time += time.perf_counter() - t0

            # Достаём найденные рамки в нашем формате.
            detections = []
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append(
                    {
                        "class": model.names[int(box.cls[0])],
                        "bbox": [round(v, 1) for v in (x1, y1, x2, y2)],
                        "confidence": round(float(box.conf[0]), 3),
                    }
                )

            record = {
                "source": video_path.name,
                "frame_id": frame_id,
                "timestamp": round(frame_id / fps_in, 3),
                "detections": detections,
            }
            jf.write(json.dumps(record, ensure_ascii=False) + "\n")

            # Рисуем рамки и сохраняем кадр.
            annotated = result.plot()
            writer.write(annotated)

            if show:
                cv2.imshow("detect (q - выход)", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    logging.info("Остановлено пользователем")
                    break

            frame_id += 1
            total_people += len(detections)

    cap.release()
    writer.release()
    if show:
        cv2.destroyAllWindows()

    total_time = time.perf_counter() - t_start
    avg_fps = frame_id / total_time if total_time > 0 else 0.0
    ms_per_frame = (infer_time / frame_id * 1000) if frame_id else 0.0

    logging.info(
        "%s | кадров: %d из %d | средний FPS: %.1f | инференс: %.1f мс/кадр | "
        "найдено людей (всего): %d",
        video_path.name, frame_id, expected_frames, avg_fps, ms_per_frame, total_people,
    )
    if expected_frames and frame_id < expected_frames:
        logging.warning(
            "%s: обработано меньше кадров, чем ожидалось (%d из %d)",
            video_path.name, frame_id, expected_frames,
        )


def main():
    parser = argparse.ArgumentParser(description="Поиск людей на видео (YOLOv8n)")
    parser.add_argument("--source", required=True, help="видеофайл или папка с видео")
    parser.add_argument("--config", default="config.yaml", help="файл настроек")
    parser.add_argument("--show", action="store_true", help="показывать окно с видео")
    args = parser.parse_args()

    cfg = load_config(args.config)
    setup_logging(cfg["log_file"])

    videos = collect_videos(args.source)
    if not videos:
        logging.error("Видео не найдено по пути: %s", args.source)
        return

    logging.info("Загружаем модель %s", cfg["model"])
    model = YOLO(cfg["model"])  # при первом запуске веса скачаются сами

    for video in videos:
        process_video(video, model, cfg, show=args.show)


if __name__ == "__main__":
    main()
