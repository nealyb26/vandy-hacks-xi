from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Post, Comment

def home(request) -> HttpResponse:
    context = {"post_list": Post.objects.order_by("-post_date")}
    return render(request, "deals/home.html", context)

def detail(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "deals/detail.html", {"post": post})