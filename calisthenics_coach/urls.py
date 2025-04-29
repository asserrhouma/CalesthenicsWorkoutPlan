from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from workouts.views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('workouts.urls')),  # Include the workouts app URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='workouts/login.html'), name='login'),  # Update this line
    path('accounts/', include('django.contrib.auth.urls')),  # For other authentication views
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
