from django.urls import path

from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('forecast/<city>/', views.forecast_by_city, name='forecast'),
]