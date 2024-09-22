from django.urls import path
from .import views 
urlpatterns = [
    path('',views.auth,name='auth'),
    path('home/',views.dashboard,name='dashboard'),
    path('add-country/', views.add_country, name='add_country'),
    path('add-university/', views.add_university, name='add_university'),
    path('universities/<int:country_id>/', views.universities_by_country, name='universities_by_country'),

    #For adding Program
    path('add-program/select-country/', views.select_country, name='select_country'),
    path('add-program/select-university/<int:country_id>/', views.select_university, name='select_university'),
    path('add-program/select-level/<int:university_id>/', views.select_level, name='select_level'),
    path('add-program/<int:university_id>/<str:level>/', views.add_program, name='add_program'),




]
