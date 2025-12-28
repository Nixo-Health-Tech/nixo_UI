from django.urls import path
from . import views

#app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chatbot'),
    path('api/chat/', views.chat_handler, name='chat_api'),
]