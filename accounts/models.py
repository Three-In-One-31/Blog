from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.core.files import File
from django.core.files.storage import default_storage

# Create your models here.
class User(AbstractUser):
    def save(self, *args, **kwargs):
        # 사용자가 프로필 이미지를 설정하지 않았을 때
        if not self.profile_image:
            default_image_path = 'static/img/default.png'
            
            # 파일이 존재하지 않으면 static에 존재하는 default.png를 profile에 복사
            if not default_storage.exists(default_image_path):
                with open(default_image_path, 'rb') as default_image:
                    self.profile_image.save('default.png', File(default_image), save=False)

        super().save(*args, **kwargs)

    # 프로필 이미지 크기 변경
    profile_image = ResizedImageField(
        size=[200, 200],
        crop=['middle', 'center'],
        upload_to='profile',
        default='profile/default.png',
    )

    # 팔로워
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)


class Blog(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    introduce = models.TextField(max_length=300, default='나를 소개합니다.')
    
    def __str__(self):
        return self.owner.username