from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('creatures/', views.creatures_index, name='creatures_index'),
    path('creatures/<int:creature_id>/', views.creatures_detail, name='detail'),
    path('creatures/<int:creature_id>/add_feeding/', views.add_feeding, name='add_feeding')
]