from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('settings/', views.settings, name="settings"),
    path("file_upload/", views.file_upload, name="file_upload"),
    path('delete/<str:id>/', views.delete_file, name="delete_file")
]