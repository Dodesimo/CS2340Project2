from django.contrib import admin
from django.urls import path, include
from accounts.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('chatbot/', include('chatbot.urls')),
]
