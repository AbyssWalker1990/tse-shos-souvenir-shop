from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from goods.models import OrderProduct
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=("Пароль"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Підтвердження паролю"),
                                widget=forms.PasswordInput,
                                help_text=("Введіть такий самий пароль ще раз"))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        labels = {
            'username': 'Логін',
            'email': 'Електронна пошта',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'second_name', 'father_name', 'email']
        labels = {
            'first_name': "Ім'я",
            'second_name': 'Прізвище',
            'father_name': 'По батькові',
            'email': 'Електронна пошта',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control'}
            )


class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['count']

    def __init__(self, *args, **kwargs):
        super(OrderProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control w-25 form-control-color',
                 'id': 'goods-count-input',
                 }
            )

