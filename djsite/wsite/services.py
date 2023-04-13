import os
from datetime import datetime
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from wsite.forms import ImageForm
from wsite.models import *

def create_user(request,user):
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

def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    return user

def image_upload(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.time_creation = datetime.now()
        image.save()
    else:
        form = ImageForm()
    return form

def delete_photo(request, photo):
    if request.user.id != photo.user_id:
        return "User isn't login or wrong user"
    else:
        photo.delete()
        photoImage = str(photo.image)
        os.remove(f"media/{photoImage}")
        return "cool"
    
def like_photo(request,photo):
    like = Likes(photo_id=photo.id, user_id=request.user.id)
    like.save()
    photo.like_count +=1
    photo.save()

def dislike_photo(request,photo,like):
    like.delete()
    photo.like_count -=1
    photo.save()

def sub_on_user(request,user):
    new_sub = Subscriptions(following_user_id=request.user, user_id = user)
    user.sub_count +=1
    user.save()
    new_sub.save()

def unsub_on_user(user,sub_user):
    sub_user.delete()
    user.sub_count -=1
    user.save()

def news_feed(sub):
    content_maker = get_object_or_404(Subscriptions,following_user_id=sub.id)
    photo_list = Photo.objects.filter(user_id=content_maker.user_id).all()
    return(photo_list)