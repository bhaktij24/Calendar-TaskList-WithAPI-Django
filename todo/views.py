from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import TodoList
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup_user(request):

    if request.method == "GET":
        return render(request, 'todo/signupUser.html', {'form': UserCreationForm()})
    else:
        # New user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupUser.html', {'form': UserCreationForm(),'error': "Username already taken. Please try some other username or login with the same username."})

        else:
            #Password not match
            return render(request, 'todo/signupUser.html', {'form': UserCreationForm(),'error': "Passwords did not match"})

@login_required
def currenttodos(request):
        todo = TodoList.objects.filter(user=request.user, dateCompleted__isnull=True)
        return render(request, 'todo/currenttodos.html',{'todo':todo})

@login_required
def completed_todos(request):
    todo = TodoList.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('dateCompleted')
    return render(request, 'todo/completedtodos.html',{'todo':todo})

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homePage')

def login_user(request):
    if request.method == "GET":
        return render(request, 'todo/loginUser.html', {'form': AuthenticationForm()})
    else:
        # New user
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginUser.html',{'form': AuthenticationForm(),'error':'Some problem with username/password. Try again!'})
        else:
            login(request,user)
            return redirect('currenttodos')
            #todos = TodoList.objects.all()
            #return render(request,'todo/currenttodos.html', {'todo':todos})


def home_page(request):
    return render(request, 'todo/home.html')

@login_required
def create_todo(request):
    if request.method == "GET":
        return render(request,'todo/createTodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/createTodo.html', {'form':TodoForm(),'error':'Bad Data. Please retry!'})

@login_required
def view_todos(request, todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodos.html',{'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodos.html', {'form':TodoForm(),'error':'Bad Data. Please retry!'})

@login_required
def complete_todos(request,todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def delete_todos(request,todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')    