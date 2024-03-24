from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import FormView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product

from users.forms import UserRegisterForm, UserProfileForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Отправка письма с подтверждением
        send_mail(
            'Подтверждение регистрации',
            f'Вы успешно зарегистрированы. Ваш пароль: {form.cleaned_data["password1"]}',
            settings.DEFAULT_FROM_EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        # Генерация нового пароля
        new_password = ''.join(random.choices('abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=8))

        # Обновление пароля пользователя
        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        # Отправка нового пароля на почту пользователя
        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {new_password}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


