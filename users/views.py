from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile


# Create your views here.
def usersignup(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        request.session['username'] = username
        request.session['password'] = password
        return redirect('complete_profile')
    return render(request, 'users/user-signup.html')


def complete_profile(request):
    if request.method == 'POST':
        username = request.session.get('username')
        password = request.session.get('password')
        user = User.objects.create_user(username=username, password=password)
        user.first_name = request.POST.get('first_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Get or create UserProfile instance
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.gender = request.POST.get('gender', '')
        profile.interests = request.POST.get('interests', '')
        profile.profession = request.POST.get('profession', '')
        profile.country = request.POST.get('country', '')
        profile.about = request.POST.get('about', '')

         # Handle profile picture
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        # Save the UserProfile instance
        try:
            profile.save()
            print("Profile saved successfully")
        except Exception as e:
            print(f"Error saving profile: {e}")


            
        
        # Log the user in
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        
        return redirect('profile')
    return render(request, 'users/complete_profile.html')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile




# orginal code
def profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    context = {
        'profile': profile,
        'user': user
    }
    return render(request, 'users/author.html', context)
   



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



from allauth.socialaccount.models import SocialAccount
def get_google_profile(request):
    print("Getting Google profile information...")
    try:
        social_account = SocialAccount.objects.get(user=request.user, provider='google')
        print("Social account found:", social_account)
        extra_data = social_account.extra_data
        profile_picture = extra_data['picture']
        print("Profile picture URL:", profile_picture)
        name = extra_data['name']
        print("Name:", name)
        return profile_picture, name
    except Exception as e:
        print("Error retrieving Google profile information:", e)
        return None, None
    
    
from django.shortcuts import render

def profile_view(request):
    if request.user.socialaccount_set.filter(provider='google-oauth2').exists():
        social_account = request.user.socialaccount_set.get(provider='google-oauth2')
        print(social_account.extra_data)
        if 'picture' in social_account.extra_data:
            profile_picture = social_account.extra_data['picture']
            return render(request, 'users/author.html', {'profile_picture': profile_picture})
        else:
            return render(request, 'users/author.html', {'error': 'Profile picture not found'})
    else:
        return render(request, 'users/author.html')