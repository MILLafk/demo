from django.contrib import admin
from .models import Video, Image, Frame, Target

# Register your models here.
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Frame)
admin.site.register(Target)
