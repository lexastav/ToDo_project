from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    """ Сама таблица дел """

    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)  # текстовое поле
    created = models.DateTimeField(auto_now_add=True)  # дата создания
    date_completed = models.DateTimeField(null=True, blank=True)  # дата выполнения
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # foreignkey с помощью
    # которого мы будем осуществлять связь с пользователями
    important = models.BooleanField(default=False)  # атрибут что бы можно было отмечать важна запись или нет

    class Meta:  # используем вспомогательный класс мета для сортировки наших дел
        ordering = ['-created']  # сортировка дел по времени их создания

    def __str__(self):
        return self.title



