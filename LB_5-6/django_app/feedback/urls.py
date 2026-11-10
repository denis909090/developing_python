from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('form/', views.feedback_page, name='feedback'),
]
