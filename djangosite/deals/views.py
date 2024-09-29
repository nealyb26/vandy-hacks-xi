from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q, F

from .models import Post, Comment

def home(request) -> HttpResponse:
    context = {"query": "", "post_list": Post.objects.order_by("-post_date")}
    return render(request, "deals/search.html", context)

def detail(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "deals/detail.html", {"post": post})

def submit(request) -> HttpResponse:
    return render(request, "deals/create-post.html")

def submit_handler(request) -> HttpResponse:
    try:
        Post.objects.create(
            product_name=request.POST["prod_name"],
            location_name=request.POST["location"],
            post_date=timezone.now())
    except (KeyError):
        return render(request, "deals/create-post.html", {"error_message": "Necessary fields not filled out"})
    return HttpResponseRedirect(reverse("deals:home"))

def comment_handler(request, post_id: int) ->HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    try:
        Comment.objects.create(
            post=post, 
            body_text=request.POST["comment_text"],
            post_date=timezone.now())
    except (KeyError):
        return render(request, "deals/detail.html", {"error_message": "Necessary fields for comment not filled out"})
    return HttpResponseRedirect(reverse("deals:detail", kwargs={"post_id": post_id}))

def search(request) -> HttpResponse:
    if 'q' not in request.GET:
        return HttpResponse("you're supposed to do a request ya idjit!")
    get_query = request.GET['q']
    filter_set = Q()
    for q in get_query.split(' '):
        filter_set &= Q(product_name__contains=q) | Q(location_name__contains=q) | Q(info_text__contains=q) | Q(tags__name__contains=q)
    
    sort = "-post_date"
    if "sort" in request.GET:
        sort = request.GET["sort"]
        # e.g. '-score'
    
    post_list = Post.objects.filter(filter_set).order_by(sort)


    return render(request, "deals/search.html", {"query": get_query, "post_list" : post_list})

def vote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if "upvote" in request.POST:
        post.score = F("score") + 1
    elif "downvote" in request.POST:
        post.score = F("score") - 1
    post.save()
    if "original page" in request.POST:
        return HttpResponseRedirect(request.POST["original page"])
    else:
        return redirect('deals:home')