from django.contrib import admin
from .models import Exercise, WorkoutPlan, WorkoutExercise, Progress

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty_level')
    search_fields = ('name', 'description')
    list_filter = ('difficulty_level',)

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'difficulty_level')
    list_filter = ('difficulty_level', 'created_by')
    search_fields = ('title', 'description')

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('workout_plan', 'exercise', 'sets', 'reps')
    list_filter = ('workout_plan', 'exercise')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'date', 'reps', 'hold_time')
    list_filter = ('user', 'exercise', 'date')
    search_fields = ('notes',)
