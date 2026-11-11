import cv2


def extract_video_metadata(path) -> dict:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("Не удалось открыть видеофайл")
    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    return {
        "fps": fps or None,
        "frame_count": frames or None,
        "width": width or None,
        "height": height or None,
        "duration_sec": round(frames / fps, 2) if fps and frames else None,
    }


def _center_inside(box, person) -> bool:
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    return person[0] <= cx <= person[2] and person[1] <= cy <= person[3]


def find_missing_ppe(person_bbox, ppe_detections, required) -> list:
    present = {d["class"] for d in ppe_detections if _center_inside(d["bbox"], person_bbox)}
    return [r for r in required if r not in present]