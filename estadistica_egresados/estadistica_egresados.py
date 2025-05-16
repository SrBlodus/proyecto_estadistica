from django.db.models import Avg
from django.shortcuts import render
from .models import Respuesta_oficial
from .forms import EstadisticasFiltroForm

def estadisticas_egresados(request):
    form = EstadisticasFiltroForm(request.GET or None)
    egresados_filtrados = Respuesta_oficial.objects.all() # Cantidad de Registros Encontrados con los filtros

    total_registros = Respuesta_oficial.objects.count()  # Cantidad General de encuestados

    if form.is_valid():
        if form.cleaned_data["facultad"]:
            egresados_filtrados = egresados_filtrados.filter(facultad=form.cleaned_data["facultad"])

        if form.cleaned_data["carrera"]:
            egresados_filtrados = egresados_filtrados.filter(carrera=form.cleaned_data["carrera"])

        if form.cleaned_data["genero"]:
            egresados_filtrados = egresados_filtrados.filter(genero=form.cleaned_data["genero"])

        if form.cleaned_data["pais"]:
            egresados_filtrados = egresados_filtrados.filter(pais=form.cleaned_data["pais"])

        if form.cleaned_data["estado_civil"]:
            egresados_filtrados = egresados_filtrados.filter(estado_civil=form.cleaned_data["estado_civil"])


        if form.cleaned_data["ano_ingreso_min"]:
            egresados_filtrados = egresados_filtrados.filter(ano_ingreso__gte=form.cleaned_data["ano_ingreso_min"])
        if form.cleaned_data["ano_ingreso_max"]:
            egresados_filtrados = egresados_filtrados.filter(ano_ingreso__lte=form.cleaned_data["ano_ingreso_max"])
        if form.cleaned_data["ano_egreso_min"]:
            egresados_filtrados = egresados_filtrados.filter(ano_egreso__gte=form.cleaned_data["ano_egreso_min"])
        if form.cleaned_data["ano_egreso_max"]:
            egresados_filtrados = egresados_filtrados.filter(ano_egreso__lte=form.cleaned_data["ano_egreso_max"])

        if form.cleaned_data["trabaja_actualmente"]:
            egresados_filtrados = egresados_filtrados.filter(ind_trabaja=form.cleaned_data["trabaja_actualmente"])

        if form.cleaned_data["ano_primer_empleo_min"]:
            egresados_filtrados = egresados_filtrados.filter(ano_primer_empleo__gte=form.cleaned_data["ano_primer_empleo_min"])
        if form.cleaned_data["ano_primer_empleo_max"]:
            egresados_filtrados = egresados_filtrados.filter(ano_primer_empleo__lte=form.cleaned_data["ano_primer_empleo_max"])

        if form.cleaned_data["trabajo_relacionado"]:
            egresados_filtrados = egresados_filtrados.filter(ind_empleo_relacionado_carrera=form.cleaned_data["trabajo_relacionado"])

        if form.cleaned_data["plan_curricular_optimo"]:
            egresados_filtrados = egresados_filtrados.filter(ind_plan_curricular_optimo=form.cleaned_data["plan_curricular_optimo"])

        if form.cleaned_data["valoracion_aprendizaje_docente"]:
            egresados_filtrados = egresados_filtrados.filter(valoracion_aprendizaje_docente__gte=form.cleaned_data["valoracion_aprendizaje_docente"])

        if form.cleaned_data["ind_materias_utiles"]:
            egresados_filtrados = egresados_filtrados.filter(ind_materias_utiles=form.cleaned_data["ind_materias_utiles"])

        if form.cleaned_data["valoracion_impacto_formacion_academica_laboral"]:
            egresados_filtrados = egresados_filtrados.filter(valoracion_impacto_formacion_academica_laboral__gte=form.cleaned_data["valoracion_impacto_formacion_academica_laboral"])

        if form.cleaned_data["ano_primer_empleo_carrera_min"]:
            egresados_filtrados = egresados_filtrados.filter(ano_primer_empleo_carrera__gte=form.cleaned_data["ano_primer_empleo_carrera_min"])

        if form.cleaned_data["ano_primer_empleo_carrera_max"]:
            egresados_filtrados = egresados_filtrados.filter(ano_primer_empleo_carrera__lte=form.cleaned_data["ano_primer_empleo_carrera_max"])

        if form.cleaned_data["ind_oportunidad_desarrollo_profesional"]:
            egresados_filtrados = egresados_filtrados.filter(ind_oportunidad_desarrollo_profesional=form.cleaned_data["ind_oportunidad_desarrollo_profesional"])

        if form.cleaned_data["valoracion_estudios_trayectoria_profesional"]:
            egresados_filtrados = egresados_filtrados.filter(valoracion_estudios_trayectoria_profesional__gte=form.cleaned_data["valoracion_estudios_trayectoria_profesional"])

        if form.cleaned_data["ind_participa_actividad_egresado"]:
            egresados_filtrados = egresados_filtrados.filter(ind_participa_actividad_egresado=form.cleaned_data["ind_participa_actividad_egresado"])

        if form.cleaned_data["ind_interes_participar_actividad_egresado"]:
            egresados_filtrados = egresados_filtrados.filter(ind_interes_participar_actividad_egresado=form.cleaned_data["ind_interes_participar_actividad_egresado"])

        if form.cleaned_data["ind_interes_posgrado"]:
            egresados_filtrados = egresados_filtrados.filter(ind_interes_posgrado=form.cleaned_data["ind_interes_posgrado"])

        if form.cleaned_data["tipo_posgrado"]:
            egresados_filtrados = egresados_filtrados.filter(tipo_posgrado=form.cleaned_data["tipo_posgrado"])

    #  Cálculo de promedios
    promedio_valoracion_estudios = egresados_filtrados.aggregate(Avg("valoracion_estudios_trayectoria_profesional"))["valoracion_estudios_trayectoria_profesional__avg"]
    promedio_aprendizaje_docente = egresados_filtrados.aggregate(Avg("valoracion_aprendizaje_docente"))["valoracion_aprendizaje_docente__avg"]
    promedio_impacto_laboral = egresados_filtrados.aggregate(Avg("valoracion_impacto_formacion_academica_laboral"))["valoracion_impacto_formacion_academica_laboral__avg"]

    #  Contadores: ¿Cuántas personas han respondido las valoraciones?
    total_valoraciones_estudios = egresados_filtrados.filter(valoracion_estudios_trayectoria_profesional__isnull=False).count()
    total_valoraciones_docente = egresados_filtrados.filter(valoracion_aprendizaje_docente__isnull=False).count()
    total_valoraciones_impacto = egresados_filtrados.filter(valoracion_impacto_formacion_academica_laboral__isnull=False).count()

    context = {
        "form": form,
        "total_egresados": egresados_filtrados.count(),
        "prom_valoracion_estudios_trayectoria_profesional": round(promedio_valoracion_estudios, 2) if promedio_valoracion_estudios else "No hay datos",
        "prom_valoracion_aprendizaje_docente": round(promedio_aprendizaje_docente, 2) if promedio_aprendizaje_docente else "No hay datos",
        "prom_valoracion_impacto_formacion_academica_laboral": round(promedio_impacto_laboral, 2) if promedio_impacto_laboral else "No hay datos",
        "total_valoraciones_estudios": total_valoraciones_estudios,
        "total_valoraciones_docente": total_valoraciones_docente,
        "total_valoraciones_impacto": total_valoraciones_impacto,
        "total_registros": total_registros,
        "egresados_filtrados": egresados_filtrados,
    }
    return render(request, "estadisticas/estadisticas_filtros.html", context)



