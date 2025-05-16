from django.shortcuts import render
from django.db.models import Q
from .models import Respuesta_oficial

def lista_encuestados(request):
    query = request.GET.get("q", "")
    encuestados = Respuesta_oficial.objects.all()

    # 🔹 Filtrar por nombre, apellido o número de documento
    if query:
        encuestados = encuestados.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(nro_documento__icontains=query)
        )

    context = {
        "encuestados": encuestados,
        "query": query,
    }
    return render(request, "estadisticas/lista_encuestados.html", context)
