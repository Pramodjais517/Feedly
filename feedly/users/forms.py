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
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class edit_profile_form(forms.ModelForm):
     class Meta:
         model = MyProfile
         fields =('avatar','first_name','last_name','phone_number',
                  'date_of_birth',)




class login_form(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields=('username','password',)