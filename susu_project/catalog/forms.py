from django import forms
from .models import *


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
