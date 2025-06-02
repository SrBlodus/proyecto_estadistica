from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.db.models import Count
from .models import Respuesta_oficial, Facultad
from django.db.models import Count, Q

def inicio(request):
    # Total de encuestados
    total_encuestados = Respuesta_oficial.objects.count()

    # Encuestados por facultad
    encuestados_por_facultad = Facultad.objects.annotate(total_encuestados=Count("respuesta_oficial"))

    # Encuestados por facultad y país de residencia (Paraguay vs. Otros)
    encuestados_por_pais = (
        Respuesta_oficial.objects
        .values("facultad__descripcion")
        .annotate(
            total_paraguay=Count("id", filter=Q(pais__descripcion="Paraguay")),  # Accediendo a la tabla relacionada
            total_extranjero=Count("id", filter=~Q(pais__descripcion="Paraguay")) # Filtrando donde el país es diferente
        )
    )

        # Encuestados por facultad y género
    encuestados_por_genero = (
        Respuesta_oficial.objects
        .values("facultad__descripcion", "genero__descripcion")
        .annotate(total=Count("id"))
    )


    context = {
        "total_encuestados": total_encuestados,
        "encuestados_por_facultad": encuestados_por_facultad,
        "encuestados_por_pais": encuestados_por_pais,
        "encuestados_por_genero": encuestados_por_genero,
    }

    return render(request, "inicio.html", context)


class CustomLoginView(LoginView):
    template_name = "usuarios/login.html"
    success_url = reverse_lazy("inicio")  # Redirigir al inicio después de loguearse


def custom_logout(request):
    logout(request)  # Cierra la sesión
    return redirect("login")  # Redirige a la vista de inicio de sesión


