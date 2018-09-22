from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm ,edit_profile_form,login_form
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from feedly.settings import EMAIL_HOST_USER
from .models import MyProfile

def home(request):
    return render(request ,'home.html')

#sidnup process /forms
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Activate Your Feedly Account'
                    message = render_to_string('acc_active_email.html', {

                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode,
                        'token': account_activation_token.make_token(user),
                    })
                    from_mail = EMAIL_HOST_USER
                    to_mail = [user.email]
                    send_mail(subject, message, from_mail, to_mail, fail_silently=False)
                    messages.success(request, 'please!Confirm your email to complete registration.')
                    return redirect('home')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})


#account activation function
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'thank you! for email verification')
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = edit_profile_form(request.POST,request.FILES,instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = edit_profile_form(instance=request.user.myprofile)
    return render(request, 'edit_profile.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return  render(request,'home.html')
            else:
                return HttpResponse('please! verify your Email first')
        else:
            messages.error(request,'username or password not correct')
            return  redirect('login')

    else:
        form = login_form()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request,'you are successfully logged out')
    return  redirect('home')


@login_required
def profile_view(request):
    return render(request,'profile.html')

