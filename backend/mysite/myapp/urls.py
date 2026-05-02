from django.urls import path
from . import views

urlpatterns = [
    # Endpoint for GET (list all) and POST (create)
    path('items/', views.manage_items, name='manage_items'),
    
    # Endpoint for DELETE (delete specific item by ID)
    path('items/<int:pk>/', views.delete_item, name='delete_item'),
]