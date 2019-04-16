from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile,Post,Comment
from phonenumber_field.modelfields import PhoneNumberField

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
             User.objects.filter(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


class Edit_Profile_Form(forms.ModelForm):
    phone_number = forms.CharField(min_length=10,required=True)
    class Meta:
        model = MyProfile
        fields=('avatar', 'first_name', 'last_name', 'gender', 'date_of_birth','phone_number')


class Login_Form(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ('username','password')


class Create_Imgpost_Form(forms.ModelForm):

    class Meta:
        model = Post
        fields=('about','image',)

class Create_Videopost_Form(forms.ModelForm):

    class Meta:
        model = Post
        fields=('about','video',)


class Create_Textpost_Form(forms.ModelForm):
    text =forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    class Meta:
        model = Post
        fields = ('text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields=('content',)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30,required=True)

    class Meta:
        fields = ('search',)