from django import forms

from grumblr.models import Post, User
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': 'UserName'}))
    password = forms.CharField(max_length=200,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        try:
            activate_user = User.objects.get(username=cleaned_data.get('username'))
            if not activate_user.is_active:
                raise forms.ValidationError("User has not been activated! Please confirm your activate email!")
        except User.DoesNotExist:
            raise forms.ValidationError("User name does not exist!")

        current_user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))

        username = self.cleaned_data.get('username')
        try:
            User.objects.filter(username__exact=username)
        # if not User.objects.filter(username__exact=username):
        except User.DoesNotExist:
            raise forms.ValidationError("User name does not exist!")

        if current_user is None:
            raise forms.ValidationError("Password Incorrect!")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': 'FirstName'}))
    lastname = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'LastName'}))
    email = forms.CharField(max_length=200,
                            widget=forms.TextInput(attrs={'placeholder' : 'Email'}))
    username = forms.CharField(max_length=200,
                                widget=forms.TextInput(attrs={'placeholder': 'UserName'}))
    password1 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Create Password'}))
    password2 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Password did not match!")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(User.objects.filter(username__exact=username)) != 0:
            raise forms.ValidationError("Username is already taken!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(User.objects.filter(email__exact=email)) != 0:
            raise forms.ValidationError("Email is already been registered!")
        return email

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ModifyFirstnameForm(forms.Form):
    firstname = forms.CharField(max_length=200)

    def clean(self):
        cleaned_data = super(ModifyFirstnameForm, self).clean()
        return cleaned_data


class ModifyLastnameForm(forms.Form):
    lastname = forms.CharField(max_length=200)

    def clean(self):
        cleaned_data = super(ModifyLastnameForm, self).clean()
        return cleaned_data


class ModifyUsernameForm(forms.Form):
    username = forms.CharField(max_length=200)

    def clean(self):
        cleaned_data = super(ModifyUsernameForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(User.objects.filter(username__exact=username)) != 0:
            raise forms.ValidationError("Username is already taken!")
        return username


class ModifyBioForm(forms.Form):
    bio = forms.CharField(max_length=420)

    def clean(self):
        cleaned_data = super(ModifyBioForm, self).clean()
        return cleaned_data


class ModifyAgeForm(forms.Form):
    age = forms.IntegerField(max_value=120)

    def clean(self):
        cleaned_data = super(ModifyAgeForm, self).clean()
        return cleaned_data
