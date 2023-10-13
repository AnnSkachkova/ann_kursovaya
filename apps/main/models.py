from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    token = models.CharField(max_length=32, verbose_name='Токен')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    def __str__(self) -> str:
        return f"Токен {self.token} для пользователя {self.user}"
    
    class Meta:
        verbose_name = 'Токен пользователя'
        verbose_name_plural = 'Токенты пользователей'
        
        