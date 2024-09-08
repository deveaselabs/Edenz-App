from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
def validate_file_size(file):
    if file.size > 5 * 1024 * 1024:  # 5 MB
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    

@deconstructible
class PathAndRename:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if isinstance(instance, PersonalDocument):
            upload_to = 'personal_documents'
            filename = f'{instance.student.user.username}_{instance.get_document_type_display().replace(" ", "_").lower()}.{ext}'
        elif isinstance(instance, Education):
            upload_to = 'degrees'
            filename = f'{instance.student.first_name}_{instance.level}.{ext}'
        else:
            raise ValueError("Unknown instance type")
        return os.path.join(upload_to, instance.student.user.username, filename)
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=50)
    position = models.CharField(blank=True,max_length=50)
    department = models.CharField(blank=True,max_length=50)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15, unique=True)
    cell_no = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # Parental Information
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    father_dob = models.DateField(blank=True, null=True)
    mother_dob = models.DateField(blank=True, null=True)
    father_cnic = models.CharField(max_length=15, blank=True, null=True)
    mother_cnic = models.CharField(max_length=15, blank=True, null=True)
    # Inquiry Form Fields
    country_preference = models.CharField(max_length=100, blank=True, null=True)
    course_preference = models.CharField(max_length=100, blank=True, null=True)
    intake = models.CharField(max_length=100, blank=True, null=True)
    academics = models.TextField(blank=True, null=True)
    ielts_score = models.CharField(max_length=100, blank=True, null=True)
    pte_score = models.CharField(max_length=100, blank=True, null=True)
    toefl_score = models.CharField(max_length=100, blank=True, null=True)
    education_gap = models.TextField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    visa_history = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    spouse_qualification = models.CharField(max_length=100, blank=True, null=True)
    spouse_employment_status = models.CharField(max_length=100, blank=True, null=True)
    spouse_income = models.CharField(max_length=100, blank=True, null=True)
    no_of_kids = models.IntegerField(blank=True, null=True)
    no_of_dependents = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Education(models.Model):
    EDUCATION_LEVELS = [
        ('SSC', 'SSC'),
        ('HSSC', 'HSSC'),
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
        ('PhD', 'PhD'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='educations')
    level = models.CharField(max_length=10, choices=EDUCATION_LEVELS)
    institute = models.CharField(max_length=100)
    passing_year = models.CharField(max_length=4)
    percentage_or_cgpa = models.CharField(max_length=10)
    degree_file = models.FileField(upload_to=PathAndRename(), blank=True, null=True)

    def __str__(self):
        return f"{self.get_level_display()} from {self.institute}"
    
class PersonalDocument(models.Model):
    DOCUMENT_TYPES = [
        ('CNIC_Front', 'CNIC Front'),
        ('CNIC_Back', 'CNIC Back'),
        ('Passport', 'Passport'),
        ('PassportSizePic', 'Passport Size Picture'),
        ('ExperienceLetter', 'Experience Letter'),
        ('CV', 'CV'),
        ('LetterOfRecommendation', 'Letter of Recommendation'),
        ('Resume', 'Resume'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='personal_documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to=PathAndRename(), validators=[validate_file_size])

    def __str__(self):
        return f"{self.student.first_name}'s {self.get_document_type_display()}"