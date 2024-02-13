from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import *
from main.models import *
from django.core.files import File
from django.core.files.storage import default_storage

# Create your views here.
def signup(request):
    if request.method == 'POST':
        # 사용자가 프로필 이미지를 설정하지 않았을 때
        if not request.FILES.get('profile_image'):
            default_image_path = 'static/img/default.png'
            profile_image_path = 'profile/default.png'
            
            # 파일이 존재하지 않으면 복사
            if not default_storage.exists(profile_image_path):
                with open(default_image_path, 'rb') as default_image:
                    default_storage.save(profile_image_path, File(default_image))  

        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_blog = Blog(owner = user)
            std_category = Category.objects.create(owner=user, name='기본 카테고리')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_blog.save()
            
            user = authenticate(username=username, password = password)
            auth_login(request, user)
            return redirect('home:home')
    else:
        form = UserForm()
    context ={
        'form': form,
    }
    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, form.get_user())
            next_url = request.GET.get('next')
            return redirect('home:home')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form, 
    }
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home:home')

def follows(request, username):
    me = request.user
    you = User.objects.get(username=username)

    if you in me.followings.all():
        me.followings.remove(you)
    else:
        me.followings.add(you)

    return redirect('home:home')

def followsInDetail(request, username, category, number):
    me = request.user
    you = User.objects.get(username=username)
    category = category

    if you in me.followings.all():
        me.followings.remove(you)
    else:
        me.followings.add(you)

    return redirect('main:detail', username=username, category=category, number=number)    