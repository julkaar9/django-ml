from django.contrib import admin
from django.http import StreamingHttpResponse
from django.urls import path

from apps.comviz.videoMiddleware import VideoCamera, gen

app_name = 'comviz'

urlpatterns = [
    path('monitor/', lambda r: StreamingHttpResponse(gen(VideoCamera()),
                                                     content_type='multipart/x-mixed-replace; boundary=frame')),
]