# MyWebApp/urls.py
from django.urls import path
from .views import user_data_form, success

urlpatterns = [
    path('', user_data_form, name='user_data_form'),
    path('user_data_form/', user_data_form, name='user_data_form'),
    path('success/', success, name='success'),
]
