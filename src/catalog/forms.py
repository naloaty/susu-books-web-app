from django import forms
from .models import *


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'mdc-text-field__input'}
        ))
    password = forms.CharField(
        label='Пароль',
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'class': 'mdc-text-field__input'}
        )
    )


class RegisterForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'mdc-text-field__input'}
        )
    )
    email = forms.EmailField(
        label='Электропочта',
        widget=forms.EmailInput(
            attrs={'class': 'mdc-text-field__input'}
        )
    )
    name = forms.CharField(
        label='Отображаемое имя',
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'mdc-text-field__input'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'class': 'mdc-text-field__input'}
        )
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'release_date', 'price']
        labels = {
            'title': 'Название',
            'authors': 'Автор',
            'release_date': 'Дата публикации',
            'price': 'Цена'
        }
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'release_date': forms.DateInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'price': forms.NumberInput(
                attrs={'class': 'mdl-textfield__input'}
            )
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'last_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
        }
