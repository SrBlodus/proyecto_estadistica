from django.db.models import Avg
from django.shortcuts import render
from .models import Respuesta_oficial
from .forms import EstadisticasFiltroForm

def estadisticas_egresados(request):
    form = EstadisticasFiltroForm(request.GET or None)
    egresados_filtrados = Respuesta_oficial.objects.all() # Cantidad de Registros Encontrados con los filtros

    total_registros = Respuesta_oficial.objects.count()  # Cantidad General de encuestados

    if form.is_valid():
        if form.cleaned_data["carrera"]:
            egresados_filtrados = egresados_filtrados.filter(carrera=form.cleaned_data["carrera"])
        if form.cleaned_data["facultad"]:
            egresados_filtrados = egresados_filtrados.filter(facultad=form.cleaned_data["facultad"])
        if form.cleaned_data["trabaja_actualmente"]:
            egresados_filtrados = egresados_filtrados.filter(ind_trabaja=form.cleaned_data["trabaja_actualmente"])
        if form.cleaned_data["exterior"]:
            egresados_filtrados = egresados_filtrados.filter(pais=form.cleaned_data["exterior"])
        if form.cleaned_data["valoracion_minima"]:
            egresados_filtrados = egresados_filtrados.filter(valoracion_estudios_trayectoria_profesional__gte=form.cleaned_data["valoracion_minima"])
        if form.cleaned_data["tipo_posgrado"]:
            egresados_filtrados = egresados_filtrados.filter(tipo_posgrado=form.cleaned_data["tipo_posgrado"])

    context = {
        "form": form,
        "total_egresados": egresados_filtrados.count(),
        "promedio_valoracion": egresados_filtrados.aggregate(Avg("valoracion_estudios_trayectoria_profesional"))["valoracion_estudios_trayectoria_profesional__avg"],
        "total_registros": total_registros,
        "egresados_filtrados": egresados_filtrados,
    }
    return render(request, "estadisticas/estadisticas_filtros.html", context)
