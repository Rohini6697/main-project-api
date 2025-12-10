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
    path('prescription_upload/',views.prescription_upload),
    path('doctor/doctor_appointment_list',views.doctor_appointment_list),
    path('doctor_update_status/<int:appointment_id>',views.doctor_update_status),

# ======================================= PATIENT ==============================================

    path('patient/list_dept_doctor',views.list_dept_doctor),
    path('patient/patient_slot_list/',views.patient_slot_list),
    path('patient/list_dept_doctor/',views.list_dept_doctor),
    path("book_appointment/", views.book_appointment),
    path("patient/appointment_list",views.appointment_list),
    path('patient/payment_verify/',views.payment_verify),


# ======================================= ADMIN ==============================================
    path('add_doctor/',views.add_doctor),
    path('doctors_list/',views.doctors_list),
    path('doctor_delete/<int:id>/',views.doctor_delete),
    path('doctor_update/<int:id>/',views.doctor_update),
    path('admin_appointment_list/',views.admin_appointment_list)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
