from django.urls import path
from . import views

urlpatterns = [
    path('heroes/', views.get_heroes, name='get_heroes'),
    path('compare/', views.compare_players, name='compare_players'),
    path('summary/', views.get_enhanced_summary, name='get_enhanced_summary'),
]
