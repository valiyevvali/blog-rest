
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('list', views.PostListApiView.as_view(),name='list'),
    path('detail/<slug>', views.PostDetailApiView.as_view(),name='detail'),
    path('delete/<slug>', views.PostDeleteApiView.as_view(),name='delete'),
    path('update/<slug>', views.PostUpdateApiView.as_view(),name='update'),
]
