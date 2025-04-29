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
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('edit-budget/<int:budget_id>/', views.edit_budget_view, name='edit_budget'),
    path('delete-budget/<int:budget_id>/', views.delete_budget_view, name='delete_budget'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction_view, name='delete_transaction'),
    path('edit-transaction/<int:transaction_id>/', views.edit_transaction_view, name='edit_transaction'),
    path('budget-notifications/', views.budget_notifications_view, name='budget_notifications'),
]
