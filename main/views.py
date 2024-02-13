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
def home(request):
    return redirect('home:home')

def main(request, username):
    try:
        owner = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("Something went wrong.") 
    postlist = Post.objects.filter(user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    post = sorted_posts.first()

    page = request.GET.get('page_posts','1')
    paginator = Paginator(sorted_posts, 4)
    page_obj = paginator.get_page(page)

    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = {}
    for category in categories:
        if category not in categoryList.keys():
            if Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first() == None:
                categoryList[category] = 1
            else:
                categoryList[category] = Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first().id

    category_items = list(categoryList.items())

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

@login_required
def create(request, username):
    owner = User.objects.get(username=username)
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

def detail(request, username, category, number):
    owner = User.objects.get(username=username)
    postlist = Post.objects.filter(category__name=category, user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    if not postlist.filter(id=number).exists():
        return redirect('main:main', username=username)
    else:
        post = postlist.get(id=number)

    page = request.GET.get('page_posts','1')
    paginator = Paginator(sorted_posts, 4)
    page_obj = paginator.get_page(page)

    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = {}
    for category in categories:
        if category not in categoryList.keys():
            if Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first() == None:
                categoryList[category] = 1
            else:
                categoryList[category] = Post.objects.filter(category__name=category, user_id=owner.id).order_by('-id').first().id
    category_items = list(categoryList.items())

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

@login_required
def delete(request, username, category, number):
    post = Post.objects.get(id=number)
    if request.user == post.user:
        post.delete()

    return redirect('main:main', username=username)

@login_required
def update(request, username, category, number):
    owner = User.objects.get(username=username)
    categories = Category.objects.filter(owner_id=owner.id)
    post = Post.objects.get(id=number)
    if request.user != post.user:
        return redirect('main:detail', username=username, category=post.category.name, number=number)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('main:detail', username=username, category=post.category.name, number=number)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'categories': categories,
    }
    return render(request, 'writepage.html', context)

@login_required
def category(request, username):
    owner = User.objects.get(username=username)
    if request.user == owner:
        categories = Category.objects.filter(owner_id=owner.id).order_by('name')
        standard = categories.first()
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

@login_required
def Delete_category(request, username):
    category_id = request.POST['categoryId']    
    delete_category = Category.objects.get(id = category_id)
    delete_category.delete()
    return redirect('main:category', username=username)

@login_required
def likes_async(request, username, category, number):
    user = request.user
    post = Post.objects.get(id=number)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False

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

@login_required
def comment_create(request, username, category, number):
    owner = User.objects.get(username=username)
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


@login_required
def comment_update(request, username, category, number, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.user != comment.user:
        return JsonResponse(status=403)
    
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


@login_required
def comment_delete(request, username, category, number, comment_id):
    comment = Comment.objects.get(id=comment_id)

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

@login_required
def comment_likes_async(request, username, category, number, comment_id):
    user = request.user
    post = Post.objects.get(id=number)
    comment = Comment.objects.get(id=comment_id)

    if user in comment.like_users.all():
        comment.like_users.remove(user)
        status = False

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

@login_required
def reply_create(request, username, category, number, comment_id):
    owner = User.objects.get(username=username)
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


@login_required
def reply_delete(request, username, category, number, comment_id, reply_id):
    reply = Reply.objects.get(id=reply_id)

    if request.user != reply.user:
        return redirect('main:detail', username=username, category=category, number=number)
    
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


@login_required
def reply_update(request, username, category, number, comment_id, reply_id):
    reply = Reply.objects.get(id=reply_id)

    if request.user != reply.user:
        return JsonResponse(status=403)

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