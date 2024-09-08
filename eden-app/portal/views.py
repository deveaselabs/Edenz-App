from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Employee, Student,PersonalDocument,Education
from django.contrib import messages
from django.contrib.auth import login , authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import StudentUpdateForm, ParentalInfoForm, InquiryForm,EducationForm,PersonalDocumentForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect


def index(request):
    if request.method == 'POST':
        passkey = request.POST['passkey']
        print(passkey)
        if passkey == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        elif passkey == 'emp':
            return redirect('emp_login')
        elif passkey == 'std':
            return redirect('student_login')

    return render(request,'portal/index.html')
# For Employee Registration
def emp_reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        education = request.POST.get('education')
        cnic = request.POST.get('cnic')
        password = request.POST.get('password')


        if User.objects.filter(username = cnic).exists():
            messages.error(request,'An Employee with this cnic already exists!!')
            return render(request,'portal/emp_reg.html')

        try:
            # Create the user object
            user = User.objects.create_user(username=cnic , password=password)
            #Create model for employee
            employee = Employee.objects.create(user = user,education= education,name = name)
            # Generate Message of success
            messages.success(request, 'Employee added successfully!')

            return redirect('emp_login')
        except Exception as e:
            # Generate Error messages
            messages.error(request,f'Error: {str(e)}')

    return render(request,'portal/emp_reg.html')

# For Employee Login

def emp_login(request):
    if request.method == 'POST':
        cnic = request.POST.get('cnic')
        password = request.POST.get('password')

        user = authenticate(username = cnic,password = password)

        if user is not None:
            login(request,user)
            return redirect(reverse('emp_portal',kwargs={'cnic' : cnic}))
        else:
            messages.error(request,'Invalid credentials')

    return render(request,'portal/emp_login.html')
# for rendering portal
@login_required
def emp_portal(request, cnic=None):
    if cnic is None:
        cnic = request.user.username
    
    try:
        employee = Employee.objects.get(user__username=cnic)
        students = Student.objects.all()  # Fetch all students

        student_data = []
        for student in students:
            educations = Education.objects.filter(student=student)
            personal_documents = PersonalDocument.objects.filter(student=student)
            student_data.append({
                'student': student,
                'educations': educations,
                'personal_documents': personal_documents
            })

        return render(request, 'portal/emp_portal.html', {'emp': employee, 'student_data': student_data})
    except Employee.DoesNotExist:
        messages.error(request, 'Employee does not exist.')
        return redirect('emp_login')
# Student Registration
 
def student_reg(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        cnic = request.POST['cnic']
        cell_no = request.POST['cell_no']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'student_reg.html')
        if User.objects.filter(email = email):
            messages.error(request,"Email already in Use")
            return redirect('student_reg')

        # Create username from CNIC
        username = cnic

        # Create student object
        try:  
            # Create User object
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create Student object
            student = Student.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            cnic=cnic,
            cell_no=cell_no,
            email=email,
            date_of_birth = date_of_birth
        )
            send_mail(
                'Student Registration Confirmation',
                f'Hello {first_name}:\n You have been registerd as a student in our student information portal.\n Your credentials are as follows:\n User name: {cnic} \n password: {password}\n Edenz Consultants Student Info Center\n Regards','info@edenzconsultant.com',[email],fail_silently=False,
            )
            messages.success(request, 'Student registered successfully!')
            return redirect('student_login')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request,'portal/student_reg.html')
def student_login(request):
    if request.method == 'POST':
        cnic = request.POST['cnic']
        password = request.POST['password']

        # Authenticate student
        user = authenticate(username=cnic, password=password)

        if user is not None:
            # Login successful, redirect to student portal
            login(request, user)
            return redirect(reverse('student_portal',kwargs={'cnic' : cnic}))
        else:
            # Authentication failed, display error message
            messages.error(request,'Invalid credentials')
            return render(request, 'portal/student_login.html')

    return render(request,'portal/student_login.html')

@login_required
def student_portal(request, cnic=None):
    if cnic is None:
        cnic = request.user.username

    student = get_object_or_404(Student, user__username=cnic)

    # Initialize forms
    personal_form = StudentUpdateForm(instance=student)
    parental_form = ParentalInfoForm(instance=student)
    inquiry_form = InquiryForm(instance=student)
    education_form = EducationForm()
    personal_document_form = PersonalDocumentForm()

    if request.method == 'POST':
        if 'personal' in request.POST:
            personal_form = StudentUpdateForm(request.POST, instance=student)
            if personal_form.is_valid():
                personal_form.save()
                messages.success(request, 'Personal information updated successfully.')
        elif 'parental' in request.POST:
            parental_form = ParentalInfoForm(request.POST, instance=student)
            if parental_form.is_valid():
                parental_form.save()
                messages.success(request, 'Parental information updated successfully.')
        elif 'inquiry' in request.POST:
            inquiry_form = InquiryForm(request.POST, instance=student)
            if inquiry_form.is_valid():
                inquiry_form.save()
                messages.success(request, 'Inquiry form updated successfully.')
        elif 'education' in request.POST:
            education_form = EducationForm(request.POST, request.FILES)
            if education_form.is_valid():
                education_instance = education_form.save(commit=False)
                education_instance.student = student
                education_instance.save()
                messages.success(request, 'Education information added successfully.')
        elif 'personal_document' in request.POST:
            personal_document_form = PersonalDocumentForm(request.POST, request.FILES)
            if personal_document_form.is_valid():
                personal_document_instance = personal_document_form.save(commit=False)
                personal_document_instance.student = student
                personal_document_instance.save()
                messages.success(request, 'Personal document added successfully.')

    educations = Education.objects.filter(student=student)
    personal_documents = PersonalDocument.objects.filter(student=student)

    return render(request, 'portal/student_portal.html', {
        'student': student,
        'personal_form': personal_form,
        'parental_form': parental_form,
        'inquiry_form': inquiry_form,
        'education_form': education_form,
        'personal_document_form': personal_document_form,
        'educations': educations,
        'personal_documents': personal_documents,
    })

def logout_view(request):
    logout(request)
    return redirect(reverse('student_login')) 
# Assuming you have a file like portal/views.py

def employee_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('emp_login')  # Replace 'login' with the name of your login URL pattern
