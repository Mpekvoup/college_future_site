from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('student/create_student/', views.create_student, name="create_student"),
    path('student/delete_student/<int:id>/', views.delete_student, name="delete_student"),
    path("register/",views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
