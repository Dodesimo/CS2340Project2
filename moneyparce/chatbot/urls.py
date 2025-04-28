from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),               # Main chat page
    path('chat/', views.chat, name='chat'),             # AJAX endpoint for sending a message
    path('new/', views.new_conversation, name='new_conversation'),
    path('test/', views.test_gemini, name='test_gemini'),           # Simple Gemini API connection test
    path('debug/', views.debug, name='debug'),          # Debug conversations (optional, admin-only)
]
