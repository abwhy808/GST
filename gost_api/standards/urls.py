from django.urls import path
from .views import gost_requirements

urlpatterns = [
    path('gost/', gost_requirements),
]