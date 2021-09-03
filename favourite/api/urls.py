from django.urls import path,include
from . import views
app_name='favourite'

urlpatterns = [
    path('list-create',views.FavouriteListCreateAPIView.as_view(),name='list-create'),
    path('update-delete/<pk>',views.FavouriteAPIView.as_view(),name='update-delete'),
]
