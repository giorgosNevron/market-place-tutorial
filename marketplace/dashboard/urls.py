from django.urls import path

from .views import ItemsDashboard

app_name = 'dashboard'

urlpatterns = [
    path('', ItemsDashboard.as_view(), name='index'),
]