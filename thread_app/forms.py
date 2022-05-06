from django import forms
from .models import Message


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=30, required=False)


class MessageForm(forms.ModelForm):
    photo = forms.ImageField(label='', required=False)
    body = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'msg_write', 'placeholder': 'Напишите что нибудь'}))

    class Meta:
        model = Message
        fields = (
            'photo',
            'body',
        )
