from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('translate_list/', views.get_translate_list, name='translate_list')
]