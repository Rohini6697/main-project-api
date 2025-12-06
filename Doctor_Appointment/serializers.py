from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AvailableSlot, MedicalNotes, Prescription, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required = True)
    age = serializers.IntegerField(required = True)
    gender = serializers.CharField(required = True)
    role = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ('username','email','password','phone','age','gender','role')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self,validated_data):
        phone = validated_data.pop('phone')
        age = validated_data.pop('age')
        gender = validated_data.pop('gender')
        role = validated_data.pop('role')


        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        UserProfile.objects.create(user=user,phone=phone,age=age,gender=gender,role=role)
        return user
    
# ======================================= DOCTOR==============================================


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = '__all__'

class MedicalNoteserializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalNotes
        fields = '__all__'

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user
        return super().create(validated_data)

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields='__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['doctor'] = user
        return super().create(validated_data)