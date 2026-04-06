from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('matches/', views.best_matches, name='best_matches'),
]