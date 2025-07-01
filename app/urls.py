from django.urls import path, include
from .views import *
urlpatterns = [
    path("",index,name="index"),
    path('register/',register, name='register'),
    path('otp/',getotp,name="otp"),
    path('login/',user_login,name="login"),
    path('reset/',resetpass,name="reset"),
    path('reset/<uidb64>/<token>/',password_reset, name='password_reset_confirm'),
    path('editprofile/',editprofile,name="editprofile"),
    path('logout/',user_logout,name="logout"),
    path('profile/<str:username>/',profile,name="profile"),
    path('reels/',reels_view,name="reels"),
    path('resend_otp/',resend_otp,name="resend_otp"),
    path('passwordemail/',passwordResetEmail,name="passwordemail"),
    path('follow/<str:username>/',follow_unfollow_user, name='follow_unfollow_user'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
    path('like/<int:post_id>/',like_post, name='like-post'),
    path('search/',search_users,name="search"),
    # path('comment/',comment,name="comment"),
    # path('addcomment/',addcomment,name="addcomment"),
   





    path("__reload__/", include("django_browser_reload.urls")),
]
