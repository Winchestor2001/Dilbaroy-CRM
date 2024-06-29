from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.HomeAPI.as_view()),
    path('register/', views.RegisterPatientAPI.as_view()),
    path('doctor/', views.DoctorAPI.as_view()),
    path('xizmatlar/', views.ServiceAPI.as_view()),
    path('xonalar/', views.RoomAPI.as_view()),
    path('bemor/<int:pk>/', views.PatientAPI.as_view()),
    path('doctor_statistics/', views.DoctorStatisticsAPI.as_view()),
    path('patient_statistics/', views.PatientStatisticsAPI.as_view()),
    path('room_statistics/', views.RoomStatisticsAPI.as_view()),
    path('room_services/', views.RoomServiceAPI.as_view()),
    path('close_room/', views.PatientRoomEndAPI.as_view()),

    path('auth/', include("djoser.urls")),
    re_path(r'^auth/', include("djoser.urls.authtoken")),
]
