from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from dirapp.models import UserProfile
from django import forms
from names import get_first_name
from random import randint


class MyForm(forms.ModelForm):
    # Checkbox input for generating new password, this is not tightened with DB Model
    GenPass = forms.NullBooleanField(label='Email new password?', widget=forms.CheckboxInput())

    class Meta:
        model = UserProfile

    def clean_Photo(self):
        try:
            Photo = self.cleaned_data['Photo']
            file_type = Photo.content_type.split('/')[1]
            if file_type != 'jpeg':
                raise forms.ValidationError('Only JPEG files are supported')
        except:
            pass
        return Photo


    # http://stackoverflow.com/questions/817284/overriding-the-save-method-in-django-modelform
    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(MyForm, self).save(commit=False)
        # Email user when new password generated
        if 'GenPass' in self.changed_data:
            userobject = self.cleaned_data['user']
            password = get_first_name() + str(randint(1000, 9999))
            userobject.set_password(password)
            userobject.save()
            mail = 'username: ' + userobject.username + "\npassword: " + password
            userobject.email_user('Your new password', mail, 'admin@dir.app')
        if commit:
            m.save()
        return m


class UserProfileInline(admin.StackedInline):
    form = MyForm
    model = UserProfile
    can_delete = False  # http://stackoverflow.com/questions/1470811/django-disallow-can-delete-on-genericstackedinline


class UserAdmin(DjangoUserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)