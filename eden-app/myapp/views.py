from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Country, University, Program

# Authentication Views
def auth(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find the user by email
            user = User.objects.get(email=email)

            # Authenticate using the username (which is required by Django's default auth)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a success page
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    
    return render(request,'auth.html')

@login_required
def dashboard(request):
    countries = Country.objects.all()
    context = {
        'countries': countries
    }
    return render(request,'dashboard.html',context)

# Country Management Views
def add_country(request):
    if request.method == 'POST':
        country_name = request.POST.get('name')
        
        # Check if the country already exists
        if Country.objects.filter(name=country_name).exists():
            messages.error(request, 'Country already exists.')
        else:
            # Save the new country
            Country.objects.create(name=country_name)
            messages.success(request, f'Country "{country_name}" added successfully.')
        
        return redirect('add_country')  # Reload the form after submission
    
    return render(request, 'add_country.html')

def universities_by_country(request, country_id):
    # Fetch the country based on the ID
    country = get_object_or_404(Country, pk=country_id)
    
    # Get all universities related to the selected country
    universities = University.objects.filter(country=country)
    
    # Get filter parameters from GET request
    degree_type = request.GET.get('degree_type', None)
    category = request.GET.get('category', None)
    university_type = request.GET.get('university_type', None)

    # Filter programs based on degree type, category, and university type if they are selected
    filtered_programs = Program.objects.filter(university__country=country)
    
    if degree_type:
        filtered_programs = filtered_programs.filter(level=degree_type)
    
    if category:
        filtered_programs = filtered_programs.filter(category=category)
    
    if university_type:
        universities = universities.filter(university_type=university_type)
        filtered_programs = filtered_programs.filter(university__in=universities)
    
    # Fetch unique categories from the programs for the filter dropdown
    categories = Program.objects.values_list('category', flat=True).distinct()
    
    context = {
        'country': country,
        'universities': universities,
        'programs': filtered_programs,
        'categories': categories,
    }

    return render(request, 'universities_by_country.html', context)

# University Management Views
def add_university(request):
    countries = Country.objects.all()

    if request.method == 'POST':
        university_name = request.POST.get('name')
        country_id = request.POST.get('country')
        city_name = request.POST.get('city')
        university_type = request.POST.get('university_type')

        # Ensure all fields are filled
        if not university_name or not country_id or not city_name or not university_type:
            messages.error(request, 'Please fill out all fields.')
            return redirect('add_university')

        # Check if the country exists
        try:
            country = Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            messages.error(request, 'Selected country does not exist.')
            return redirect('add_university')

        # Check if the university already exists in that country and city
        if University.objects.filter(name=university_name, country=country, city=city_name).exists():
            messages.error(request, f'University "{university_name}" in "{city_name}" already exists.')
        else:
            # Save the new university
            University.objects.create(name=university_name, country=country, city=city_name,university_type=university_type)
            messages.success(request, f'University "{university_name}" added successfully.')

        return redirect('add_university')  # Reload the form after submission
    
    return render(request, 'add_university.html', {'countries': countries})

# Program Management Views
def select_country(request):
    if request.method == 'POST':
        selected_country = request.POST['country']
        return redirect('select_university', country_id=selected_country)
    
    countries = Country.objects.all()
    return render(request, 'select_country.html', {'countries': countries})

# Step 2: Select University based on the selected country
def select_university(request, country_id):
    if request.method == 'POST':
        selected_university = request.POST['university']
        return redirect('select_level', university_id=selected_university)
    
    universities = University.objects.filter(country_id=country_id)
    return render(request, 'select_university.html', {'universities': universities})

# Step 3: Select Program Level
def select_level(request, university_id):
    if request.method == 'POST':
        selected_level = request.POST['level']
        return redirect('add_program', university_id=university_id, level=selected_level)
    
    return render(request, 'select_level.html')

# Step 4: Add Program Form
def add_program(request, university_id, level):
    existing_categories = Program.objects.values_list('category', flat=True).distinct()
    if request.method == 'POST':

        program_name = request.POST['name']
        program_category = request.POST['category'] or request.POST.get('new_category')
        university = University.objects.get(id=university_id)
        Program.objects.create(
            university=university,
            level=level,
            name=program_name,
            category=program_category
        )
        return redirect('dashboard')  # Redirect to success or program list page after submission
    
    return render(request, 'add_program.html', {'level': level, 'university_id': university_id,'existing_categories': existing_categories})