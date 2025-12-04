from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'feed'

urlpatterns = [
    path("", views.feed, name="feed"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("login/", auth_views.LoginView.as_view(template_name='feed/login.html'), name="login"),
    path("create/", views.create_post, name="create_post"),
    path("profile/", views.view_profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("profile/<str:username>/", views.public_profile, name="public_profile"),
    path("post/<int:pk>/like/", views.vote_post, {'vote_type':'Like'}, name="like_post"),
    path("post/<int:pk>/dislike/", views.vote_post, {'vote_type':'Dislike'}, name="dislike_post"),
    path("post/<int:pk>/comment/", views.add_comment, name="add_comment"),

]