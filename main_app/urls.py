from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dogs/', views.dogs_index, name='dog_index'),
    path('dogs/<int:dog_id>/', views.dogs_detail, name='dog_detail'),
    path('dogs/create/', views.DogCreate.as_view(), name='dog_create'),
    path('dogs/<int:pk>/update/', views.DogUpdate.as_view(), name='dog_update'),
    path('dogs/<int:pk>/delete/', views.DogDelete.as_view(), name='dog_delete'),
    path('dogs/<int:dog_id>/add_activity/',views.add_activity, name='add_activity'),
    path('activity/<int:pk>/delete', views.ActivityDelete.as_view(), name='activity_delete'),
    path('activity/<int:activity_id>/add_activity_photo/<int:dog_id>', views.add_activity_photo, name='add_activity_photo'),
    path('dogs/<int:dog_id>/add_dog_photo/', views.add_dog_photo, name='add_dog_photo'),
    path('dogs/view/dog/<int:dogphoto_id>/', views.view_photo_profile, name='view_photo_profile'),
    path('dogs/view/activity/<int:photo_id>', views.view_photo_activity, name='view_photo_activity'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/edit/', views.UserEditView.as_view(), name='edit_profile'),
    path('landing/', views.landing, name='landing'),
    path('profile/<int:user_id>/add_time_punch', views.add_time_punch, name='add_time_punch'),
    path('profile/', views.profile, name='user-profile'),
]
