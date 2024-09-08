from django.urls import path
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('applyonline',views.apply,name='apply') 
]
