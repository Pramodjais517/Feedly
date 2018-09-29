from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
from django.views import View
from .models import MyProfile,Post,Vote

class HomeView(View):
     def get(self, request, *args, **kwargs):

         context={
             # 'user':request.user,
             # 'post': Post,
             'object_list': Post.objects.order_by('-post_on'),
         }
         return render(request, 'home.html', context)


#sidnup process /forms

class SignUpView(View):
    form = SignupForm()

    def post(self, request, *args, **kwargs):
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
            messages.success(request, 'Please!Confirm your email to complete registration.')
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})



    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = SignupForm()
            return render(request, 'signup.html', {'form': form})


#account activation function

class Activate(View):
    def get(self, request, uidb64, token):
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
            return redirect('edit_profile',user.id)
        else:
            messages.success('Activation link is invalid!')
            return redirect('home')



class EditProfileView(View):
    @method_decorator(login_required)
    def post(self, request,user_id ,*args, **kwargs):
        form = edit_profile_form(request.POST, request.FILES, instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id)
        else:
            return HttpResponse("hello")

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = edit_profile_form(instance=request.user.myprofile)
        return render(request, 'edit_profile.html', {'form': form})


class LoginView(View):
        def post(self, request,*args, **kwargs):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'woahh!! logged in..')
                    return redirect('home')
                else:
                    return HttpResponse('please! verify your Email first')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')

        def get(self, request, *args, **kwagrs):
            if request.user.is_authenticated:
               return redirect('home')
            else:
                form = login_form()
            return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request,*args, **kwargs):
        logout(request)
        messages.success(request, 'you are successfully logged out')
        context={
            'object_list': Post.objects.order_by('-post_on')
        }
        return render(request, 'home.html', context)


class ProfileView(View):
    model= User
    @method_decorator(login_required)
    def get(self, request, user_id,*args, **kwargs):
        user = User.objects.get(pk=user_id)
        context={
            'user': user
        }
        return render(request, 'profile.html', context)

class DeleteAccount(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'delete_acc.html')

    def post(self, request, *args, **kwargs):
        choice = request.POST['des']
        if choice == 'accept':
            user = request.user
            user.delete()
            logout(request)
            context={
                'object_list': Post.objects.order_by('-post_on'),
            }
            messages.success(request, 'Your account is successfully deleted')
            return render(request,'home.html', context)
        if choice == 'reject':
            current_user = request.user
            return redirect('profile', current_user.id)

# class CreatePostView(View):
#     @method_decorator(login_required)
#     def get(self, request, *args, **kwagrs):
#         return render(request, 'createpost.html',{ 'form': create_imgpost_form()})
#     @method_decorator(login_required)
#     def post(self,request,user_id,*args,**kwrgs):
#         form = create_imgpost_form(request.POST)
#         context = {
#             'object_list': Post.objects.order_by('-post_on'),
#         }
#         if form.is_valid():
#             form.save()
#             return render(request, 'home.html', context)

