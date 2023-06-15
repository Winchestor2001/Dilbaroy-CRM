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

    def get_rooms(self, obj):
        i = RoomsSerializer(data=obj.room_set.all(), many=True)
        i.is_valid()
        return i.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['rooms'] = self.get_rooms(instance)
        return ret


class RoomTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['room_type']


class RoomsSerializer(serializers.ModelSerializer):
    room_type = RoomTypesSerializer()
    class Meta:
        model = Room
        fields = '__all__'


class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorPatientSerializer(serializers.ModelSerializer):
    room = RoomsSerializer()
    service = ServiceSerializer(many=True)

    class Meta:
        model = Patient
        exclude = ('doctor',)


class DoctorsStatisticsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.from_date = kwargs.pop('from_date', None)
        self.to_date = kwargs.pop('to_date', None)
        super(DoctorsStatisticsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Doctor
        fields = '__all__'

    def get_patients(self, obj):
        patients = obj.patient_set.all()
        if self.from_date and self.to_date:
            if self.from_date == self.to_date:
                patients = obj.patient_set.filter(from_date=self.from_date).order_by('-created_date')
            else:
                patients = obj.patient_set.filter(from_date__range=[self.from_date, self.to_date]).order_by(
                    '-created_date')
        i = DoctorPatientSerializer(data=patients, many=True)
        i.is_valid()
        return i.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['patients'] = self.get_patients(instance)
        return ret


class PatientSerializer(serializers.ModelSerializer):
    room = RoomsSerializer()
    service = ServiceSerializer(many=True)
    doctor = DoctorsSerializer()

    class Meta:
        model = Patient
        fields = '__all__'


class RoomServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomService
        fields = '__all__'


class RoomStatisticsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.from_date = kwargs.pop('from_date', None)
        self.to_date = kwargs.pop('to_date', None)
        super(RoomStatisticsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = RoomType
        fields = '__all__'

    def get_rooms(self, obj):
        rooms = obj.room_set.all()
        patients = []
        total_sum = 0
        for r in rooms:
            if self.from_date and self.to_date:
                if self.from_date == self.to_date:
                    p = r.patient_set.filter(created_date=self.from_date).order_by('-created_date')
                    if p:
                        total_sum += p[0].room.room_price * p[0].duration
                        for i in p:
                            patients.append(i)
                else:
                    p = r.patient_set.filter(created_date__range=[self.from_date, self.to_date]).order_by(
                        '-created_date')
                    if p:
                        total_sum += p[0].room.room_price * p[0].duration
                        for i in p:
                            patients.append(i)
        return len(patients), total_sum

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['patinets'] = self.get_rooms(instance)[0]
        ret['total_sum'] = self.get_rooms(instance)[1]
        return ret
