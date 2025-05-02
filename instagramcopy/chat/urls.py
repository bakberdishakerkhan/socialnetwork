from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.select_user, name='select_user'), 
    path('<int:other_user_id>/', views.chat_view, name='chat_view'),  
]
