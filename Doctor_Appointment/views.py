from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import AvailableSlot, Doctor_Details, MedicalNotes, UserProfile
from .serializers import AddDoctorSerializer, MedicalNoteserializer, PrescriptionSerializer, RegisterSerializer, SlotSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User


@api_view(['POST'])
def Register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # refresh = RefreshToken.for_user(user)

        return Response({
            "user_id":user.id,
            "username":user.username,
            "email":user.email,
            "role":user.userprofile.role,
            # "refresh_token": str(refresh)

        })
    return Response(serializer.errors)

@api_view(['POST'])
def UserLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)
    if user.is_superuser:
        return Response({
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "username": user.username,
            "role": "admin"
        })
    if user is None:
        return Response({'error':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh_token":str(refresh),
        "access_token":str(refresh.access_token),
        "username" : user.username,
        "role": user.userprofile.role
    })


# ======================================= DOCTOR ==============================================

# SLOT CREATION BY DOCTOR

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_slot(request):
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user = request.user)
        return Response(serializer.data)
    return Response(serializer.errors,status=404)

# SLOT LISTING BY DOCTOR

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def slot_list(request):
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    slots = AvailableSlot.objects.all()
    serializer = SlotSerializer(slots,many=True)
    return Response(serializer.data)

# SLOT DELETION BY DOCTOR

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def slot_delete(request,id):
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    try:
        slot = AvailableSlot.objects.get(id=id)
        slot.delete()
        return Response({"message":"Successfully deleted"})
    except slot.DoesNotExist():
        return Response({"message":"Slot not Found"},status=404)
    
# SLOT UPDATION BY DOCTOR

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def slot_update(request,id):
    slot = AvailableSlot.objects.get(id =id)
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    serializer = SlotSerializer(instance = slot ,data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

# MEDICAL NOTES CREATION BY DOCTOR

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def medical_note_create(request):
    serializer = MedicalNoteserializer(data = request.data, context={'request': request})
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

# MEDICAL NOTES LISTING BY DOCTOR

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medical_note_list(request):
    medical_note = MedicalNotes.objects.all()
    serializer = MedicalNoteserializer(instance = medical_note, many = True, context={'request': request})
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    return Response(serializer.data)   

# MEDICAL NOTES DELETION BY DOCTOR

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def medical_note_delete(request,id):
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    try:
        medical_note = MedicalNotes.objects.get(id=id)
        medical_note.delete()
        return Response({'message':'Medical Note Deleted Successfully'})
    except medical_note.DoesNotExist:
        return Response({'message':'Medical Not Found'},status=404)
    
# MEDICAL NOTES UPDATION BY DOCTOR

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def medical_note_update(request,id):
    medical_note = MedicalNotes.objects.get(id=id)
    serializer = MedicalNoteserializer(instance =medical_note,data = request.data, context={'request': request})
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=400)

#  PRESCRIPTION UPLOADED BY DOCTOR

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prescription_upload(request):
    try:
        profile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        return Response({'message':'Profile not found'},status=404)
    if profile.role != 'doctor':
        return Response({'message':'You cant access this'})
    serializer = PrescriptionSerializer(data = request.data,context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=400)

# ======================================= ADMIN ==============================================

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_doctor(request):

    # step 1: create USER
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists!"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=request.data.get('password'),
        email=request.data.get('email')
    )

    # step 2: create USER PROFILE (doctor role)
    profile = UserProfile.objects.create(
        user=user,
        phone=request.data.get('phone'),
        age=request.data.get('age'),
        gender=request.data.get('gender'),
        role="doctor"
    )

    # step 3: create DOCTOR DETAILS
    Doctor_Details.objects.create(
        doctor=profile,
        specialization=request.data.get('specialization'),
        experience=request.data.get('experience'),
        qualification=request.data.get('qualification')
    )

    return Response({"message": "Doctor added successfully"})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def doctor_delete(request,id):
    try:
        doctor = Doctor_Details.objects.get(id=id)
        doctor.delete()
        return Response({'message':'deleted doctor successfully'})
    except doctor.DoesNotExist:
        return Response({'message':'Data does not exist'},status=404)
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def doctors_list(request):
    doctor = Doctor_Details.objects.all()
    serializer = AddDoctorSerializer(doctor,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def doctor_update(request, id):
    doctor_details = Doctor_Details.objects.get(id=id)
    profile = doctor_details.doctor      # UserProfile model
    user = profile.user                  # User model

    data = request.data

    # --------------------
    # UPDATE User FIELDS
    # --------------------
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.save()

    # --------------------
    # UPDATE UserProfile FIELDS
    # --------------------
    profile.phone = data.get("phone", profile.phone)
    profile.age = data.get("age", profile.age)
    profile.gender = data.get("gender", profile.gender)
    profile.role = data.get("role", profile.role)
    profile.save()

    # --------------------
    # UPDATE Doctor_Details FIELDS
    # --------------------
    doctor_details.specialization = data.get("specialization", doctor_details.specialization)
    doctor_details.experience = data.get("experience", doctor_details.experience)
    doctor_details.qualification = data.get("qualification", doctor_details.qualification)
    doctor_details.save()

    # Serializer only for output
    serializer = AddDoctorSerializer(doctor_details)
    return Response(serializer.data)

# ======================================= PATIENT ==============================================

@api_view(['GET'])
def patient_slot_list(request):
    slots = AvailableSlot.objects.all()
    serializer = SlotSerializer(slots,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_dept_doctor(request):
    doctors = Doctor_Details.objects.all()

    data = []
    for d in doctors:
        data.append({
            "username": d.doctor.user.username,
            "specialization": d.specialization
        })

    return Response(data)

import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Appointment
from rest_framework import status
import razorpay
import qrcode
import os
from django.conf import settings


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


from rest_framework.decorators import api_view
from rest_framework.response import Response
import razorpay
import qrcode
import base64
from io import BytesIO

@api_view(['POST'])
def book_appointment(request):
    user_id = request.data.get("user")
    doctor_id = request.data.get("doctor")
    amount = request.data.get("amount")

    if not user_id or not doctor_id or not amount:
        return Response({"error": "user, doctor, amount required"}, status=400)

    user = User.objects.get(id=user_id)
    doctor = Doctor_Details.objects.get(id=doctor_id)

    appointment = Appointment.objects.create(
        user=user,
        doctor=doctor,
    )

    # Razorpay order
    order = client.order.create({
        "amount": int(amount) * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    order_id = order["id"]

    # Razorpay payment link
    link = client.payment_link.create({
        "amount": int(amount) * 100,
        "currency": "INR",
        "reference_id": order_id,
        "description": f"Payment for appointment",
        "callback_url": "https://your-backend.com/payment/verify/",
        "callback_method": "get"
    })

    payment_url = link["short_url"]

    return Response({
        "appointment_id": appointment.id,
        "payment_url": payment_url,
        "order_id": order_id
    })
