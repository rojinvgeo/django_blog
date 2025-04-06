from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.userlogin, name='userlogin'),
    path('signup/', views.usersignup, name='usersignup'),
    path('complete_profile/',views.complete_profile, name='complete_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.userlogout, name='logout'),
    path('google-signup/', views.google_signup, name='google_signup'),
  path('google-login/', views.google_login, name='google_login'),  

]