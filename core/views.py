from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import os
from django.template.loader import get_template

# Welcome Page
def welcome(request):
    print("Current working directory:", os.getcwd())
    try:
        template = get_template('welcome.html')
        print("Template found successfully!")
    except Exception as e:
        print("Template error:", e)
    return render(request, 'welcome.html')
# Registration Page
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        return redirect('login')
    return render(request, 'register.html')

# Login Page
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('welcome')  # Redirect to the welcome page after logout

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Circle, Membership, Post
from .forms import CircleForm, PostForm


@login_required
def home(request):
    my_circles = Circle.objects.filter(membership__user=request.user)
    global_circles = Circle.objects.exclude(membership__user=request.user)
    return render(request, 'home.html', {
        'my_circles': my_circles,
        'global_circles': global_circles,
    })

@login_required
def circle_detail(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    members = Membership.objects.filter(circle=circle)
    posts = circle.posts.all()
    user_is_member = members.filter(user=request.user).exists()

    if request.method == 'POST':
        if 'join_circle' in request.POST and not user_is_member:
            Membership.objects.create(user=request.user, circle=circle)
            return redirect('circle_detail', circle_id=circle.id)

    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.circle = circle
        post.save()
        return redirect('circle_detail', circle_id=circle.id)

    return render(request, 'circle_detail.html', {
        'circle': circle,
        'members': members,
        'posts': posts,
        'form': form,
        'user_is_member': user_is_member,
    })




@login_required
def create_circle(request):
    if request.method == 'POST':
        form = CircleForm(request.POST)
        if form.is_valid():
            circle = form.save(commit=False)
            circle.creator = request.user
            circle.save()
            Membership.objects.create(user=request.user, circle=circle)
            return redirect('home')
    else:
        form = CircleForm()
    return render(request, 'create_circle.html', {'form': form})

