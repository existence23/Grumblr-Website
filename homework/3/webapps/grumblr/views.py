from django.shortcuts import render, redirect
from grumblr.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import time


@login_required
def home(request):
    context = {}
    posts = Post.objects.all().order_by('-creat_time')
    context['posts'] = posts
    return render(request, 'grumblr/globalstream.html', context)


def self_login(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'grumblr/login.html', context)

    errors = []
    context['errors'] = errors

    if len(User.objects.filter(username=request.POST['username'])) == 0:
        errors.append('User name does not exist!')
        return render(request, 'grumblr/login.html', context)

    current_user = authenticate(username=request.POST['username'], password=request.POST['password'])

    if current_user is not None:
        login(request, current_user)
        return redirect('/grumblr')
    else:
        errors.append('Password Incorrect!')

    return render(request, 'grumblr/login.html', context)


def self_logout(request):
    logout(request)
    return render(request, 'grumblr/login.html')


@login_required
def add_post(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'grumblr/globalstream.html', context)

    errors = []
    context['errors'] = errors

    if not 'new_post' in request.POST or not request.POST['new_post']:
        errors.append('You must type something to present your new post!')
    else:
        new_post = Post(text=request.POST['new_post'], user=request.user, \
                        time_str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), \
                        user_name=request.user.username)
        new_post.save()

    posts = Post.objects.all().order_by('-creat_time')
    context = {'posts' : posts, 'errors' : errors}
    return render(request, 'grumblr/globalstream.html', context)


@login_required
def delete_post(request, post_id):
    errors = []
    user_id = 0
    try:
        post_to_delete = Post.objects.get(id=post_id)
        post_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post did not exist')

    posts = Post.objects.filter(user_name=request.user.username).order_by('-creat_time')

    able_to_delete = []
    able_to_delete.append('True')
    context = {'single_user' : request.user, 'errors' : errors, 'posts': posts, 'able_to_delete':able_to_delete}

    return render(request, 'grumblr/profile.html', context)


@login_required
def delete_account(request):
    errors = []
    try:
        for post in Post.objects.filter(user_name=request.user.username):
            post.delete()
        user_to_delete = request.user
        logout(request)
        user_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The user does not exist')

    return redirect('/grumblr')


@login_required
def check_profile(request, user_id):
    errors = []
    context = {}
    able_to_delete = []

    try:
        user_to_check = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        errors.append("The User does not exist")
        return redirect('/grumblr')
    all_posts = Post.objects.all().order_by('-creat_time')
    posts = all_posts.filter(user_name=user_to_check.username).order_by('-creat_time')
    context['posts'] = posts
    if request.user.id == user_id:
        able_to_delete.append('True')

    context = {'single_user' : user_to_check, 'errors' : errors, 'posts': posts, 'able_to_delete':able_to_delete}
    return render(request, 'grumblr/profile.html', context)


# Create your views here.
def register(request):
    context = {}

    # Still display the registration form is this is a GET request
    if request.method == 'GET':
        return render(request, 'grumblr/register.html', context)

    errors = []
    context['errors'] = errors

    # Check the validity of the form data
    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('Firstname is required')

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Lastname is required')

    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required')
    else:
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password in required')

    if 'password1' in request.POST and request.POST['password1'] \
        and 'password2' in request.POST and request.POST['password2'] \
        and request.POST['password1'] != request.POST['password2']:
        errors.append('Password did not match')

    if len(User.objects.filter(username=request.POST['username'])):
        errors.append('Username is already taken')

    if errors:
        return render(request, 'grumblr/register.html', context)

    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'], \
                                        first_name=request.POST['firstname'], \
                                        last_name=request.POST['lastname'])

    login(request, new_user)
    return redirect('/grumblr')

