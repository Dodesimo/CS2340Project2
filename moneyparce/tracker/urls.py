from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add/', views.add_transaction_view, name='add_transaction'),
    path('regenerate-summary/<str:date_str>/', views.regenerate_summary_view, name='regenerate_summary'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]
