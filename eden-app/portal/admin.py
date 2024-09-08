from django.contrib import admin
from .models import Employee,Student,Education,PersonalDocument

# Register your models here.

admin.site.register(Employee)
admin.site.register(Student)
admin.site.register(Education)
admin.site.register(PersonalDocument)
