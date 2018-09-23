from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Subreddit



def index(request):
    all_subreddit = Subreddit.objects.order_by('id')[:5]
    context = {'all_subreddit': all_subreddit}
    return render(request, 'subred/index.html', context)

def detail(request, subreddit_id):
    return HttpResponse("detail view of %s" %subreddit_id)



