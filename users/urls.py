from django.urls import path

from users import views

urlpatterns = [
    path('profile', views.UserProfile.as_view(), name='profile'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('logout', views.UserLogout.as_view(), name='logout'),
]
