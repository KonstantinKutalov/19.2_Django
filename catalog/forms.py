from django import forms
from .models import Recipient, MailingSettings, Message


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']


class MailingSettingsForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ['send_time', 'frequency', 'status']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
