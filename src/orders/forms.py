from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name',
            'email', 'address', 'postal_code', 'city'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электропочта',
            'address': 'Адрес',
            'postal_code': 'Почтовый индекс',
            'city': 'Город'
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'postal_code': forms.NumberInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'mdl-textfield__input'}
            ),
        }