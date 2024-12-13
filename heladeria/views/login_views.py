from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

def iniciar(request):
    if request.method == 'GET':
        return render(request, "iniciar.html", {'form': AuthenticationForm})
    else:
        name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=name, password=password)
        if user is None:
            messages.success(request, 'Usuario y/o contraseña incorrecto!')
            return render(request, "iniciar.html", {'form': AuthenticationForm})
        else:
            login(request, user)
            return redirect('inicio')

def registro(request):
    if request.method == 'GET':
        return render(request, "registro.html", {'form': UserCreationForm})
    else:
        if request.POST["password1"] != request.POST["password2"]:
            messages.error(request, 'Las contraseñas no coinciden!')
            return render(request, "registro.html", {'form': UserCreationForm})
        elif len(request.POST["password1"]) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, "registro.html", {'form': UserCreationForm})
        else:
            name = request.POST["username"]
            password = request.POST["password2"]
            user = User.objects.create_user(username=name, password=password)
            user.save()
            messages.success(request, 'Usuario creado con éxito!')
            return render(request, "registro.html", {'form': UserCreationForm})

@login_required
def home(request):
    return render(request, "principal.html")

def salir(request):
    logout(request)
    return redirect('iniciar')
