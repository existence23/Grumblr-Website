from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from grumblr.forms import *
from itertools import chain
from webapps import settings
import time
from django.core.mail import send_mail
from random import Random
from grumblr.models import EmailVerifyRecord


@login_required
def home(request):
    context = {}
    posts = Post.objects.all().order_by('-create_time')
    context['posts'] = posts
    context['form'] = NewPostForm()
    context['current_user'] = request.user
    return render(request, 'grumblr/globalstream.html', context)


def self_login(request):
    context = {}

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'grumblr/modifyPersonalFile/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'grumblr/modifyPersonalFile/login.html', context)
    else:
        login_user = User.objects.get(username=form.cleaned_data['username'])
        login(request, login_user)
        return redirect('/grumblr')


def self_logout(request):
    logout(request)
    context = {}
    context['form'] = LoginForm()
    return render(request, 'grumblr/modifyPersonalFile/login.html', context)


@login_required
def add_post(request):
    context = {}

    if request.method == 'GET':
        context['form'] = NewPostForm()
        return render(request, 'grumblr/globalstream.html', context)

    form = NewPostForm(request.POST)
    context['form'] = form

    if form.is_valid():
        new_post = Post(text=form.cleaned_data['newpost'], user=request.user,
                        time_str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        user_name=request.user.username)
        new_post.save()

    posts = Post.objects.all().order_by('-create_time')
    context['posts'] = posts
    context['form'] = NewPostForm()
    context['current_user'] = request.user
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

    posts = Post.objects.filter(user_name=request.user.username).order_by('-create_time')

    able_to_delete = []
    able_to_delete.append('True')
    context = {'single_user' : request.user, 'errors' : errors, 'posts': posts, 'able_to_delete':able_to_delete}

    return render(request, 'grumblr/profile.html', context)


@login_required
def follow(request, post_id):
    errors = []
    context = {}
    try:
        user_of_post = Post.objects.get(id=post_id).user
        current_user = request.user
        current_user.followers.add(user_of_post)
        current_user.save()
    except ObjectDoesNotExist:
        errors.append('The post did not exist')

    posts = Post.objects.all().order_by('-create_time')
    context['errors'] = errors
    context['posts'] = posts
    context['form'] = NewPostForm()
    context['current_user'] = request.user
    return render(request, 'grumblr/globalstream.html', context)


@login_required
def unfollow(request, post_id):
    errors = []
    context = {}
    try:
        user_of_post = Post.objects.get(id=post_id).user
        current_user = request.user
        current_user.followers.remove(user_of_post)
        current_user.save()
    except ObjectDoesNotExist:
        errors.append('The post did not exist')

    posts = Post.objects.all().order_by('-create_time')
    context['errors'] = errors
    context['posts'] = posts
    context['form'] = NewPostForm()
    context['current_user'] = request.user
    return render(request, 'grumblr/globalstream.html', context)


@login_required
def check_follower(request):
    context = {}
    posts = []
    for user in request.user.followers.all():
        posts = sorted(chain(posts, Post.objects.filter(user_name=user.username)), reverse=True)
    posts = sorted(chain(posts, Post.objects.filter(user_name=request.user.username)), reverse=True)
    context['posts'] = posts
    context['form'] = NewPostForm()
    context['current_user'] = request.user
    context['follower_page'] = True
    return render(request, 'grumblr/globalstream.html', context)


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
    all_posts = Post.objects.all().order_by('-create_time')
    posts = all_posts.filter(user_name=user_to_check.username).order_by('-create_time')
    context['posts'] = posts
    if request.user.id == user_id:
        able_to_delete.append('True')

    context = {'single_user' : user_to_check, 'errors' : errors, 'posts': posts, 'able_to_delete':able_to_delete}
    return render(request, 'grumblr/profile.html', context)


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGg1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email):
    code = random_str(16)
    title = "New Grumblr User: Verify Your Email Adress"
    body = "Please click the link to activate your account in Grumblr: " \
           "http://127.0.0.1:8000/email/{0}".format(code)
    email_record = EmailVerifyRecord(email=email, code=code)
    email_record.save()
    send_mail(subject=title,
              message=body,
              from_email=settings.EMAIL_FROM,
              recipient_list=[email])


def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'grumblr/register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)
    else:
        new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            first_name=form.cleaned_data['firstname'],
                                            last_name=form.cleaned_data['lastname'],
                                            email=form.cleaned_data['email'],
                                            is_active=False)
        send_register_email(new_user.email)

        new_user.save()

        return render(request, 'grumblr/register_confirm_message.html', context)


def verify(request, active_code):
    emailRecord = EmailVerifyRecord.objects.get(code__exact=active_code)
    current_user = User.objects.get(email__exact=emailRecord.email)
    print(request.user)
    current_user.is_active = True
    login(request, current_user)
    current_user.save()
    print(request.user)
    return render(request, 'grumblr/completeFile.html')


def complete(request):
    current_user = request.user
    if 'avatar' in request.FILES:
        avatar = request.FILES.get('avatar')
        current_user.image = avatar
    else:
        current_user.image = "default_photo.jpg"

    current_user.age = request.POST['age']

    current_user.save()
    return redirect('/grumblr')


def check_personal(request):
    if not request.user:
        return render(request, 'grumblr/personalFile.html')
    current_user = request.user
    context = {'user' : current_user}
    return render(request, 'grumblr/personalFile.html', context)


def modify_firstname(request):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyFirstName.html')
    elif request.method == 'POST':
        if not 'firstname' in request.POST or not request.POST['firstname']:
            return render(request, request, 'grumblr/modifyPersonalFile/modifyFirstName.html')
        firstname = request.POST.get('firstname')
        current_user = request.user
        current_user.first_name = firstname
        current_user.save()
        return render(request, 'grumblr/modifyPersonalFile/popup.html', {'firstname' : firstname})


def modify_lastname(request):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyLastName.html')
    elif request.method == 'POST':
        if not 'lastname' in request.POST or not request.POST['lastname']:
            return render(request, request, 'grumblr/modifyPersonalFile/modifyLastName.html')
        lastname = request.POST.get('lastname')
        current_user = request.user
        current_user.last_name = lastname
        current_user.save()
        return render(request, 'grumblr/modifyPersonalFile/popup.html', {'lastname' : lastname})


def modify_username(request):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html')
    elif request.method == 'POST':
        if not 'username' in request.POST or not request.POST['username']:
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html')
        errors = []
        new_username = request.POST.get('username')
        if User.objects.filter(username__exact=new_username):
            errors.append("UserName already been used!")
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html', {'errors':errors})

        current_user = request.user
        current_user.username = new_username
        current_user.save()

        posts = Post.objects.filter(user__exact=current_user)
        for post in posts:
            print(post.text)
            post.user_name = new_username
            post.save()

        return render(request, 'grumblr/modifyPersonalFile/popup.html', {'username' : new_username})


def send_password_email(email):
    code = random_str(16)
    title = "Change Your Grumblr Password: Verify Your Email First"
    body = "Please click the link to confirm your email to change password: " \
           "http://127.0.0.1:8000/change-password/{0}".format(code)
    email_record = EmailVerifyRecord(email=email, code=code, type="password")
    email_record.save()
    send_mail(subject=title,
              message=body,
              from_email=settings.EMAIL_FROM,
              recipient_list=[email])


def modify_password(request, active_code):
    print("arrive here")
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyPassword.html')
    elif request.method == 'POST':
        if not 'old_password' in request.POST or not request.POST['old_password']:
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html')
        if not 'new_password' in request.POST or not request.POST['new_password']:
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html')
        errors = []
        authenticate_user = authenticate(username=request.user.username, password=request.POST['old_password'])
        # print(request.user.username)
        if authenticate_user is None:
            errors.append("Fail to validate your old password!")
            return render(request, 'grumblr/modifyPersonalFile/modifyPassword.html', {'errors' : errors})
        current_user = request.user
        current_user.set_password(request.POST['new_password'])
        current_user.save()
        return render(request, 'grumblr/personalFile.html')


@login_required
def confirm_email(request):
    send_password_email(request.user.email)
    return render(request, 'grumblr/modifyPersonalFile/confirmEmail.html')


def confirm_change_password(request, active_code):

    email = request.user.email
    email_record = EmailVerifyRecord.objects.get(email__exact=email, type__exact="password", code__exact=active_code)

    if email_record is None:
        return render(request, 'grumblr/modifyPersonalFile/failConfirmEmail.html')
    else:
        return render(request, 'grumblr/modifyPersonalFile/modifyPassword.html')


def modify_age(request):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyAge.html')
    elif request.method == 'POST':
        if not 'age' in request.POST or not request.POST['age']:
            return render(request, 'grumblr/modifyPersonalFile/modifyAge.html')
        age = request.POST.get('age')
        current_user = request.user
        current_user.age = age
        current_user.save()
        return render(request, 'grumblr/modifyPersonalFile/popup.html', {'age' : age})


def modify_bio(request):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyBio.html')
    elif request.method == 'POST':
        if not 'bio' in request.POST or not request.POST['bio']:
            return render(request, 'grumblr/modifyPersonalFile/modifyBio.html')
        bio = request.POST.get('bio')
        current_user = request.user
        current_user.bio = bio
        current_user.save()
        return render(request, 'grumblr/modifyPersonalFile/popup.html', {'bio' : bio})


def modify_photo(request):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyPhoto.html')
    elif request.method == 'POST':
        if not 'avatar' in request.FILES or not request.FILES['avatar']:
            return render(request, 'grumblr/modifyPersonalFile/modifyPhoto.html')
        avatar = request.FILES.get('avatar')
        current_user = request.user
        current_user.image = avatar
        current_user.save()
        return render(request, 'grumblr/modifyPersonalFile/popup.html', {'avatar' : avatar})