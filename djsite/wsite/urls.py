from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from wsite.views import *

urlpatterns = [
    path('', HomePage.as_view()),
    path('register/', IndexUser.as_view()),
    path("register/create_user/", CreateUser.as_view()),
    path("user/<str:user_link>", UserInf.as_view(), name='user_inf'),
    path("user/<str:user_link>/sub", SubUser.as_view(), name='sub_user'),
    path('user/<str:user_link>/delete_photo/<int:photo_id>', DeletePhoto.as_view(), name='delete_photo'),
    path('user/<str:user_link>/like_photo/<int:photo_id>', LikePhoto.as_view(), name='like_photo'),
    path("login_user/",Log.as_view()),
    path("login_user/loguser/",LoginUser.as_view()),
    path('upload/', ImageUpload.as_view()),
    path('user/<str:user_link>/logout', logout_user, name='logout'),
    path('news_feed', NewsFeed.as_view())
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)