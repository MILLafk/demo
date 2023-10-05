from django.urls import include, path
from rest_framework.routers import DefaultRouter
from opencv.views import (
    VideoUploadViewSet,
    FaceDetectViewSet,
    ImageUploadViewSet,
    FrameExtractViewSet,
    ProcessVideoViewSet,
    MyView,
)

router = DefaultRouter()
router.register("opencv/video", VideoUploadViewSet, basename="opencv-video")
router.register("opencv/extract", FrameExtractViewSet, basename="opencv-extract")
router.register("opencv/image", ImageUploadViewSet, basename="opencv-image")
router.register("opencv/face", FaceDetectViewSet, basename="opencv-face")
# TODO: create url for Eye Detection
router.register("opencv/process", ProcessVideoViewSet, basename="opencv-process")
# router.register("opencv/my_page", MyView, basename="opencv-mypage")

urlpatterns = [
    path('', include(router.urls)),
    path('my-url/', MyView.as_view(), name='my-view'),
]
