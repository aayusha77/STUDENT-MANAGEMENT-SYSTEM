from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/update/<int:id>/', views.update_student, name='update_student'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
]
