
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from todolist.models import Task
from todolist.forms import TaskForm
from django.core import serializers
from django.http import JsonResponse
import datetime

@login_required(login_url='/todolist/login/')
# Create your views here.
def show_todolist(request):
    context = {
        'list_task': Task.objects.filter(user = request.user).order_by('date', 'title', 'description', 'is_finished').values()
    }
    return render(request, 'show_todolist.html', context = context)

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login_user')
    
    context = {'form':form}
    return render(request, 'registrasi.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("todolist:show_todolist"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        pass
    context = {}
    return render(request, 'login.html', context = context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login_user'))
    response.delete_cookie('last_login')
    return response

def new_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = Task()
            new_task.user = request.user
            new_task.date = datetime.datetime.now()
            new_task.title = request.POST.get('judul_task')
            new_task.description = request.POST.get('deskripsi')
            new_task.save()
            return HttpResponseRedirect(reverse('todolist:show_todolist'))
            
    context = {
        'form': TaskForm()
    }
    return render(request, 'new_task.html', context = context)

def change_status(request):
    task = Task.objects.filter(pk = request.GET.get('id'))
    for i in task:
        i.is_finished = not i.is_finished
        i.save() 

    return HttpResponseRedirect(reverse('todolist:show_todolist'))

def delete_task(request, id):
    if request.method == 'DELETE':
        task = Task.objects.filter(pk = id)
        for i in task:
            i.delete()
    return HttpResponseRedirect(reverse('todolist:show_todolist'))

def json(request):
    tasks = Task.objects.filter(user = request.user)
    return HttpResponse(serializers.serialize("json", tasks), content_type = "application/json")

def add(request):
    new_task = Task()
    new_task.user = request.user
    new_task.date = datetime.datetime.now()
    new_task.description = request.POST.get('description')
    new_task.title = request.POST.get('title')
    new_task.is_finished = False
    new_task.save()
    return HttpResponseRedirect(reverse('todolist:show_todolist'))

