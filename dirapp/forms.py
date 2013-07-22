from django import forms
from django.forms import ModelForm
from dirapp.models import UserProfile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class UserProfileForm(ModelForm):
    Address = forms.CharField(label='Postal Address', max_length=255)

    class Meta:
        model = UserProfile
        fields = ['Address', 'Photo', 'Phone']

    def clean_Photo(self):
        try:
            Photo = self.cleaned_data['Photo']
            if hasattr(Photo, 'content_type'):
                file_type = Photo.content_type.split('/')[1]
                if file_type != 'jpeg':
                    raise forms.ValidationError('Only JPEG files are supported')
        except IOError:
            pass
        return Photo


class PassForm(forms.Form):
    passA = forms.CharField(max_length=255, widget=forms.PasswordInput, label="Password", required=False)
    passB = forms.CharField(max_length=255, widget=forms.PasswordInput, label="Password again", required=False)

    def clean(self):
        try:
            passA = self.cleaned_data['passA']
            passB = self.cleaned_data['passB']
        except:
            passA = passB = ''
        if passA != passB:
            raise forms.ValidationError('Passwords does not match!')
        return self.cleaned_data


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']