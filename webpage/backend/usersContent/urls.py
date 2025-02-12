from django.urls import path
from . import views

urlpatterns = [
    path('load_users/', views.load_users, name='load_users'),
    path('load_team/', views.load_team, name='load_team'),
]
