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
    serializer = AddDoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def doctor_delete(request,id):
    try:
        doctor = Doctor_Details.objects.get(id=id)
        doctor.delete()
        return Response({'message':'deleted doctor successfully'})
    except doctor.DoesNotExist:
        return Response({'message':'Data does not exist'})
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def doctors_list(request):
    doctor = Doctor_Details.objects.all()
    serializer = AddDoctorSerializer(doctor,many=True)
    return Response(serializer.data)