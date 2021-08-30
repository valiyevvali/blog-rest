
from django.contrib import admin
from django.urls import path,include
from .views import PostListApiView
urlpatterns = [
    path('list', PostListApiView.as_view(),name='list'),
]
