from django import forms
from .models import Student,Education,PersonalDocument

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name','class':'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class':'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Date of Birth'}),
        }

class ParentalInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['father_name', 'mother_name', 'father_dob', 'mother_dob', 'father_cnic', 'mother_cnic']
        widgets = {
            'father_name': forms.TextInput(attrs={'placeholder': "Father's Name",'class':'form-control'}),
            'mother_name': forms.TextInput(attrs={'placeholder': "Mother's Name",'class':'form-control'}),
            'father_dob': forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder': "Father's Date of Birth"}),
            'mother_dob': forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder': "Mother's Date of Birth"}),
            'father_cnic': forms.TextInput(attrs={'placeholder': "Father's CNIC",'class':'form-control'}),
            'mother_cnic': forms.TextInput(attrs={'placeholder': "Mother's CNIC",'class':'form-control'}),
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'country_preference', 'course_preference', 'intake', 'academics',
            'ielts_score', 'pte_score', 'toefl_score', 'education_gap', 'work_experience',
            'marital_status', 'visa_history', 'comments', 'spouse_qualification',
            'spouse_employment_status', 'spouse_income', 'no_of_kids', 'no_of_dependents'
        ]
        widgets = {
            'country_preference': forms.TextInput(attrs={'placeholder': 'Country Preference','class':'form-control'}),
            'course_preference': forms.TextInput(attrs={'placeholder': 'Course Preference','class':'form-control'}),
            'intake': forms.TextInput(attrs={'placeholder': 'Intake','class':'form-control'}),
            'academics': forms.TextInput(attrs={'placeholder': 'Academics','class':'form-control'}),
            'ielts_score': forms.TextInput(attrs={'placeholder': 'IELTS Score','class':'form-control'}),
            'pte_score': forms.TextInput(attrs={'placeholder': 'PTE Score','class':'form-control'}),
            'toefl_score': forms.TextInput(attrs={'placeholder': 'TOEFL Score','class':'form-control'}),
            'education_gap': forms.TextInput(attrs={'placeholder': 'Education Gap','class':'form-control'}),
            'work_experience': forms.TextInput(attrs={'placeholder': 'Work Experience','class':'form-control'}),
            'marital_status': forms.TextInput(attrs={'placeholder': 'Marital Status','class':'form-control'}),
            'visa_history': forms.TextInput(attrs={'placeholder': 'Visa History','class':'form-control'}),
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comments','class':'form-control'}),
            'spouse_qualification': forms.TextInput(attrs={'placeholder': 'Spouse Qualification','class':'form-control'}),
            'spouse_employment_status': forms.TextInput(attrs={'placeholder': 'Spouse Employment Status','class':'form-control'}),
            'spouse_income': forms.TextInput(attrs={'placeholder': 'Spouse Income','class':'form-control'}),
            'no_of_kids': forms.TextInput(attrs={'placeholder': 'Number of Kids','class':'form-control'}),
            'no_of_dependents': forms.TextInput(attrs={'placeholder': 'Number of Dependents','class':'form-control'}),
        }
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['level', 'institute', 'passing_year', 'percentage_or_cgpa','degree_file']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
            'institute': forms.TextInput(attrs={'placeholder': 'Institute','class':'form-control'}),
            'passing_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Passing Year'}),
            'percentage_or_cgpa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Percentage or CGPA'}),
        }

class PersonalDocumentForm(forms.ModelForm):
    class Meta:
        model = PersonalDocument
        fields = ['document_type', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
        }

