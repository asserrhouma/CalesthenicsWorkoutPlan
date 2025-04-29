from django import forms
from .models import Exercise, WorkoutPlan, WorkoutExercise, Progress

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'difficulty_level', 'video_url', 'tips']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tips': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['title', 'description', 'difficulty_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'rest_time', 'order']
        widgets = {
            'rest_time': forms.NumberInput(attrs={'min': 0}),
            'order': forms.NumberInput(attrs={'min': 1}),
        }

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['exercise', 'reps', 'hold_time', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'reps': forms.NumberInput(attrs={'min': 0}),
            'hold_time': forms.NumberInput(attrs={'min': 0}),
        } 