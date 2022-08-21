from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')


def signup(request):
    # created POST method 
    if request.method == "POST":
        username  = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        #checking fields are correct or not and redirecting again
        if password == password2:
            if User.objects.filter(email=email).exits():
                messages.info(request,'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
        else:
            messages.info(request,'Password does not match')
            return redirect('signup')
    else:
        return render(request,'signup.html')

