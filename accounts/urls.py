from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/follows/', views.follows, name='follows'),
    path('<str:username>/follows/<str:category>/<int:number>', views.followsInDetail, name='followsInDetail'),
    
]