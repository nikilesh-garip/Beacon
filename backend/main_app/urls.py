# beacon-project/backend/urls.py
from django.urls import path
from. import views

urlpatterns = [
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login, name='login'),
    path('api/chatbot/', views.chatbot_response, name='chatbot'),
]