from django.urls import path

from . import views

app_name = "deals"
urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:post_id>/", views.detail, name="detail"),
    path("submit/", views.submit, name="submit"),
    path("submit_handler", views.submit_handler, name="submithandler"),
    path("search/", views.search, name="search"),
]