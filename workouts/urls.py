from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:workout_pk>/add-exercise/', views.workout_add_exercise, name='workout_add_exercise'),
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/create/', views.progress_create, name='progress_create'),
    path('register/', views.register, name='register'),
]