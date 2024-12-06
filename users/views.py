from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate


# Create your views here.


def usersignup(request):
    user=None
    error_message=None
    if request.POST:
        username=request.POST['email']
        password=request.POST['password']
        try:
            user=User.objects.create_user(username=username,password=password)
            return redirect('blog')  
        except Exception as e:
            error_message=str(e)
            messages.add_message(request, messages.ERROR, 'Email Already Exists')
            return redirect('usersignup')  
    return render(request,'users/user-signup.html',{'user':user, 'error_message':error_message})




def userlogin(request):
    error_message=None
    if request.POST:
        username=request.POST['email']
        password=request.POST['password']
        user=authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('blog')  # Redirect to home page after successful login
        else:
            messages.error(request, 'username or  password is incorrect')
            return redirect('userlogin')
    return render(request, 'users/user-login.html',{'error_message': error_message})


def profile(request):
    return render(request, 'users/profile.html')
from django.contrib.auth import logout as django_logout

def userlogout(request): 
    django_logout(request)
     # Clear session cookies 
    request.session.flush() 
    # Redirect to the blog's index page 
    return redirect('blog') # Assuming 'index' is the name of your index view


from django.shortcuts import redirect

def google_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'users/user-signup.html')



def google_login(request):
    return redirect('social:begin', 'google-oauth2')