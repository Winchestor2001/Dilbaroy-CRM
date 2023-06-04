from django.contrib import admin
from .models import *


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_price']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'pass_data', 'doctor', 'room', 'from_date']
    search_fields = ['full_name', 'pass_data', 'doctor', 'room']
    list_display_links = ['id', 'full_name']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['room_type']


@admin.register(RoomService)
class RoomServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'room_number', 'room_personal', 'room_patients', 'room_price', 'room_comfortable']

