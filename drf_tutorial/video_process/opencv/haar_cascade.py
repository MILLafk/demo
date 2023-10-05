import os
import cv2
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from opencv.models import Image, Frame, Target


face_cascade = cv2.CascadeClassifier(
    "/home/catchall/Desktop/workshop/drf_tutorial/video_process/opencv/classifiers/haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    "/home/catchall/Desktop/workshop/drf_tutorial/video_process/opencv/classifiers/haarcascade_eye.xml"
)


def frame_extract(video_instance):
    images = []
    video_file = os.path.join(settings.MEDIA_ROOT, str(video_instance.file))
    cap = cv2.VideoCapture(video_file)
    frame_no = 1
    while True:
        # reading frame from the video source
        ret, frame = cap.read()
        if ret:
            if frame_no % 50 == 9:
                frame = cv2.resize(frame, (960, 540))
                _, buffer = cv2.imencode(".jpg", frame)
                content = ContentFile(BytesIO(buffer).getvalue())
                image_data = {"user": video_instance.user, "video": video_instance}
                image = Image.objects.create(**image_data)
                image.file.save(
                    f"face{video_instance.id}_{image.id}.jpg", content, save=True
                )
                images.append(image.id)
                print(f"Extracted image id: {image.id}")
            frame_no += 1
        else:
            break
    cap.release()
    return images


def face_detect(image_instance):
    image_file = os.path.join(settings.MEDIA_ROOT, str(image_instance.file))
    cv2_image = cv2.imread(image_file)

    # cinverting frame to Gray scale to pass on classifier
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

    # detect faces and return coordinates of rectangle
    # This is the section, where you need to work
    # To get more accurate result, you need to play with this parameters
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)
    face_list = []
    for (x, y, w, h) in faces:
        cv2.rectangle(cv2_image, (x, y), (x + w, y + h), (255, 0, 0), 1)
        face_list.append([x, y, w, h])

    # save video frame data to Frame model
    if face_list:
        height, width, channel = cv2_image.shape
        _, buffer = cv2.imencode(".jpg", cv2_image)
        content = ContentFile(BytesIO(buffer).getvalue())
        frame_data = {
            "width": width,
            "height": height,
            "channel": channel,
            "bboxes": face_list,
            "image": image_instance,
        }
        frame = Frame.objects.create(**frame_data)
        frame.file.save(f"face{image_instance.id}_{frame.id}.jpg", content, save=True)
        print(f"Face Detected frame id: {frame.id}")
    return frame.id


def eye_detect(frame_instance):
    targets = []
    frame_file = os.path.join(settings.MEDIA_ROOT, str(frame_instance.file))
    frame = cv2.imread(frame_file)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for (x, y, w, h) in frame_instance.bboxes:
        roi_gray = gray[y : y + h, x : x + w]
        roi_gray = cv2.resize(roi_gray, (216, 216))
        roi_color = frame[y : y + h, x : x + w]
        roi_color = cv2.resize(roi_color, (216, 216))
        eyes = eye_cascade.detectMultiScale(roi_gray)
        eyes_list = []
        for (ex, ey, ew, eh) in eyes:
            eyes_list.append([ex, ey, ew, eh])
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        height, width, _ = roi_color.shape
        _, buffer = cv2.imencode(".jpg", roi_color)
        content = ContentFile(BytesIO(buffer).getvalue())
        target_data = {
            "width": width,
            "height": height,
            "bboxes": eyes_list,
            "frame": frame_instance,
        }
        target = Target.objects.create(**target_data)
        target.file.save(f"eyes{frame_instance.id}_{target.id}.jpg", content, save=True)
        targets.append(target.id)
        print(f"Eye Detected target id: {target.id}")
    return targets
