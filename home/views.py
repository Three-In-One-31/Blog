from django.shortcuts import render, redirect
from accounts.models import *
from main.models import *
from main.forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

# 홈
def home(request):
    # 전체 이용자 포스트 확인을 위한 전달 변수
    page = request.GET.get('page_posts','1')
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)
    page_obj_nb = None

    # 로그인한 사용자인 경우
    if request.user.is_authenticated:
        # 이웃 포스트 확인을 위한 전달 변수
        page_nb = request.GET.get('page_nb','1')
        posts_nb = Post.objects.filter(user__in=request.user.followings.all()).order_by('-created_at')
        paginator_nb = Paginator(posts_nb, 3)
        page_obj_nb = paginator_nb.get_page(page_nb)

    context = {
        'posts':page_obj,
        'posts_nb':page_obj_nb,
    }

    return render(request, 'home.html', context)