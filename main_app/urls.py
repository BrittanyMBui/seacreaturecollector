from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('creatures/', views.creatures_index, name='creatures_index'),
    path('creatures/<int:creature_id>/', views.creatures_detail, name='detail'),
    path('creatures/<int:creature_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('creatures/<int:creature_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('creatures/<int:creature_id>/delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('creatures/<int:creature_id>/delete/', views.delete_creature, name='delete_creature'),
    path('creatures/<int:creature_id>/edit/', views.edit_creature, name='edit_creature'),

    # AUTH
    path('accounts/signup', views.signup, name='signup'),
]