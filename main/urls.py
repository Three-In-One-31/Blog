from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('<str:username>/', views.main, name='main'),
    path('<str:username>/create/', views.create, name='create'),

    path('<str:username>/<str:category>/<int:number>/', views.detail, name='detail'),
    path('<str:username>/<str:category>/<int:number>/delete/', views.delete, name='delete'),
    path('<str:username>/<str:category>/<int:number>/update/', views.update, name='update'),

    path('<str:username>/<str:category>/<int:number>/likes-async/', views.likes_async, name='likes-async'),

    path('<str:username>/<str:category>/<int:number>/comments/create/', views.comment_create, name='comment_create'),
    path('<str:username>/<str:category>/<int:number>/comments/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('<str:username>/<str:category>/<int:number>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<str:username>/<str:category>/<int:number>/comments/<int:comment_id>/likes-async/', views.comment_likes_async, name='comment-likes-async'),  
  
    path('<str:username>/<str:category>/<int:number>/comments/<int:comment_id>/replys/create/', views.reply_create, name='reply_create'),
    path('<str:username>/<str:category>/<int:number>/comments/<int:comment_id>/replys/<int:reply_id>/delete/', views.reply_delete, name='reply_delete'),
    path('<str:username>/<str:category>/<int:number>/comments/<int:comment_id>/replys/<int:reply_id>/update/', views.reply_update, name='reply_update'),

    path('<str:username>/category', views.category, name='category'),
    path('<str:username>/category/create', views.Create_category, name='createCategory'),
    path('<str:username>/category/delete', views.Delete_category, name='deleteCategory'),

]