from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout

def inicio(request):
    return render(request, "inicio.html")



class CustomLoginView(LoginView):
    template_name = "usuarios/login.html"
    success_url = reverse_lazy("inicio")  # Redirigir al inicio después de loguearse


def custom_logout(request):
    logout(request)  # Cierra la sesión
    return redirect("login")  # Redirige a la vista de inicio de sesión


