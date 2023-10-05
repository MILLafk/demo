import requests
from django.conf import settings
from json.decoder import JSONDecodeError
from opencv.haar_cascade import (
    frame_extract,
    face_detect,
    # eye_detect,
)
from opencv.models import Image

REQUEST_URL = f"http://{settings.HOST}:8000/"


def process_vid(video):
    # Frame Extraction
    try:
        response = requests.post(
            REQUEST_URL + "opencv/extract/",
            json={"video": video.id},
        ).json()
        image_ids = response["images"]
    except JSONDecodeError:
        image_ids = frame_extract(video)
    # Face Detection
    frame_ids = []
    for image_id in image_ids:
        try:
            response = requests.post(
                REQUEST_URL + "opencv/face/",
                json={"image": image_id},
            ).json()
            frame_ids.append(response["frame"])
        except JSONDecodeError:
            image = Image.objects.get(id=image_id)
            frame_id = face_detect(image)
            frame_ids.append(frame_id)

    # TODO: Eye Detection
    target_ids = []

    return {
        "video": video.id,
        "images": image_ids,
        "frames": frame_ids,
        "targets": target_ids,
    }
