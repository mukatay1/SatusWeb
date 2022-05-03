from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Post, UserProfile, Comment, Message


class SatusLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(SatusLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'typable'})
        self.fields['login'].label = 'Имя пользователя'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'typable'})
        self.fields['password'].label = 'Пароль'
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'checkbox_satus'})
        self.fields['remember'].label = 'Запомнить'


class SatusSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SatusSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'typable'})
        self.fields['username'].label = 'Придумайте имя пользователя'
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'typable'})
        self.fields['email'].label = 'Почта'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'typable'})
        self.fields['password1'].label = 'Придумайте пароль'
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'typable'})
        self.fields['password2'].label = 'Повторите пароль'


class DateFormat(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class PostForm(forms.ModelForm):
    name = forms.CharField(label='Титул', widget=forms.Textarea(attrs={'rows': 1, 'class': 'post_form'}))
    context = forms.CharField(label='', required=False,
                              widget=forms.Textarea(attrs={'rows': 5, 'class': 'post_form'}))
    photo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        exclude = ('slug', 'likes', 'dislikes', 'time_created', 'author')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            return ValidationError('Длина превышает 255 символов')
        return name


class UserProfileForm(forms.ModelForm):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('none', 'None')

    ]

    bio = forms.CharField(label='Ваше имя', required=False,
                          error_messages={'required': 'Данное поле должно быть заполненно',
                                          'invalid': 'Введите допустимое значение'},
                          widget=forms.TextInput(attrs={'class': 'typable_user'}))

    gender = forms.ChoiceField(label='Ваш пол', required=False, choices=GENDER,
                               error_messages={'required': 'Данное поле должно быть заполненно',
                                               'invalid': 'Введите допустимое значение'},
                               widget=forms.Select(attrs={'class': 'typable_usser'}))
    birth = forms.DateTimeField(label='Ваше день рождение', required=False,
                                error_messages={'required': 'Данное поле должно быть заполненно',
                                                'invalid': 'Введите допустимое значение'},
                                widget=DateFormat(format=["%d-%m-%Y"]))
    photo = forms.ImageField(label='Ваше фото', required=False,
                             error_messages={'required': 'Данное поле должно быть заполненно',
                                             'invalid': 'Введите допустимое значение'},
                             widget=forms.FileInput(attrs={'class': 'typable_user'}))
    phone = forms.IntegerField(label='Ваш номер', required=False,
                               error_messages={'required': 'Данное поле должно быть заполненно',
                                               'invalid': 'Введите допустимое значение'},
                               widget=forms.NumberInput(attrs={'class': 'typable_user'}))
    city = forms.CharField(label='Ваш город', required=False,
                           error_messages={'required': 'Данное поле должно быть заполненно',
                                           'invalid': 'Введите допустимое значение'},
                           widget=forms.TextInput(attrs={'class': 'typable_user'}))

    class Meta:
        model = UserProfile
        fields = ('bio', 'gender', 'birth', 'photo', 'phone', 'city')


class CommentForm(forms.ModelForm):
    context = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 2, 'class': 'post_form'}))

    class Meta:
        model = Comment
        fields = ('context',)


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=30, required=False)


class MessageForm(forms.ModelForm):
    photo = forms.ImageField(label='', required=False)
    body = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'msg_write', 'placeholder': 'Напишите что нибудь'}))

    class Meta:
        model = Message
        fields = ('photo', 'body')
