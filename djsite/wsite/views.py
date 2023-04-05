from django.http import  HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import User, Photo, Likes, Subscriptions
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import ImageForm
import os
from django.contrib.auth.decorators import login_required

def index(request):
    users = User.objects.all()
    return render(request,"index.html",{'users':users})

def create_user(request):
    if request.method == "POST":
        user = User()
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.bio = request.POST.get("bio")
        user.link = request.POST.get("link")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        if user.link == '':
            user.link = user.username
        user.set_password(request.POST.get("password"))
        user.save()
        return redirect("http://127.0.0.1:8000/user/"+user.link)
    return HttpResponseRedirect("/")

def user_inf(request,user_link):
    try:
        user = User.objects.get(link = user_link)
        images = Photo.objects.filter(user_id=user.id).all()
        if request.method == "delete":
            img = Photo.objects.get(user_id = user.id)
            img.delete()
            return HttpResponseRedirect("/")
        return render(request, "info_user.html",{'user':user,'photos':images})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")
    
    
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("http://127.0.0.1:8000/user/"+user.link)
        else:
            return HttpResponse("<h1>fail try to login</h1>")

def log(request):
    users = User.objects.all()
    return render(request,"login.html",{'users':users})

def logout_user(request,user_link):
    logout(request)
    return redirect("http://127.0.0.1:8000")


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageForm()
    return render(request, 'add_photo.html', {'form': form})

@login_required(redirect_field_name='login_user/')
def delete_photo(request, user_link, photo_id):
    user = get_object_or_404(User, link=user_link)
    photo = get_object_or_404(Photo, id=photo_id, user_id=user.id)
    if request.user.id != photo.user_id:
        return redirect('http://127.0.0.1:8000/login_user')
    else:
        photo.delete()
        os.remove("media/"+str(photo.image))
        return redirect('user_inf', user_link=user_link)

@login_required(redirect_field_name='login_user/')
def like_photo(request, user_link, photo_id):
    photo = get_object_or_404(Photo, id = photo_id)
    try:
        like = Likes.objects.get(photo_id=photo.id, user_id=request.user.id)
        like.delete()
        photo.like_count -=1
        photo.save()
        return redirect('user_inf', user_link=user_link)
    except Likes.DoesNotExist:
        like = Likes(photo_id=photo.id, user_id=request.user.id)
        like.save()
        photo.like_count +=1
        photo.save()
        return redirect('user_inf', user_link=user_link)

@login_required(redirect_field_name='login_user/')
def sub(request, user_link):
    user = get_object_or_404(User, link = user_link)
    if request.user.id != user.id:
        try:
            sub_user = Subscriptions.objects.get(following_user_id=request.user, user_id = user)
            sub_user.delete()
            user.sub_count -=1
            user.save()
            return redirect('user_inf', user_link=user_link)
        except Subscriptions.DoesNotExist:
            new_sub = Subscriptions(following_user_id=request.user, user_id = user)
            user.sub_count +=1
            user.save()
            new_sub.save()
            return redirect('user_inf', user_link=user_link)
    else:
        return HttpResponse("<h1>невозможно подписаться на самого себя, лучше найди друзей и тогда они смогут на тебя подписываться :( сори что давлю, но чувак реально найди друзей и все будет круто\</h1>")


def home(request):
    return render(request, "home.html")