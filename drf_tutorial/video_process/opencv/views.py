from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from opencv.serializers import (
    VideoSerializers,
    FaceDetectionSerializers,
    ImageSerializers,
    FrameExtractionSerializers,
    ProcessVideoSerializers,
)
from opencv.models import Video, Image
from opencv.haar_cascade import (
    # eye_detect,
    face_detect,
    frame_extract,
)
from opencv.process import process_vid



# Create your views here.


class MyView(View):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        videos = Video.objects.filter(user=request.user)
        context = {'users': users, 'videos': videos}
        return render(request, 'index.html', context)
    
    
class VideoUploadViewSet(viewsets.ModelViewSet):
    """
    Uploads a File
    """

    queryset = Video.objects.all()
    serializer_class = VideoSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
class ImageUploadViewSet(viewsets.ModelViewSet):
    """
    Uploads a File
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FrameExtractViewSet(viewsets.ViewSet):
    """
    Frame Extraction
    """

    serializer_class = FrameExtractionSerializers

    def create(self, request):
        serializer = FrameExtractionSerializers(data=request.data)
        if serializer.is_valid():
            video_id = serializer.validated_data['video_id']
            try:
                video = Video.objects.get(id=video_id, user=request.user)
            except Video.DoesNotExist:
                return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

            images = frame_extract(video)
            context = {"video": video.id, "images": images}
            return Response(context, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FaceDetectViewSet(viewsets.ViewSet):
    """
    Face Detection
    """

    serializer_class = FaceDetectionSerializers

    def create(self, request):
        serializer = FaceDetectionSerializers(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            frame_id = face_detect(image)
            context = {"image": image.id, "frame": frame_id}
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: Create Viewset for Eye Detection
# class EyeDetectViewSet(viewsets.ViewSet):


class ProcessVideoViewSet(viewsets.ViewSet):
    """
    Perform Face and Eye Detection in Videos
    """

    serializer_class = ProcessVideoSerializers

    def create(self, request):
        serializer = ProcessVideoSerializers(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            context = process_vid(video)
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
