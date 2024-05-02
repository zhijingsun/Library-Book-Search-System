from django import forms


class UserForm(forms.Form):
    email = forms.CharField(label="email", max_length=128)
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)

class RegisterForm(forms.Form):

    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label="birthday", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="confirm_password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
