from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'home'),
    path('emp_reg',views.emp_reg,name = 'emp_reg'),
    path('emp_login',views.emp_login,name = 'emp_login'),
    path('emp_portal/cnic = <str:cnic>',views.emp_portal,name = 'emp_portal'),
    path('student_reg',views.student_reg,name = 'student_reg'),
    path('student_login',views.student_login,name = 'student_login'),
    path('student_portal/cnic = <str:cnic>',views.student_portal,name = 'student_portal'),
    path('logout/', views.logout_view, name='logout'),
    path('employee/logout/', views.employee_logout, name='employee_logout'),
] 