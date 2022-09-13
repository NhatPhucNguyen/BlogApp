from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import Post,Comment,Topic
from .forms import PostCreateForm,PostUpdateForm
# Create your views here.

def home(request):
    return render(request,'base/home.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('post_list')
        else:
            messages.error(request,'Username or password does not exist !')
    context = {}
    return render(request,'base/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('post_list')

def signup_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request,'An error occurred during the registration !')
    context = {'form':form}
    return render(request,'base/signup.html',context)

def author_profile(request,pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    author = User.objects.get(id=pk)
    if q != '':    
        author_posts = Post.objects.filter(
            Q(author_id=author.id) & Q(topic__name=q)
        )
    else:
        author_posts = Post.objects.filter(
            author = author
        )    
    author_post_count = Post.objects.filter(author=author).count()
    topics = Topic.objects.all()
    topic_post_count = {}
    for topic in topics:
        topic_post_count.update({topic.name:Post.objects.filter(topic__name=topic,author=author).count()})
    context = {'author':author,"posts":author_posts,'post_count':author_post_count,'topics':topics,'topic_post_count':topic_post_count}
    return render(request,'base/author_profile.html',context)
        
def post_list(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(body__icontains=q) |
        Q(author__username = q)
    )        
    topics = Topic.objects.all()
    all_post_count= Post.objects.all().count()
    topic_post_count = {}
    for topic in topics:
        topic_post_count.update({topic.name:Post.objects.filter(topic__name=topic).count()})        
    context = {'posts':posts,'topics':topics,'post_count':all_post_count,'topic_post_count':topic_post_count}
    return render(request,'base/post_list.html',context)

def post_detail(request,pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comments.all()
    
    if request.method == 'POST':
        comment = Comment.objects.create(
            post = post,
            author = request.user,
            body = request.POST.get('body')
        )
        return redirect('post_details',pk=post.id)   
    context = {'post':post,'comments':post_comments}
    return render(request,'base/post_details.html',context)

@login_required(login_url='login')
def post_create(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid:            
            form.instance.author = request.user
            form.save()
            return redirect('post_list')
    context = {'form':form}
    return render(request,'base/post_create.html',context)

@login_required(login_url='login')
def post_update(request,pk):
    post = Post.objects.get(id=pk)
    form = PostUpdateForm(instance=post)
    if request.user != post.author:
        return HttpResponse('<h1>You are not allowed to edit the post !</h1>')
    if request.method == 'POST':
        form = PostCreateForm(request.POST,instance=post)
        if form.is_valid:
            form.save()
            return redirect('post_list')
    context = {'post':post,'form':form}
    return render(request,'base/post_update.html',context)

@login_required(login_url='login')
def post_delete(request,pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('<h1>You are not allowed to delete this post !</h1>')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    context = {'post':post}
    return render(request,'base/post_delete.html',context)

@login_required(login_url='login')
def comment_delete(request,pk):
    comment = Comment.objects.get(id=pk)    
    if request.user != comment.author:
        return HttpResponse('<h1>You are not allowed to delete this comment !</h1>')
    if request.method == 'POST':
        comment.delete()
        return redirect('post_details',pk=comment.post.id)
    context = {'comment':comment,'post':comment.post}
    return render(request,'base/comment_delete.html',context)   