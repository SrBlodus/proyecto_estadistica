from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.db.models import Count
from .models import Respuesta_oficial, Facultad

def inicio(request):
    # Total de encuestados
    total_encuestados = Respuesta_oficial.objects.count()

    # Encuestados por facultad
    encuestados_por_facultad = Facultad.objects.annotate(total_encuestados=Count("respuesta_oficial"))


    context = {
        "total_encuestados": total_encuestados,
        "encuestados_por_facultad": encuestados_por_facultad,
    }

    return render(request, "inicio.html", context)


class CustomLoginView(LoginView):
    template_name = "usuarios/login.html"
    success_url = reverse_lazy("inicio")  # Redirigir al inicio después de loguearse


def custom_logout(request):
    logout(request)  # Cierra la sesión
    return redirect("login")  # Redirige a la vista de inicio de sesión


