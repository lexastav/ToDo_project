from django.contrib import admin
from .models import TodoList


class TodoAdmin(admin.ModelAdmin):

    """Класс нужен для того, что бы отображалась дата и время создания записи в TodoList"""

    readonly_fields = ('created', )


admin.site.register(TodoList, TodoAdmin)
