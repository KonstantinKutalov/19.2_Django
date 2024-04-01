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
from django.urls import reverse

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.forms import UserRegisterForm, UserProfileForm

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Сначала устанавливаем пользователя неактивным
        user.save()

        # Отправляем письмо с подтверждением
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = self.request.build_absolute_uri(
            reverse('users:email_verification', kwargs={'uidb64': uid, 'token': token})
        )
        send_mail(
            'Подтверждение адреса электронной почты',
            f'Пожалуйста, подтвердите ваш адрес электронной почты, перейдя по ссылке: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def email_verification(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш адрес электронной почты успешно подтвержден.')
    else:
        messages.error(request, 'Недействительная ссылка подтверждения.')

    return redirect(reverse_lazy('users:login'))
