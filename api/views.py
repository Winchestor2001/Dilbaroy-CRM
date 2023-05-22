from datetime import datetime

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .models import *
from .utils import text_to_slug
from .serializers import *


class HomeAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        context = [
            {
                'company': "Dilbaroy Clinik"
            }
        ]
        return Response({'status': '(403) Permission denied', 'context': context}, status=403)


class RegisterPatientAPI(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(data=patients, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)

    def post(self, request):
        doctor = request.data['doctor']
        services = request.data['services']
        full_name = request.data['full_name']
        pass_data = request.data['pass_data']
        phone_number = request.data['phone_number']
        address = request.data['address']
        workplace = request.data['workplace']
        birthday = datetime.strptime(request.data['birthday'], '%Y-%m-%d')
        room_number = request.data['room_number']
        duration = request.data['duration']
        food = request.data['food']
        food_duration = request.data['food_duration']
        from_date = request.data['from_date']
        total_amount = request.data['total_amount']
        doctor = Doctor.objects.get(pk=doctor)
        patient = Patient.objects.create(
            slug_name=text_to_slug(full_name),
            doctor=doctor, full_name=full_name, pass_data=pass_data,
            phone_number=phone_number, address=address, workplace=workplace, birthday=birthday,
            food=food, food_duration=food_duration, from_date=from_date, total_amount=total_amount
        )

        room = Room.objects.get(pk=room_number)
        patient.room = room
        patient.duration = duration
        room.room_personal -= 1
        room.save()

        if len(services) > 0:
            for t in services:
                patient.service.add(t)

        patient.save()
        return Response({'status': 'OK'})


class DoctorAPI(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorsSerializer(data=doctors, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class ServiceAPI(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(data=services, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class RoomAPI(APIView):
    def get(self, request):
        room_types = RoomType.objects.all()
        serializer = RoomTypeSerializer(data=room_types, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class PatientAPI(APIView):
    def get(self, request, pk):
        patient = Patient.objects.filter(pk=pk)
        serializer = PatientSerializer(data=patient, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)
