from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import RegisterSerializer
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