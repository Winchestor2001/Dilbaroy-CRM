from django.contrib import admin
from .models import *


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    search_fields = ['full_name']


@admin.register(Service)
class MainServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_price']


@admin.register(Doctor)
class MainServiceAdmin(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'pass_data', 'doctor', 'room', 'from_date']
    search_fields = ['full_name', 'pass_data', 'doctor', 'room']


@admin.register(RoomType)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['room_type']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'room_number', 'room_personal', 'room_price', 'room_comfortable']

