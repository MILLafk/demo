from rest_framework import serializers
from opencv.models import (
    Video,
    # Frame,
    Image,
)


class VideoSerializers(serializers.ModelSerializer):
    file = serializers.FileField(max_length=500)
    

    class Meta:
        model = Video
        fields = ["id", "file", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ImageSerializers(serializers.ModelSerializer):
    file = serializers.FileField(max_length=500)
    

    class Meta:
        model = Image
        fields = ["id", "file", "user", "video"]
        read_only_fields = ["user"]


    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class FrameExtractionSerializers(serializers.Serializer):
    #video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())
    video_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        video_id = validated_data["video_id"]
        return video_id


class FaceDetectionSerializers(serializers.Serializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    def create(self, validated_data):
        image = validated_data["image"]
        return image


# TODO: Create EyeDetectionSerializers
# class EyeDetectionSerializers(serializers.Serializer):


class ProcessVideoSerializers(serializers.Serializer):
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    def create(self, validated_data):
        video = validated_data["video"]
        return video
