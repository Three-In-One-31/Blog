from django import forms
from .models import *
from accounts.models import *

# 포스트 작성 폼
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'tag', 'category',)

class EditIntroduceForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('introduce',)
    introduce = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

# 댓글 작성 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'user', 'like_users', )
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': '댓글을 입력해주세요',
                }
            ),
        }
        labels = {
            'content': '',
        }

# 답글 작성 폼
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('user', 'post', 'comment',)
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control mt-2',
                    'rows': '3',
                    'placeholder': '답글을 입력해주세요',
                }
            ),
        }
        labels = {
            'content': '',
        }