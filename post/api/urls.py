from django.views.decorators.cache import cache_page
from django.urls import path, include
from . import views

app_name = 'post'
urlpatterns = [
    path('list',cache_page(60*1)(views.PostListApiView.as_view()), name='list'),
    path('detail/<slug>', views.PostDetailApiView.as_view(), name='detail'),
    # path('delete/<slug>', views.PostDeleteApiView.as_view(), name='delete'), combined to update
    path('update/<slug>', views.PostUpdateApiView.as_view(), name='update'),
    path('create', views.PostCreateApiView.as_view(), name='create'),
]
