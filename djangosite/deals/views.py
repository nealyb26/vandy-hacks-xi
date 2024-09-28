from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import Post, Comment

def home(request) -> HttpResponse:
    context = {"post_list": Post.objects.order_by("-post_date")}
    return render(request, "deals/home.html", context)

def detail(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "deals/detail.html", {"post": post})

def submit(request) -> HttpResponse:
    return render(request, "deals/create-post.html")

def submit_handler(request) -> HttpResponse:
    try:
        Post.objects.create(
            product_name=request.POST["prod_name"],
            location=request.POST["location"],
            post_date=timezone.now())
    except (KeyError):
        return render(request, "deals/create-post.html", {"error_message": "Necessary fields not filled out"})
    return HttpResponseRedirect(reverse("deals:home"))