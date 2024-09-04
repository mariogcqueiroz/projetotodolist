from django import get_version
from django.views.generic import TemplateView
from .tasks import show_hello_world
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import DemoModel
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, TaskForm
# Create your views here.


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return redirect('login')
            except ValidationError as e:
                form.add_error(None, e.message)
        else:
            form.add_error(None, 'Formulário inválido')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autentica o usuário com as credenciais fornecidas
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Credenciais inválidas.')
    
    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def task_create(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        stat = request.POST.get('stat')

        # Cria a nova tarefa com os dados recebidos
        Task.objects.create(user=request.user, titulo=titulo, descricao=descricao, stat=stat)
        return redirect('task_list')  # Redireciona para a lista de tarefas

    # Se for um GET request, inicializa o formulário vazio
    form = TaskForm()
    
    return render(request, 'task_create.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        stat = request.POST.get('stat')
        
        # Atualiza a tarefa com os dados recebidos
        task.titulo = titulo
        task.descricao = descricao
        task.stat = stat
        task.save()
        
        return redirect('task_list')  # Redireciona para a lista de tarefas

    # Inicializa o formulário com a instância da tarefa
    form = TaskForm(instance=task)
    
    return render(request, 'task_update.html', {'form': form})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect(reverse('task_list'))
    return render(request, 'task_delete.html', {'task': task})

class ShowHelloWorld(TemplateView):
    template_name = 'hello_world.html'

    def get(self, *args, **kwargs):
        show_hello_world.apply()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demo_content'] = DemoModel.objects.all()
        context['version'] = get_version()
        return context
