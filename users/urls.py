from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import PasswordResetView

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  # Добавлен URL-шаблон для входа
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('email_verification/<uidb64>/<token>/', email_verification, name='email_verification'),
]
