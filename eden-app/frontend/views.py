from django.shortcuts import render,redirect
from django.contrib import messages


# Create your views here.

def main(request):
    return render(request, 'frontend/index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Process the form data, such as saving it to a database or sending an email
        # You can create a Contact model and save the data, or send an email directly.
        
        messages.success(request, "Thank you for your message! We'll get back to you soon.")
        return redirect('contact') 
    return render(request,'frontend/contact.html')
def about(request):
    return render(request,'frontend/about.html')
def apply(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        services = request.POST.getlist('services')
        city = request.POST.get('city')
        
        # Here, handle saving the data to your model or process it as needed.
        
        messages.success(request, "Thank you for applying!")
        return redirect('main')
    return render(request,'frontend/apply.html')
