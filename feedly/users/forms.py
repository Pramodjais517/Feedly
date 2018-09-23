from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
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

# class create_post_form(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('title',)