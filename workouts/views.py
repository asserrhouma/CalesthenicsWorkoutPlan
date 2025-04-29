from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exercise, WorkoutPlan, WorkoutExercise, Progress
from .forms import ExerciseForm, WorkoutPlanForm, ProgressForm, WorkoutExerciseForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    # Get featured exercises (latest 4)
    featured_exercises = Exercise.objects.all().order_by('-id')[:4]
    
    # Get workout statistics
    workout_stats = {
        'total_workouts': WorkoutPlan.objects.count(),
        'total_exercises': Exercise.objects.count(),
        'total_users': User.objects.count()
    }
    
    # Get featured workout plans (latest 3)
    workout_plans = WorkoutPlan.objects.all().order_by('-id')[:3]  # Changed from -created_at to -id
    
    return render(request, 'workouts/home.html', {
        'exercises': featured_exercises,
        'workout_plans': workout_plans,
        'stats': workout_stats
    })

@login_required
def exercise_list(request):
    search_query = request.GET.get('search', '')
    exercise_list = Exercise.objects.all()
    
    if search_query:
        exercise_list = exercise_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(exercise_list, 6)
    page = request.GET.get('page')
    exercises = paginator.get_page(page)
    return render(request, 'workouts/exercise_list.html', {'exercises': exercises, 'search_query': search_query})

@login_required
def exercise_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Only staff members can create exercises')
        return redirect('exercise_list')
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = form.save()
            return redirect('exercise_detail', pk=exercise.pk)
    else:
        form = ExerciseForm()
    return render(request, 'workouts/exercise_form.html', {'form': form})

@login_required
def exercise_update(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'workouts/exercise_form.html', {'form': form})

@login_required
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')
    return render(request, 'workouts/exercise_confirm_delete.html', {'exercise': exercise})

@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'workouts/exercise_detail.html', {'exercise': exercise})

@login_required
def workout_list(request):
    workouts = WorkoutPlan.objects.filter(created_by=request.user)
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(WorkoutPlan, pk=pk, created_by=request.user)
    exercises = WorkoutExercise.objects.filter(workout_plan=workout)
    return render(request, 'workouts/workout_detail.html', {'workout': workout, 'exercises': exercises})

@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.created_by = request.user
            workout.save()
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutPlanForm()
    return render(request, 'workouts/workout_form.html', {'form': form})

@login_required
def workout_add_exercise(request, workout_pk):
    workout = get_object_or_404(WorkoutPlan, pk=workout_pk, created_by=request.user)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            workout_exercise = form.save(commit=False)
            workout_exercise.workout_plan = workout
            workout_exercise.save()
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutExerciseForm()
    return render(request, 'workouts/workout_exercise_form.html', {'form': form, 'workout': workout})

@login_required
def progress_list(request):
    progress = Progress.objects.filter(user=request.user)
    return render(request, 'workouts/progress_list.html', {'progress': progress})

@login_required
def progress_create(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            return redirect('progress_list')
    else:
        form = ProgressForm()
    return render(request, 'workouts/progress_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'workouts/register.html', {'form': form})
