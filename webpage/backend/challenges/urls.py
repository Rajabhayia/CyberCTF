from django.urls import path
from . import views

urlpatterns = [
    path('challengesData/', views.load_topics, name='load_topics'),
    path('checkFlag/', views.checkFlag, name='checkFlag' ),
]
