from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile,Post

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
             User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


class edit_profile_form(forms.ModelForm):
    # date_of_birth = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    class Meta:
        model = MyProfile
        fields=('avatar', 'first_name', 'last_name', 'gender', 'date_of_birth','phone_number')


class login_form(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ('username','password')


class create_imgpost_form(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    class Meta:
        model = Post
        exclude=('post_by','video','text')

class create_videopost_form(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    class Meta:
        model = Post
        exclude=('post_by','image','text')


class create_textpost_form(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    class Meta:
        model = Post
        exclude=('post_by','video','image')