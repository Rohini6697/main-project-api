from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    ROLL_CHOICES = (
        ('patient','Patient'),
        ('doctor','Doctor'),
        ('admin','Admin')
    )
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    phone = models.CharField(max_length=20,null=False,blank=False)
    age = models.PositiveIntegerField(null=False,blank=False)
    gender = models.CharField(max_length=20,null=False,blank=False)
    role = models.CharField(max_length=20,choices=ROLL_CHOICES,default='patient')

    def __str__(self):
        return f"{self.user.username} {self.role}"