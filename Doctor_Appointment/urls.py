from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('register/',views.Register),
    path('login/',views.UserLogin),
    path('doctor/add_slot/',views.add_slot),
    path('doctor/slot_list/',views.slot_list),
    path('doctor/slot_delete/<int:id>/',views.slot_delete),
    path('doctor/slot_update/<int:id>/',views.slot_update)
]