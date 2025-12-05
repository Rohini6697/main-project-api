from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import AvailableSlot
from .serializers import RegisterSerializer, SlotSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view 
@api_view(['POST'])
def Register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "user_id":user.id,
            "username":user.username,
            "email":user.email,
            "role":user.userprofile.role,
            "refresh_token": str(refresh)

        })
    return Response(serializer.errors)

@api_view(['POST'])
def UserLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)
    if user is None:
        return Response({'error':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh_token":str(refresh),
        "access_token":str(refresh.access_token),
        "username" : user.username,
        "role": user.userprofile.role
    })
@api_view(['POST'])
def add_slot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=404)
@api_view(['GET'])
def slot_list(request):
    slots = AvailableSlot.objects.all()
    serializer = SlotSerializer(slots,many=True)
    return Response(serializer.data)
@api_view(['DELETE'])
def slot_delete(request,id):
    try:
        slot = AvailableSlot.objects.get(id=id)
        slot.delete()
        return Response({"message":"Successfully deleted"})
    except slot.DoesNotExist():
        return Response({"message":"Slot not Found"},status=404)
    
@api_view(['PUT'])
def slot_update(request,id):
    slot = AvailableSlot.objects.get(id =id)
    serializer = SlotSerializer(instance = slot ,data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)