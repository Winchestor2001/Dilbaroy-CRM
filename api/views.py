from datetime import datetime, timedelta

from django.db.models import Sum
from django.utils import timezone
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
    authentication_classes = [TokenAuthentication]

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
        birthday = datetime.strptime(request.data['birthday'], '%Y-%m-%d')
        room_number = request.data['room_number']
        duration = request.data['duration']

        food = request.data['food']
        food_amount = request.data['food_amount']
        food_duration = request.data['food_duration']

        massaj1 = request.data['massaj1']
        massaj1_amount = request.data['massaj1_amount']
        massaj1_duration = request.data['massaj1_duration']

        massaj2 = request.data['massaj2']
        massaj2_amount = request.data['massaj2_amount']
        massaj2_duration = request.data['massaj2_duration']

        from_date = request.data['from_date']
        total_amount = request.data['total_amount']
        room_amount = request.data['room_amount']
        doctor = Doctor.objects.get(pk=doctor)
        patient = Patient.objects.create(
            slug_name=text_to_slug(full_name),
            doctor=doctor, full_name=full_name, pass_data=pass_data,
            phone_number=phone_number, address=address, birthday=birthday,
            food=food, food_duration=food_duration, from_date=from_date, total_amount=total_amount,
            food_amount=food_amount, room_amount=room_amount,
            massaj1=massaj1, massaj1_amount=massaj1_amount, massaj1_duration=massaj1_duration,
            massaj2=massaj2, massaj2_amount=massaj2_amount, massaj2_duration=massaj2_duration,
        )

        room = Room.objects.get(pk=room_number)
        room.room_patients -= 1
        room.save()

        patient.room = room
        patient.duration = duration

        if len(services) > 0:
            for t in services:
                patient.service.add(t)

        patient.save()

        patient = Patient.objects.get(id=patient.id)
        serializer = PatientSerializer(instance=patient)

        return Response(serializer.data, status=201)


class DoctorAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorsSerializer(data=doctors, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class ServiceAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(data=services, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class RoomAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        room_types = RoomType.objects.all()
        serializer = RoomTypeSerializer(data=room_types, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class PatientAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        patient = Patient.objects.filter(pk=pk)
        serializer = PatientSerializer(data=patient, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)

    def put(self, request, pk):
        room_duration = request.data.get('room_duration')
        room_refund = request.data.get('room_refund')
        room_amount = request.data.get('room_amount')

        massaj1_duration = request.data.get('massaj1_duration')
        massaj1_refund = request.data.get('massaj1_refund')
        massaj1_amount = request.data.get('massaj1_amount')

        massaj2_duration = request.data.get('massaj2_duration')
        massaj2_refund = request.data.get('massaj2_refund')
        massaj2_amount = request.data.get('massaj2_amount')

        food_duration = request.data.get('food_duration')
        food_refund = request.data.get('food_refund')
        food_amount = request.data.get('food_amount')

        total_amount = request.data.get('total_amount')
        total_refund = request.data.get('total_refund')
        patient = Patient.objects.get(pk=pk)
        patient.duration = room_duration
        patient.room_refund = room_refund
        patient.room_amount = room_amount

        patient.food_duration = food_duration
        patient.food_refund = food_refund
        patient.food_amount = food_amount

        patient.massaj1_duration = massaj1_duration
        patient.massaj1_refund = massaj1_refund
        patient.massaj1_amount = massaj1_amount

        patient.massaj2_duration = massaj2_duration
        patient.massaj2_refund = massaj2_refund
        patient.massaj2_amount = massaj2_amount

        patient.total_amount = total_amount
        patient.total_refund = total_refund
        patient.save()

        ser_patient = Patient.objects.filter(pk=pk)

        serializer = PatientSerializer(data=ser_patient, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class DoctorStatisticsAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        from_date = timezone.make_aware(datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d'))
        to_date = timezone.make_aware(datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d') + timedelta(days=1))
        doctors = Doctor.objects.all()
        serializer = DoctorsStatisticsSerializer(data=doctors, many=True, from_date=from_date, to_date=to_date)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class PatientStatisticsAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        from_date = timezone.make_aware(datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d'))
        to_date = timezone.make_aware(datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d') + timedelta(days=1))
        patients = Patient.objects.all()
        if from_date and to_date:
            if from_date == to_date:
                patients = Patient.objects.filter(from_date=from_date).order_by('-from_date')
            else:
                patients = Patient.objects.filter(from_date__range=[from_date, to_date]).order_by('-from_date')
        serializer = PatientSerializer(data=patients, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class RoomServiceAPI(APIView):
    def get(self, request):
        food = RoomService.objects.all()
        serializer = RoomServiceSerializer(data=food, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class RoomStatisticsAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        from_date = timezone.make_aware(datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d'))
        to_date = timezone.make_aware(datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d') + timedelta(days=1))
        rooms = RoomType.objects.all()
        serializer = RoomStatisticsSerializer(data=rooms, many=True, from_date=from_date, to_date=to_date)
        serializer.is_valid()
        return Response(serializer.data, status=200)


class PatientRoomEndAPI(APIView):
    def post(self, request):
        patient_id = request.data.get('patient_id')
        patient = Patient.objects.get(pk=patient_id)
        patient.room_status = True
        room = Room.objects.get(id=patient.room.id)
        room.room_patients += 1
        room.save()
        patient.save()
        serializer = PatientSerializer(instance=patient)
        return Response(serializer.data, status=200)
