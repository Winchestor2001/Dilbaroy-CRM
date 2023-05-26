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


class RoomsSerializer(serializers.ModelSerializer):
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
                patients = obj.patient_set.filter(from_date__range=[self.from_date, self.to_date]).order_by('-created_date')
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

    # def update(self, instance, validated_data):
    #     print(instance)
    #     if 'duration' in validated_data:
    #         instance.duration = validated_data['duration']
    #     if 'food_amount' in validated_data:
    #         instance.food_amount = validated_data['food_amount']
    #     if 'food_duration' in validated_data:
    #         instance.food_duration = validated_data['food_duration']
    #     if 'food_refund' in validated_data:
    #         instance.food_refund = validated_data['food_refund']
    #     if 'room_refund' in validated_data:
    #         instance.room_refund = validated_data['room_refund']
    #     if 'total_refund' in validated_data:
    #         instance.total_refund = validated_data['total_refund']
    #     if 'total_amount' in validated_data:
    #         instance.total_amount = validated_data['total_amount']
    #     instance.room = instance.room
    #     instance.service = instance.service
    #     instance.doctor = instance.doctor
    #     instance.full_name = instance.full_name
    #     instance.phone_number = instance.phone_number
    #     instance.address = instance.address
    #
    #     instance.save()
    #     return instance


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'
