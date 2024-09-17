from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Password does not match")
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        image_extension = image.name.split('.')[-1]

        if image_extension not in ['jpg', 'jpeg']:
            raise forms.ValidationError("Image format not supported")
        return image


class SignUpForm(UserCreationForm):
    pass


class LoginForm(AuthenticationForm):
    pass


class ProfileForm(forms.Form):
    mobile = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))