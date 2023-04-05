from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.index),
    path("register/create_user/", views.create_user),
    path("user/<str:user_link>", views.user_inf, name='user_inf'),
    path("user/<str:user_link>/sub", views.sub, name='sub_user'),
    path('user/<str:user_link>/delete_photo/<int:photo_id>', views.delete_photo, name='delete_photo'),
    path('user/<str:user_link>/like_photo/<int:photo_id>', views.like_photo, name='like_photo'),
    path("login_user/",views.log),
    path("login_user/loguser/",views.login_user),
    path('upload/', views.image_upload_view),
    path('user/<str:user_link>/logout', views.logout_user, name='logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)