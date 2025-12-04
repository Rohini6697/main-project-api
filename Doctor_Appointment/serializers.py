from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile



class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required = True)
    age = serializers.IntegerField(required = True)
    gender = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ('username','email','password','phone','age','gender')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self,validated_data):
        phone = validated_data.pop('phone')
        age = validated_data.pop('age')
        gender = validated_data.pop('gender')


        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        UserProfile.objects.create(user=user,phone=phone,age=age,gender=gender)
        return user