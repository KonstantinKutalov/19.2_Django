from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password

from myproject.settings import DEFAULT_FROM_EMAIL
from users.models import User

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email_for_password_reset = forms.EmailField(label='Email для сброса пароля')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'country')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email_for_password_reset = self.cleaned_data.get('email_for_password_reset')
        if commit:
            user.save()
            self.send_password_reset_email(user)
        return user

    def send_password_reset_email(self, user):
        new_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        user.password = make_password(new_password)
        user.save()
        send_mail('Восстановление пароля', f'Ваш новый пароль: {new_password}', DEFAULT_FROM_EMAIL,
                  [user.email_for_password_reset], fail_silently=False)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

# Новое
