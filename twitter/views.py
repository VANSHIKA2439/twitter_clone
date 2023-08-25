from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile,Tweet
from django.contrib import messages
from .forms import TweetsForm, SignUpForm, ProfileImageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = TweetsForm(request.POST or None)
        if request.method=="POST":
            if form.is_valid():
                tweet=form.save(commit=False)
                tweet.user=request.user
                tweet.save()
                messages.success(request,"Your tweet is posted succesfully. ")
                return redirect("home")
        tweets=Tweet.objects.all().order_by("-created_at")
        return render(request,'home.html',{'tweets':tweets,'form':form})
    else:
        tweets=Tweet.objects.all().order_by("-created_at")
        return render(request,'home.html',{'tweets':tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles=Profile.objects.exclude(user=request.user)
        
        return render(request,'profile_list.html',{'profiles':profiles})
    else:
        messages.success(request,"Please Login to view profiles. ")
        return redirect('home')


def profile(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        tweets=Tweet.objects.filter(user_id=pk)
        if request.method=='POST':
            current_user=request.user.profile
            action=request.POST['follow']
            if action=='unfollow':
                current_user.follows.remove(profile)
            elif action=='follow':
                current_user.follows.add(profile)
            current_user.save()
        return render(request,'profile.html',{'profile':profile,'tweets':tweets})
    else:
        messages.success(request,"Please Login to view your profile. ")
        return redirect('home')


def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        passwd=request.POST['passwd']
        user=authenticate(request,username=username,password=passwd)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been succesfully logged in!")
            return redirect('home')
        else:
            messages.success(request,"Please enter correct details.")
            return render(request,'login.html',{})
    else:
        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,"You have been succesfully logged out!")
    return redirect('home')

def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            passwd=form.cleaned_data['password1']
            user = authenticate(username=username,password=passwd)
            login(request,user)
            messages.success(request,"You have been succesfully registered!")
            return redirect('home')

    return render(request,'register.html',{'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        profile_user=Profile.objects.get(user__id=request.user.id)
        user_form=SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form=ProfileImageForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request,current_user)
            messages.success(request,"You have been succesfully updated your profile!")
            return redirect('home')
        return render(request,'update.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        messages.success(request,"You must be logged in to update your profile!")
        return redirect('home')

def tweet_likes(request,pk):
    if request.user.is_authenticated:
        tweet=get_object_or_404(Tweet,id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,"You must be logged in to like tweets!")
        return redirect('home')


def tweet_show(request,pk): 
    tweet=get_object_or_404(Tweet,id=pk)
    if tweet:
        return render(request,'tweet_show.html',{'tweet':tweet})
    else:
        messages.success(request,"You must be logged in to like tweets!")
        return redirect('home')

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id==pk:
            profiles=Profile.objects.get(user_id=pk)
            return render(request,'followers.html',{'profiles':profiles})
        else:
            messages.success(request,"Please Login to view profiles. ")
            return redirect('home')
    else:
        messages.success(request,"You must been logged in!")
        return redirect('home')

def unfollow(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request,(f"You have succesfully unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,"You must been logged in!")
        return redirect('home')

def follow(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request,(f"You have succesfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,"You must been logged in!")
        return redirect('home')

def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id==pk:
            profiles=Profile.objects.get(user_id=pk)
            return render(request,'follows.html',{'profiles':profiles})
        else:
            messages.success(request,"Please Login to view profiles. ")
            return redirect('home')
    else:
        messages.success(request,"You must been logged in!")
        return redirect('home')

def delete_tweet(request,pk):
    if request.user.is_authenticated:
        tweet=get_object_or_404(Tweet,id=pk)
        if request.user.username == tweet.user.username:
            tweet.delete()    
            messages.success(request,"Your tweet has beet succesfully deleted!")
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('home')
    else:
        messages.success(request,"You must be logged in to like tweets!")
        return redirect(request.META.get("HTTP_REFERER"))

def edit_tweet(request,pk):
    if request.user.is_authenticated:
        tweet=get_object_or_404(Tweet,id=pk)
        form = TweetsForm(request.POST or None,instance=tweet)
        if request.user.username == tweet.user.username:
            if request.method=="POST":
                if form.is_valid():
                    tweet=form.save(commit=False)
                    tweet.user=request.user
                    tweet.save()
                    messages.success(request,"Your tweet is edited succesfully. ")
                    return redirect("home")
                else:
                    return render(request,'edit_tweet.html',{'form':form,'tweet':tweet})
            else:
                return render(request,'edit_tweet.html',{'form':form,'tweet':tweet})
        else:
            messages.success(request,"You don't own the tweet! ")
            return redirect('home')
    else:
         messages.success(request,"You must be logged in to edit tweets!")
         return redirect(request.META.get("HTTP_REFERER"))


def search_tweet(request):
    if request.method=='POST':
        search=request.POST['search']
        searched=Tweet.objects.filter(body__contains=search)
        return render(request,'search_tweet.html',{'search':search,'searched':searched})
    return render(request,'search_tweet.html',{})


def search_user(request):
    if request.method=='POST':
        search=request.POST['search']
        searched=User.objects.filter(username__contains=search)
        return render(request,'search_user.html',{'search':search,'searched':searched})
    return render(request,'search_user.html',{})