from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.user_login, name="user_login"),
    path("logout", views.user_logout, name="user_logout"),
    path("register", views.user_register, name="user_register"),
    path(
        "activate_account/<uidb64>/<token>",
        views.activate_account,
        name="activate_account",
    ),
    path("myaccount", views.account, name="myaccount"),
    path("my_vocabulary", views.my_vocabulary, name="my_vocabulary"),
    path("add_vocabularies", views.add_vocabularies, name="add_vocabularies"),
    path(
        "update_vocabulary/<str:pk>/",
        views.update_vocabulary,
        name="update_vocabulary",
    ),
    path(
        "delete_vocabulary/<str:pk>/",
        views.delete_vocabulary,
        name="delete_vocabulary",
    ),
    path(
        "delete_account/<str:pk>/", views.delete_account, name="delete_account"
    ),
    path("user/<str:pk>/", views.user, name="user"),
    path("allusers/", views.all_users, name="all-users"),
]
