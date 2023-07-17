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
            attrs={
                'class': 'mdc-text-field__input',
                'id': 'login-input',
                'aria-labelledby': 'login-input-label'
            }
        )
    )
    email = forms.EmailField(
        label='Электропочта',
        widget=forms.EmailInput(
            attrs={
                'class': 'mdc-text-field__input',
                'id': 'email-input',
                'aria-labelledby': 'email-input-label'
            }
        )
    )
    name = forms.CharField(
        label='Отображаемое имя',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'mdc-text-field__input',
                'id': 'name-input',
                'aria-labelledby': 'name-input-label'
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'mdc-text-field__input',
                'id': 'password-input',
                'aria-labelledby': 'password-input-label'
            }
        )
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name']
        labels = {
            'email': 'Электропочта',
            'name': 'Отображаемое имя'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'mdl-textfield__input'}),
            'name': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
        }


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


BOOK_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddBookForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=BOOK_QUANTITY_CHOICES,
        coerce=int
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
