from rest_framework import serializers
from .models import *


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

    def get_analysis(self, obj):
        i = RoomsSerializer(data=obj.room_set.all(), many=True)
        i.is_valid()
        return i.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['rooms'] = self.get_analysis(instance)
        return ret


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    room = RoomsSerializer()
    service = ServiceSerializer(many=True)
    doctor = DoctorsSerializer()

    class Meta:
        model = Patient
        fields = '__all__'
