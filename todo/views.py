from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import TodoList


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')

            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {
                                  'form': UserCreationForm(),
                                  'error': 'Ууупс... Похоже это имя уже кто-то использует! Придумай другое.'
                              })

        else:
            return render(request, 'todo/signup_user.html',
                          {
                              'form': UserCreationForm(),
                              'error': 'Ууупс... Похожи пароли не совпадают! Будь внимательнее!'
                          })


def home(request):
    return render(request, 'todo/home.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html',
                          {
                            'form': AuthenticationForm(),
                            'error': 'Имя пользователя и пароль не совпадают'
                          })
        else:
            login(request, user)
            return redirect('current_todos')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def current_todos(request):
    todos = TodoList.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/current_todos.html', {'todos': todos})


@login_required
def completed_todos(request):
    todos = TodoList.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completed_todos.html', {'todos': todos})


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html',
                          {
                              'form': TodoForm(),
                              'error': 'Переданы неверные данные. Повтори попытку.'
                          })


@login_required
def view_todo(request, todo_pk):
    global form
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/view_todo.html',
                          {
                              'todo': todo,
                              'form': form,
                              'error': 'Плохая информация (('
                          })


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')


