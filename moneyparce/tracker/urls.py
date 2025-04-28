from django.urls import path
from . import views

app_name = 'tracker'  # Add this line to define the namespace

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add/', views.add_transaction_view, name='add_transaction'),
    path('regenerate-summary/<str:date_str>/', views.regenerate_summary_view, name='regenerate_summary'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('new/', views.add_budget_view, name='add_budget'),
    path('example-budgets/', views.example_budgets_view, name='example_budgets'), # Ensure this exists if used
    path('manage-categories/', views.manage_categories_view, name='manage_categories'), # Add URL for managing categories
]
