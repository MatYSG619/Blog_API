from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создание')

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')
    level = models.PositiveIntegerField(default=0, verbose_name='Уровень')
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children'
    )
