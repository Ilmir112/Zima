from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.views import LoginView



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'patronymic', 'position_in', 'organization', 'access_level')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['first_name'].label = 'Имя'
        self.fields['patronymic'].label = 'Отчество'
        self.fields['position_in'].label = 'Должность'
        self.fields['organization'].label = 'Организация'
        self.fields['access_level'].label = 'Уровень доступа'

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username