from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    ROLL_CHOICES = (
        ('patient','Patient'),
        ('doctor','Doctor'),
    )
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    phone = models.CharField(max_length=20,null=False,blank=False)
    age = models.PositiveIntegerField(null=False,blank=False)
    gender = models.CharField(max_length=20,null=False,blank=False)
    role = models.CharField(max_length=20,choices=ROLL_CHOICES,default='patient')

    def __str__(self):
        return f"{self.user.username} {self.role}"
    
# ======================================= DOCTOR ==============================================

class AvailableSlot(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    date = models.DateField()
    Time = models.TimeField()

    def __str__(self):
        return f"{self.date}"
    
class MedicalNotes(models.Model):
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient_notes')
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor_notes')
    # appointment = models.ForeignKey(AvailableSlot,on_delete=models.CASCADE)

    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.username}-{self.created_at}"
    
class Prescription(models.Model):
    patient = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='patient_prescription')
    doctor = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='doctor_prescription')
    files = models.FileField(upload_to='prescription/')
    description = models.CharField(max_length=500)
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.user.username}"

# ======================================= ADMIN ==============================================
class Doctor_Details(models.Model):
    doctor = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experiance = models.IntegerField()
    qualification = models.CharField()

    def __str__(self):
        return f"{self.doctor.user.username}-{self.doctor.role}"