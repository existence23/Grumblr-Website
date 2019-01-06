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
from grumblr.models import EmailVerifyRecord, Comment
from django.http import Http404, HttpResponse
from django.db import transaction


@login_required
def home(request):
    return render(request, 'grumblr/globalstream.html')


def self_login(request):
    context = {}

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'grumblr/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'grumblr/login.html', context)
    else:
        login_user = User.objects.get(username=form.cleaned_data['username'])
        login(request, login_user)
        return redirect('/grumblr')


def self_logout(request):
    logout(request)
    context = {}
    context['form'] = LoginForm()
    return render(request, 'grumblr/login.html', context)


@login_required
def get_changes(request, origin_time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    posts = Post.get_changes(origin_time)
    current_user = request.user.username
    context = {"max_time":max_time, "posts":posts, 'current_user':current_user}
    return render(request, "posts.json", context, content_type='application/json')


@login_required
@transaction.atomic
def get_posts(request, origin_time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    posts = Post.get_posts(origin_time)
    current_user = request.user.username
    context = {'max_time':max_time, 'posts':posts, 'current_user':current_user}
    return render(request, 'posts.json', context, content_type='application/json')


@login_required
@transaction.atomic
def follower_get_changes(request, origin_time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    posts = []
    for user in request.user.followers.all():
        posts = chain(posts, Post.get_changes(origin_time).filter(user_name=user.username))
    posts = chain(posts, Post.get_changes(origin_time).filter(user_name=request.user.username))
    current_user = request.user.username
    context = {"max_time":max_time, "posts":posts, 'current_user':current_user}
    return render(request, "posts.json", context, content_type='application/json')


@login_required
@transaction.atomic
def follower_get_posts(request, origin_time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    posts = []
    for user in request.user.followers.all():
        posts = sorted(chain(posts, Post.get_posts(origin_time).filter(user_name=user.username)))
    posts = sorted(chain(posts, Post.get_posts(origin_time).filter(user_name=request.user.username)))
    current_user = request.user.username
    context = {"max_time":max_time, "posts":posts, 'current_user':current_user}
    return render(request, "posts.json", context, content_type='application/json')


@login_required
@transaction.atomic
def add_post(request, origin_time="1970-01-01T00:00+00:00"):
    if not 'post' in request.POST or not request.POST['post']:
        raise Http404
    else:
        new_post = Post(text=request.POST['post'],  user=request.user,
                    time_str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    user_name=request.user.username)
        new_post.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def delete_post(request, post_id):
    try:
        post_to_delete = Post.objects.get(id=post_id)
        post_to_delete.deleted = True
        post_to_delete.save()
    except ObjectDoesNotExist:
        return Http404
    return HttpResponse("")


@login_required
def comment(request):
    if not 'comment' in request.POST or not request.POST['comment']\
            or not 'post-id' in request.POST or not request.POST['post-id']:
        raise Http404
    else:
        new_comment = Comment(text=request.POST['comment'], user=request.user,
                              time_str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              post=Post.objects.get(id=request.POST['post-id']),
                              user_name=request.user.username)
        new_comment.save()
    context = {'comment':new_comment}
    return render(request, 'comment.json', context, content_type='application/json')


@login_required
def get_comments(request, post_id):
    comments = Comment.objects.filter(post_id=post_id)
    context = {'comments':comments}
    return render(request, 'comments.json', context, content_type='application/json')


@login_required
def follow(request, post_id):
    try:
        user_of_post = Post.objects.get(id=post_id).user
        current_user = request.user
        current_user.followers.add(user_of_post)
        current_user.save()
    except ObjectDoesNotExist:
        return Http404
    return HttpResponse("")


@login_required
def unfollow(request, post_id):
    try:
        user_of_post = Post.objects.get(id=post_id).user
        current_user = request.user
        current_user.followers.remove(user_of_post)
        current_user.save()
    except ObjectDoesNotExist:
        return Http404
    return HttpResponse("")


@login_required
def check_follower(request):
    return render(request, 'grumblr/followerStream.html')


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
    context = {"user_id":user_id}
    return render(request, 'grumblr/profile.html', context)


@login_required
def get_profile_posts(request, user_id):
    max_time = Post.get_max_time()
    posts = Post.objects.filter(user_name=User.objects.get(id=user_id), deleted=False)
    current_user = request.user.username
    context = {"max_time": max_time, "posts": posts, 'current_user': current_user}
    return render(request, 'posts.json', context, content_type='application/json')


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
           "http://13.59.88.183/email/{0}".format(code)
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
    current_user.is_active = True
    login(request, current_user)
    current_user.save()
    return render(request, 'grumblr/completeFile.html')


def complete(request):
    current_user = request.user
    if 'avatar' in request.FILES:
        avatar = request.FILES.get('avatar')
        current_user.image = avatar
    else:
        current_user.image = "default_photo.jpg"
    if str(request.POST['age']).isdigit():
        current_user.age = request.POST['age']
        current_user.save()
        return redirect('/grumblr')
    else:
        return render(request, 'grumblr/completeFile.html')

def check_personal(request):
    if not request.user:
        return render(request, 'grumblr/personalFile.html')
    current_user = request.user
    context = {'user' : current_user}
    return render(request, 'grumblr/personalFile.html', context)


def modify_firstname(request):
    context = {}
    if request.method == 'GET':
        context['modify_firstname_form'] = ModifyFirstnameForm()
        return render(request, 'grumblr/modifyPersonalFile/modifyFirstName.html', context)
    else:
        modify_firstname_form = ModifyFirstnameForm(request.POST)
        context['modify_firstname_form'] = modify_firstname_form

        if not modify_firstname_form.is_valid():
            return render(request, 'grumblr/modifyPersonalFile/modifyFirstName.html', context)
        else:
            firstname = modify_firstname_form.cleaned_data['firstname']
            current_user = request.user
            current_user.first_name = firstname
            current_user.save()
            return render(request, 'grumblr/modifyPersonalFile/popup.html', {'firstname': firstname})


def modify_lastname(request):
    context = {}
    if request.method == 'GET':
        context['modify_lastname_form'] = ModifyLastnameForm()
        return render(request, 'grumblr/modifyPersonalFile/modifyLastName.html', context)
    else:
        modify_lastname_form = ModifyLastnameForm(request.POST)
        context['modify_lastname_form'] = modify_lastname_form

        if not modify_lastname_form.is_valid():
            return render(request, 'grumblr/modifyPersonalFile/modifyLastName.html', context)
        else:
            lastname = modify_lastname_form.cleaned_data['lastname']
            current_user = request.user
            current_user.last_name = lastname
            current_user.save()
            return render(request, 'grumblr/modifyPersonalFile/popup.html', {'lastname': lastname})


def modify_username(request):
    context = {}
    if request.method == 'GET':
        context['modify_username_form'] = ModifyUsernameForm()
        return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html', context)
    else:
        modify_username_form = ModifyUsernameForm(request.POST)
        context['modify_username_form'] = modify_username_form

        if not modify_username_form.is_valid():
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html', context)
        else:
            username = modify_username_form.cleaned_data['username']
            current_user = request.user
            current_user.username = username
            current_user.save()

            posts = Post.objects.filter(user__exact=current_user)
            for post in posts:
                print(post.text)
                post.user_name = username
                post.save()

            return render(request, 'grumblr/modifyPersonalFile/popup.html', {'username': username})


def send_password_email(email):
    code = random_str(16)
    title = "Change Your Grumblr Password: Verify Your Email First"
    body = "Please click the link to confirm your email to change password: " \
           "http://13.59.88.183/change-password/{0}".format(code)
    email_record = EmailVerifyRecord(email=email, code=code, type="password")
    email_record.save()
    send_mail(subject=title,
              message=body,
              from_email=settings.EMAIL_FROM,
              recipient_list=[email])


def modify_password(request, active_code):
    if request.method == 'GET':
        return render(request, 'grumblr/modifyPersonalFile/modifyPassword.html')
    elif request.method == 'POST':
        if not 'old_password' in request.POST or not request.POST['old_password']:
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html')
        if not 'new_password' in request.POST or not request.POST['new_password']:
            return render(request, 'grumblr/modifyPersonalFile/modifyUserName.html')
        errors = []
        authenticate_user = authenticate(username=request.user.username, password=request.POST['old_password'])
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
    context = {}
    if request.method == 'GET':
        context['modify_age_form'] = ModifyAgeForm()
        return render(request, 'grumblr/modifyPersonalFile/modifyAge.html', context)
    else:
        modify_age_form = ModifyAgeForm(request.POST)
        context['modify_age_form'] = modify_age_form

        if not modify_age_form.is_valid():
            return render(request, 'grumblr/modifyPersonalFile/modifyAge.html', context)
        else:
            age = modify_age_form.cleaned_data['age']
            current_user = request.user
            current_user.age = age
            current_user.save()
            return render(request, 'grumblr/modifyPersonalFile/popup.html', {'age': age})


def modify_bio(request):
    context = {}
    if request.method == 'GET':
        context['modify_bio_form'] = ModifyBioForm()
        return render(request, 'grumblr/modifyPersonalFile/modifyBio.html', context)
    else:
        modify_bio_form = ModifyBioForm(request.POST)
        context['modify_bio_form'] = modify_bio_form

        if not modify_bio_form.is_valid():
            return render(request, 'grumblr/modifyPersonalFile/modifyBio.html', context)
        else:
            bio = modify_bio_form.cleaned_data['bio']
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
