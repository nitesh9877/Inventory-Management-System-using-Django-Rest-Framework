# inventory/urls.py

from django.urls import path
from .views import create_item, read_item, update_item, delete_item, register, login, get_all_items

urlpatterns = [
    path('items/', create_item, name='create_item'), # ==== for create =======
    path('items/<int:item_id>/', read_item, name='read_item'), # == GET single items ========
    path('items/all/', get_all_items, name='get_all_items'),  # == GET all items ========
    path('items/<int:item_id>/update/', update_item, name='update_item'), # ===== for update ====
    path('items/<int:item_id>/delete/', delete_item, name='delete_item'), # ===== for delete ====
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    
]

