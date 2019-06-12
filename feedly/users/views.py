from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *
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
from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.db.models import Q
import json
import urllib
from django.conf import settings
from .search_engine import Search


class LandingView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request,'landing.html',{'form':Login_Form()})


class HomeView(View):
    """its the homepage of the site where posts are displayed """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        is_voted = Vote.objects.filter(voter=user,status = True)
        post_voted_list = list()
        form = CommentForm()

        for votes in is_voted:
            post_voted =Post.objects.get(vote=votes)
            post_voted_list.append(post_voted)

        context={
            # 'user':request.user,
            # 'searchform':SearchForm,
            'post_voted_list': post_voted_list,
            'object_list': Post.objects.order_by('-post_on'),
            'com_form': form,
            'comments':Comment.objects.all().order_by('comment_on')
        }
        return render(request, 'home.html', context)


class SortedView(View):
    """ this view helps in sorting the displayed posts according to the choice made."""
    @method_decorator(login_required)
    def get(self, request,rec, *args, **kwargs):
        if rec =='3':
            queryset=Post.objects.order_by('-post_on')
        if rec =='2':
            queryset = Post.objects.order_by('?')
        if rec =='1':
            queryset = Post.objects.order_by('-result')
        context={
            'object_list': queryset,
        }
        return render(request, 'home.html', context)


class SignUpView(View):
    """It is used to fill and validate and create a new user whenever a new signup form is filled"""
    form = SignupForm()

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ end of reCAPTCHA validation"""
            if result['success']:

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
                return redirect('signup')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return redirect('signup')
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
            # messages.success(request, 'thank you! for email verification')
            return redirect('edit_profile',user.id)
        else:
            return HttpResponse("invalid linkh")



class EditProfileView(View):
    @method_decorator(login_required)
    def post(self, request,user_id ,*args, **kwargs):
        form = Edit_Profile_Form(request.POST, request.FILES, instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!!')
            return redirect('edit_profile', user_id)
        else:
            return HttpResponse("hello")

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = Edit_Profile_Form(instance=request.user.myprofile)
        return render(request, 'edit_profile.html', {'form': form})


class LoginView(View):
    """This view logins the  user and raises validation error in case of wrong credentials """
    def post(self, request,*args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                messages.error('please! verify your Email first')
                return redirect('landing')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('landing')

    def get(self, request, *args, **kwagrs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = Login_Form()
        return render(request, 'landing.html', {'form': form})


class LogoutView(View):
    """this view simply logs out user and thereby deleting the session."""
    def get(self, request,*args, **kwargs):
        logout(request)
        return redirect('landing')


class ProfileView(View):
    """profile view is used to view and edit profile of yours"""
    @method_decorator(login_required)
    def get(self, request, user_id,*args, **kwargs):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(post_by=user).order_by('-post_on')
        userlogin = self.request.user
        is_voted = Vote.objects.filter(voter=userlogin, status=True)
        post_voted_list = list()
        form = CommentForm()
        for votes in is_voted:
            post_voted = Post.objects.get(vote=votes)
            post_voted_list.append(post_voted)
        context={
            'user': user,
            'posts': posts,
            'comments':Comment.objects.all().order_by('-comment_on'),
            'post_voted_list': post_voted_list,
            'com_form': form,
        }
        return render(request, 'profile.html', context)


class DeleteAccount(View):
    """this deletes the account of the user"""
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'delete_acc.html')

    def post(self, request, *args, **kwargs):
        choice = request.POST['des']
        if choice == 'accept':
            user = request.user
            user.delete()
            logout(request)
            return redirect('landing')
        if choice == 'reject':
            current_user = request.user
            return redirect('profile', current_user.id)


class CreatePostView(View):
    """this generates the new post for the user(ex : image,text,video)"""
    @method_decorator(login_required)
    def get(self, request,user_id,ch, *args, **kwagrs):
        if ch == 'image':
            form = Create_Imgpost_Form(request.POST or None, request.FILES or None)
        if ch == 'text':
            form = Create_Textpost_Form(request.POST or None)
        if ch == 'video':
            form = Create_Videopost_Form(request.POST or None, request.FILES or None)
        return render(request, 'createpost.html',{'form':form})

    @method_decorator(login_required)
    def post(self,request,user_id,ch,*args,**kwrgs):
        if ch == 'image':
            form = Create_Imgpost_Form(request.POST or None, request.FILES or None)
        if ch == 'text':
            form = Create_Textpost_Form(request.POST or None)
        if ch == 'video':
            form = Create_Videopost_Form(request.POST or None, request.FILES or None)
        f = form.save(commit=False)
        f.post_by = self.request.user
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'createpost.html', {'form': form,})


class VoteView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        post = request.GET['postid']
        print(post)
        user = self.request.user
        item = Post.objects.get(pk=post)
        prev_votes = Vote.objects.filter(Q(voter=user)& Q(post_id = post))
        has_voted = (prev_votes.count()>0)
        if not has_voted:
            Vote.objects.create(voter=user, post_id=post, status=True)
            item.result = item.result +1
            voted = True
            item.save()
        else:
            item.result = item.result - 1
            voted = False
            item.save()
            prev_votes[0].delete()
        result = Vote.objects.filter(post_id = post).count()
        print(result)
        print(voted)
        data={
            'result': result,
            'voted': voted,
        }

        return JsonResponse(data)


class CommentView(View):
    @method_decorator(login_required)
    def post(self,request,postid,*args,**kwargs):
        form = CommentForm(request.POST or None)
        print ("in view comment")
        print (postid)
        f = form.save(commit=False)
        f.comment_by = self.request.user
        f.post_id = postid
        if form.is_valid():
            form.save()
            # comm = Comment.objects.all().order_by('comment_on')
            # comments = list(comm.values())
            data = {
                'comment': f.content,
                'comment_by': f.comment_by.username,
                'comment_on': f.comment_on.strftime("%b. %d, %Y,%I:%M %p"),
            }
            return JsonResponse(data)

        else:
            return HttpResponse("form Invalid")


class SearchView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        search = request.GET.get('search')
        if search not in ('',' '):
            search_words = search.strip().split(' ')
            quer = MyProfile.objects
            query = Search(search_words,quer,0,user=request.user)
            friend = FriendList.objects.get(user=request.user)
            requests = FriendRequest.objects.get(user=request.user)
            sentreq = FriendRequestSent.objects.get(user=request.user)
            friendlist = list(friend.friends.all())
            requestlist = list(requests.friend_request.all())
            sentrequestlist = list(sentreq.request_sent.all())
            if query:
                context={
                        'results': query,
                        'friendlist': friendlist,
                        'requestlist': requestlist,
                        'sentrequest':sentrequestlist,
                       }
                return render(request,'search_result.html',context)
            else:
                    messages.success(request,"No user found!!")
                    return render(request,'search_result.html')
        else:
            return redirect(request.META['HTTP_REFERER'])


class SendCancelRequestView(View):

    @method_decorator(login_required)
    def get(self,request,user_id,*args,**kwargs):
        # user = user_id
        try:
            req= FriendRequestSent.objects.get(user=self.request.user,request_sent=user_id)
        except FriendRequestSent.DoesNotExist:
            req = None
        if req is None:
            sender = FriendRequestSent.objects.get(user=self.request.user)
            sender.request_sent.add(user_id)
            receiver = FriendRequest.objects.get(user=user_id)
            receiver.friend_request.add(sender.user)
            data={
                'status':'sent',
            }
            return JsonResponse(data)
        else:
            req.request_sent.remove(user_id)
            receiver = FriendRequest.objects.get(user=user_id)
            receiver.friend_request.remove(req.user)
            data={
                'status':'cancel'
            }
            return JsonResponse(data)


class FriendRequestView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        friend_request_list = FriendRequest.objects.get(user=self.request.user)
        request_list = list(friend_request_list.friend_request.all())
        context = {
            'friend_request_list':request_list,
        }
        return render(request,'friend_request.html',context)


class AcceptDeclineRequestView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        sender = self.kwargs['user_id']
        status = self.kwargs['status']
        if status == 'approve':
            req = FriendRequest.objects.get(user=self.request.user)
            req.friend_request.remove(sender)
            sent = FriendRequestSent.objects.get(user=sender)
            sent.request_sent.remove(self.request.user)
            friendlist = FriendList.objects.get(user=self.request.user)
            friendlist.friends.add(sender)
            senderfrndlist = FriendList.objects.get(user=sender)
            senderfrndlist.friends.add(self.request.user)
            data={
                'status':'approved',
                'user': sender,
            }
            return JsonResponse(data)
        elif status == 'decline':
            req = FriendRequest.objects.get(user=self.request.user)
            req.friend_request.remove(sender)
            sent = FriendRequestSent.objects.get(user=sender)
            sent.request_sent.remove(self.request.user)
            data = {
                'status':'declined',
                'res':sender
            }
            return JsonResponse(data)

class SentRequestView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        sender = FriendRequestSent.objects.get(user=self.request.user)
        sent_request = sender.request_sent.all()
        context={
            'sent_request':sent_request,
        }
        if len(sent_request)==0:
            messages.success(request,"No Sent request!!")
            return render(request,'sent_request.html')
        return render(request,'sent_request.html',context)