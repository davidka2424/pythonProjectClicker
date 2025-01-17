from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    username = forms.CharField(
        max_length=20,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'placeholder': 'Как к вам можно обращаться?'}),
    )
    password = forms.CharField(
        min_length=3,
        max_length=20,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите надежный пароль, чтобы тяночка была только ваша'}),
    )
    password_confirm = forms.CharField(
        min_length=3,
        max_length=20,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли разные!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user