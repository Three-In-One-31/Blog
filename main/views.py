from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from accounts.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator

# Create your views here.

# 홈으로 보내는 기능
def home(request):
    return redirect('home:home')


# 블로그 메인 기능
def main(request, username):
    # 블로그 주인
    try:
        owner = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("잘못된 접근입니다.") 
    
    # 포스트 리스트
    postlist = Post.objects.filter(user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    post = sorted_posts.first()
    
    # 페이지네이션
    page = request.GET.get('page_posts','1')
    paginator = Paginator(sorted_posts, 4)
    page_obj = paginator.get_page(page)

    # 카테고리
    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = {}
    for category in categories:
        if category not in categoryList.keys():
            if Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first() == None:
                categoryList[category] = 1
            else:
                categoryList[category] = Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first().id

    category_items = list(categoryList.items())

    # 댓글, 답글 폼
    comment_form = CommentForm()
    reply_form = ReplyForm()
    context = {
        'owner':owner,
        'username':username,
        'postlist':postlist,
        'category':category,
        'sorted_posts':page_obj,
        'categoryList':categoryList,
        'category_items': category_items,
        'post':post,
        'comment_form':comment_form,
        'reply_form':reply_form,
    }

    return render(request, 'main.html', context)


# 포스트 작성 기능
@login_required
def create(request, username):
    # 블로그 주인
    owner = User.objects.get(username=username)

    # 카테고리
    categories = Category.objects.filter(owner_id=owner.id)
    if not categories:
        Category.objects.create(name='기본 카테고리' ,owner=owner)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.category_id = request.POST.get('category')
            post.save()
            return redirect('main:detail', username=username, category=post.category.name ,number=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'categories': categories,
        'owner':owner,
    }

    return render(request, 'writepage.html', context)


# 포스트 상세 페이지
def detail(request, username, category, number):
    # 블로그 주인
    owner = User.objects.get(username=username)

    # 포스트
    postlist = Post.objects.filter(category__name=category, user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    if not postlist.filter(id=number).exists():
        return redirect('main:main', username=username)
    else:
        post = postlist.get(id=number)

    # 페이지네이션
    page = request.GET.get('page_posts','1')
    paginator = Paginator(sorted_posts, 4)
    page_obj = paginator.get_page(page)

    # 카테고리
    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = {}
    for category in categories:
        if category not in categoryList.keys():
            if Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first() == None:
                categoryList[category] = 1
            else:
                categoryList[category] = Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first().id
    category_items = list(categoryList.items())

    # 댓글, 답글 폼
    comment_form = CommentForm()
    reply_form = ReplyForm()

    context = {
        'owner':owner,
        'username':username,
        'category':category,
        'postlist':postlist,
        'sorted_posts':page_obj,
        'post':post,
        'categoryList':categoryList,
        'category_items': category_items,
        'comment_form':comment_form,
        'reply_form':reply_form,
    }

    return render(request, 'detail.html', context)


# 자기 소개 수정 기능
@login_required
def edit_introduce(request, username):
    # 블로그 주인
    owner = User.objects.get(username=username)

    # 요청자가 블로그 주인인지 확인
    if request.user != owner:
        return JsonResponse(status=403)
    
    # 자기 소개 수정
    if request.method == 'POST':
        introduce = request.POST.get('introduce')
        owner.blog.introduce = introduce
        owner.blog.save()

        data = {
            'introduce': owner.blog.introduce,
        }

        return JsonResponse(data)

    return JsonResponse(status=405)

# 포스트 삭제
@login_required
def delete(request, username, category, number):
    post = Post.objects.get(id=number)
    # 사용자 확인
    if request.user == post.user:
        post.delete()

    return redirect('main:main', username=username)


# 포스트 업데이트
@login_required
def update(request, username, category, number):
    # 작성을 위한 정보
    owner = User.objects.get(username=username)
    categories = Category.objects.filter(owner_id=owner.id)
    post = Post.objects.get(id=number)

    # 사용자 확인
    if request.user != post.user:
        return redirect('main:detail', username=username, category=post.category.name, number=number)

    # 수정 데이터 저장
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('main:detail', username=username, category=post.category.name, number=number)
    
    # 요청이 POST가 아닌 경우
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'categories': categories,
    }

    return render(request, 'writepage.html', context)


# 카테고리 관리 기능
@login_required
def category(request, username):
    # 블로그 주인
    owner = User.objects.get(username=username)

    # 요청자가 주인일 경우
    if request.user == owner:
        categories = Category.objects.filter(owner_id=owner.id).order_by('name')
        standard = categories.first()

        # 카테고리가 없는 경우
        if not categories:
            Category.objects.create(name='기본 카테고리' ,owner=owner)

        context = {
            'owner':owner,
            'categories':categories,
            'standard':standard,
        }

        return render(request, 'category/category.html', context)
    
    else:
        return redirect('main:main', username=username)


# 카테고리 생성 기능
@login_required
def Create_category(request, username):
    owner = User.objects.get(username=username)
    category_name = request.POST['categoryName']
    new_categories = Category(name=category_name, owner_id=owner.id)
    new_categories.save()
    categories = Category.objects.filter(owner_id=owner.id).order_by('name')
    context = {
        'owner':owner,
        'categories':categories,
        }
    return render(request, 'category/setting.html', context)


# 카테고리 삭제 기능
@login_required
def Delete_category(request, username):
    category_id = request.POST['categoryId']    
    delete_category = Category.objects.get(id = category_id)
    delete_category.delete()
    return redirect('main:category', username=username)


# 포스트 공감 기능
@login_required
def likes_async(request, username, category, number):
    user = request.user
    post = Post.objects.get(id=number)

    # 요청자가 이미 공감하는 경우
    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False

    # 요청자가 공감하지 않는 경우
    else:
        post.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count': len(post.like_users.all()),
        'username': username,
        'category': category,
        'number': number,
    }

    return JsonResponse(context)


# 댓글 작성 기능
@login_required
def comment_create(request, username, category, number):
    # 블로그 주인
    owner = User.objects.get(username=username)

    # 댓글 작성 폼
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = number
        comment.save()

    data = {
        'owner': owner.username,
        'username': username,
        'category': category,
        'number': number,
        'comment_user_id': comment.user.id,
        'comment_user_profile_image_url': comment.user.profile_image.url,
        'comment_username': comment.user.username,
        'comment_updated_at': comment.updated_at,
        'comment_created_at': comment.created_at,
        'comment_id': comment.id,
        'comment_content': comment.content,
        'like_users': comment.like_users.count()
    }

    return JsonResponse(data)


# 댓글 수정 기능
@login_required
def comment_update(request, username, category, number, comment_id):
    # 수정하려는 댓글
    comment = Comment.objects.get(id=comment_id)

    # 요청자가 댓글 작성자인지 확인
    if request.user != comment.user:
        return JsonResponse(status=403)
    
    # 댓글 수정
    if request.method == 'POST':
        content = request.POST.get('content') 
        comment.content = content
        comment.save()

        data = {
            'content': comment.content,
            'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')

        }

        return JsonResponse(data)
    
    return JsonResponse(status=405)


# 댓글 삭제 기능
@login_required
def comment_delete(request, username, category, number, comment_id):
    # 삭제하려는 댓글
    comment = Comment.objects.get(id=comment_id)

    # 요청자가 댓글 작성자인지 확인
    if request.user != comment.user:
        return redirect('main:detail', username=username, category=category, number=number)
    
    else:
        comment.delete()
        data = {
            'username': username,
            'category': category,
            'number': number,
            'comment_id' : comment_id,
        }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')


# 댓글 공감 기능
@login_required
def comment_likes_async(request, username, category, number, comment_id):
    # 요청자, 댓글 정보
    user = request.user
    post = Post.objects.get(id=number)
    comment = Comment.objects.get(id=comment_id)

    # 요청자가 이미 포스트를 공감하는 경우 
    if user in comment.like_users.all():
        comment.like_users.remove(user)
        status = False

    # 요청자가 포스트를 공감하지 않는 경우
    else:
        comment.like_users.add(user)
        status = True

    context = {
        'username': username,
        'status': status,
        'category': category,
        'number': number,
        'comment_id': comment_id,
        'count': len(comment.like_users.all()),
    }
    
    return JsonResponse(context)


# 답글 생성 기능
@login_required
def reply_create(request, username, category, number, comment_id):
    # 블로그 주인
    owner = User.objects.get(username=username)

    # 답글 작성 폼
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        reply = reply_form.save(commit=False)
        reply.post_id = number
        reply.user = request.user
        reply.comment_id = comment_id
        reply.save()
        
    context = {
        'owner': owner.username,
        'username': username,
        'category': category,
        'number': number,
        'comment_id': reply.comment_id,
        'reply_user_id': reply.user.id,
        'reply_user_profile_image_url': reply.user.profile_image.url,
        'reply_username': reply.user.username,
        'reply_updated_at': reply.updated_at,
        'reply_created_at': reply.created_at,
        'reply_id': reply.id,
        'reply_content': reply.content,
        }

    return JsonResponse(context)


# 답글 삭제 기능
@login_required
def reply_delete(request, username, category, number, comment_id, reply_id):
    # 답글 정보
    reply = Reply.objects.get(id=reply_id)

    # 요청자가 답글 작성자가 아닌 경우
    if request.user != reply.user:
        return redirect('main:detail', username=username, category=category, number=number)
    
    # 요청자가 답글 작성자인 경우
    else:
        reply.delete()
        data = {
            'username': username,
            'category': category,
            'number' : number,
            'comment_id' : comment_id,
            'reply_id' : reply_id,
        }
    
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')


# 답글 수정 기능
@login_required
def reply_update(request, username, category, number, comment_id, reply_id):
    # 답글 정보 
    reply = Reply.objects.get(id=reply_id)

    # 요청자가 답글 작성자가 아닌 경우
    if request.user != reply.user:
        return JsonResponse(status=403)

    # 요청자가 답글 작성자인 경우
    if request.method == 'POST':
        content = request.POST.get('content')
        reply.content = content
        reply.save()
        data = {
            'content': reply.content,
            'updated_at': reply.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse(data)

    return JsonResponse(status=405)