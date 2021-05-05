from django.forms import ModelForm
from .models import TodoList


class TodoForm(ModelForm):

    """Своя собственная форма для списка дел"""
    class Meta:
        model = TodoList
        fields = ['title', 'content', 'important', 'date_completed']




