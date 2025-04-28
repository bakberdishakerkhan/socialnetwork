from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('registration/', views.registration, name='registr'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('follow_toggle/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
]
