from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('register/',views.Register),
    path('login/',views.UserLogin),
    
# ======================================= DOCTOR ==============================================

    path('doctor/add_slot/',views.add_slot),
    path('doctor/slot_list/',views.slot_list),
    path('doctor/slot_delete/<int:id>/',views.slot_delete),
    path('doctor/slot_update/<int:id>/',views.slot_update),
    path('medical_note_create/',views.medical_note_create),
    path('medical_note_list/',views.medical_note_list),
    path('medical_note_delete/<int:id>/',views.medical_note_delete),
    path('medical_note_update/<int:id>/',views.medical_note_update),

# ======================================= PATIENT ==============================================


# ======================================= ADMIN ==============================================


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
