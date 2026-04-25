from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default='./images/no-image.png', verbose_name='Картинка')
    description = models.TextField(max_length=2000, blank=True, null=False, verbose_name='Описание')
    created_at = models.DateField(auto_now_add=True)


