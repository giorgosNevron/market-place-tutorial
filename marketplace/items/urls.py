from django.urls import path

from .views import Items, ItemDetails, NewItem, DeleteItem, EditItem

app_name = 'item'

urlpatterns = [
    path('', Items.as_view(), name='items'),
    path('new/', NewItem.as_view(), name='new'),
    path('<int:pk>/', ItemDetails.as_view(), name='detail'),
    path('<int:pk>/delete/', DeleteItem.as_view(), name='delete'),
    path('<int:pk>/edit/', EditItem.as_view(), name='edit'),
]