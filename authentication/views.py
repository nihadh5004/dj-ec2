from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        print('else')
        return redirect('signin') 
    
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username,password=password)
        print(username,password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('signin')
    else:
        return render(request,'signin.html')
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'signup.html')  
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'signup.html')
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match. Please re-enter the passwords.')
            return render(request, 'signup.html')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,'We have sent a link to your mail,Please Verify Account from Your Email')
        
        return render(request,'signin.html')
    else:
        return render(request,'signup.html')