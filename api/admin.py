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
    search_fields = ['full_name', 'pass_data']
    list_display_links = ['id', 'full_name']
    exclude = ['obj_status']

    def delete_model(self, request, obj):
        # Update obj_status to True instead of deleting the object
        obj.obj_status = True
        obj.save()

    def get_queryset(self, request):
        # Return only objects with obj_status set to False
        qs = super().get_queryset(request)
        return qs.filter(obj_status=False)

    def delete_queryset(self, request, queryset):
        # Update obj_status to True for all objects in the queryset
        queryset.update(obj_status=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_selected(self, request, queryset):
        # Update obj_status to True for all selected objects
        for obj in queryset:
            self.delete_model(request, obj)

    actions = ['delete_selected']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['room_type']


@admin.register(RoomService)
class RoomServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'room_number', 'room_personal', 'room_patients', 'room_price', 'room_comfortable']

