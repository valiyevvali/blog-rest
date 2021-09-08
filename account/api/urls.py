from django.urls import path,include
from . import views
app_name='account'

urlpatterns = [
    path('me',views.ProfileView.as_view(),name='me'),
    path('change_password',views.UpdatePasswordView.as_view(),name='change_password'),
    path('register', views.CreateUserView.as_view(), name='register'),
]
