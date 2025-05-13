from dateutil import parser
from django.shortcuts import render,redirect
from django.http import HttpResponse
import csv
from .models import Respuesta_borrador, Respuesta_oficial, Facultad, Carrera, CampusSede, Genero, EstadoCivil, Pais, \
    TipoPosgrado
from .forms import CSVUploadForm
from django.contrib import messages
import hashlib

def imp_exp_archivos_inicio(request):
    return render(request, "imp-exp-archivos/inicio_imp_exp_archivos.html")

def importar_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES["archivo_csv"]
            reader = csv.DictReader(archivo.read().decode("utf-8").splitlines())

            for row in reader:
                try:
                    # Convertir la marca temporal al formato correcto
                    marca_temporal = row.get("Marca temporal", "").strip()
                    #print(f"Fecha convertida: {marca_temporal}")

                    # Reemplazar caracteres especiales y limpiar el formato
                    marca_temporal = marca_temporal.replace("p. m.", "PM").replace("a. m.", "AM").replace("\xa0"," ").replace("GMT-3", "")
                    #print(f"Fecha convertida: {marca_temporal}")
                    try:
                        fecha_hora_encuesta = parser.parse(marca_temporal)
                    except ValueError:
                        fecha_hora_encuesta = None  #  Si hay error, guarda `None`

                    #print(f"Fecha convertida: {fecha_hora_encuesta}")


                    # Obtener los nro_documento e IDs correspondientes para buscar duplicados
                    nro_documento = row.get("Cédula de Identidad Paraguaya Nº", "").strip()
                    facultad_obj = Facultad.objects.filter(descripcion=row.get("Facultad", "").strip()).first()
                    carrera_obj = Carrera.objects.filter(descripcion=row.get("Carrera", "").strip()).first()
                    campus_sede_obj = CampusSede.objects.filter(descripcion=row.get("Campus o sede de promoción", "").strip()).first()

                    # Verificar si el registro ya existe en `Respuesta_oficial`
                    existe = Respuesta_oficial.objects.filter(
                        nro_documento=nro_documento,
                        facultad=facultad_obj,
                        carrera=carrera_obj,
                        campus_sede=campus_sede_obj
                    ).first()


                    estado = "D" if existe else "P"

                    if existe:
                        fecha_hora_encuesta_anterior = existe.fecha_hora_encuesta
                    else:
                        fecha_hora_encuesta_anterior = None

                    # Generar un hash único del registro
                    datos_unicos = f"{nro_documento}|{fecha_hora_encuesta}"
                    hash_registro = hashlib.md5(datos_unicos.encode()).hexdigest()

                    # Verificar si el registro ya existe en `Respuesta_borrador`
                    existe_borrador = Respuesta_borrador.objects.filter(hash_valor=hash_registro).exists()

                    if not existe_borrador:
                        # Aquí buscamos el siguiente nro. de registro
                        ultimo_nro_registro = Respuesta_borrador.objects.order_by("-nro_registro").first()
                        nuevo_nro_registro = (ultimo_nro_registro.nro_registro + 1) if ultimo_nro_registro else 1

                        # Convertir valores vacíos a None antes de insertar
                        def convertir_a_entero(valor):
                            return int(valor) if valor.strip() and valor.isdigit() else None

                        ano_primer_empleo = convertir_a_entero(
                            row.get("Año en obtener primer empleo o emprendimiento", ""))
                        ano_primer_empleo_carrera = convertir_a_entero(
                            row.get("Año en obtener su primer empleo/emprendimiento que este relacionado a su carrera", ""))

                        valoracion_aprendizaje_docente = convertir_a_entero(
                            row.get("¿Cómo valoras los aprendizajes que los docentes te ayudaron a adquirir para tu desarrollo profesional?", ""))
                        valoracion_impacto_formacion_academica_laboral = convertir_a_entero(
                            row.get("¿Cómo evaluarías el impacto de la formación académica en tu situación laboral actual?",""))
                        valoracion_estudios_trayectoria_profesional =convertir_a_entero(
                            row.get("¿Cómo valorarías el impacto de tus estudios en tu trayectoria profesional?",""))




                        # Todas las respuestas base que tengan Sí o No serán definidas aquí
                        preguntas_si_no = {
                            "Trabaja o emprende actualmente": "ind_trabajo",
                            "¿Participaste en actividades, seminarios o charlas sobre tu carrera después de egresar?": "ind_participa_actividad_egresado",
                            "¿Te gustaría seguir participando en actividades organizadas por tu facultad?":"ind_interes_participar_actividad_egresado",
                            "¿Has considerado realizar un posgrado o especialización después de egresar?":"ind_interes_posgrado",
                            "¿Su empleo o emprendimiento esta relacionado a su carrera?":"ind_empleo_relacionado_carrera",
                            "¿Consideras que el plan curricular fue óptimo para enfrentar los desafíos laborales?":"ind_plan_curricular_optimo",
                            "¿Las materias en general que cursaste te fueron útiles en tu desempeño laboral?":"ind_materias_utiles",
                            "¿Has tenido oportunidades de desarrollo profesional, como ascensos o promociones?":"ind_oportunidad_desarrollo_profesional",
                        }

                        # Iterar sobre las preguntas y asignar "S", "N" o mantener vacío
                        respuestas_si_no = {}
                        for pregunta, variable in preguntas_si_no.items():
                            respuesta = row.get(pregunta, "").strip()
                            respuestas_si_no[variable] = "S" if respuesta == "Sí" else "N" if respuesta == "No" else ""



                        # Guardar en el borrador con valores sin convertir
                        Respuesta_borrador.objects.create(
                            fecha_hora_encuesta = fecha_hora_encuesta,
                            fecha_hora_encuesta_anterior = fecha_hora_encuesta_anterior,
                            nro_registro=nuevo_nro_registro,
                            correo=row.get("Nombre de usuario", "").strip(),
                            nro_telefono=row.get("Número de teléfono", "").strip(),
                            nombres=row.get("Nombres", "").strip(),
                            apellidos=row.get("Apellidos", "").strip(),
                            nro_documento=nro_documento,
                            genero=row.get("Género", "").strip(),
                            pais=row.get("País actual de residencia", "").strip(),
                            ciudad=row.get("Ciudad actual de residencia", "").strip(),
                            estado_civil=row.get("Estado Civil", "").strip(),
                            campus_sede=row.get("Campus o sede de promoción", "").strip(),
                            facultad=row.get("Facultad", "").strip(),
                            carrera=row.get("Carrera", "").strip(),
                            ano_ingreso=row.get("Año de ingreso", ""),
                            ano_egreso=row.get("Año de egreso", ""),
                            ind_trabaja=respuestas_si_no["ind_trabajo"],
                            ano_primer_empleo=ano_primer_empleo,
                            ind_empleo_relacionado_carrera = respuestas_si_no["ind_empleo_relacionado_carrera"],
                            ind_plan_curricular_optimo=respuestas_si_no["ind_plan_curricular_optimo"],
                            valoracion_aprendizaje_docente=valoracion_aprendizaje_docente,
                            ind_materias_utiles = respuestas_si_no["ind_materias_utiles"],
                            valoracion_impacto_formacion_academica_laboral = valoracion_impacto_formacion_academica_laboral,
                            opcional_aprendizajes_no_curriculares = row.get("¿Qué aprendizajes no curriculares (actitudes, compromiso, liderazgo) consideras que fueron fundamentales para tu desarrollo laboral?(Opcional)","").strip(),
                            ano_primer_empleo_carrera=ano_primer_empleo_carrera,
                            ind_oportunidad_desarrollo_profesional = respuestas_si_no["ind_oportunidad_desarrollo_profesional"],
                            valoracion_estudios_trayectoria_profesional = valoracion_estudios_trayectoria_profesional,
                            opcional_influencia_en_trayectoria=row.get("¿Cómo o en qué consideras que la formación recibida haya influido en tu trayectoria profesional?(Opcional)","").strip(),
                            ind_participa_actividad_egresado = respuestas_si_no["ind_participa_actividad_egresado"],
                            ind_interes_participar_actividad_egresado = respuestas_si_no["ind_interes_participar_actividad_egresado"],
                            ind_interes_posgrado = respuestas_si_no["ind_interes_posgrado"],
                            tipo_posgrado = row.get("¿Qué tipo de posgrado crees que sería más relevante para el desarrollo profesional?", "").strip(),
                            opcional_area_posgrado = row.get("¿Cuáles son las áreas que consideras que son necesarias para un posgrado para egresados de tu carrera? Ejemplo: Ciberseguridad, Análisis de Datos, etc.(Opcional)", "").strip(),
                            opcional_estrategia_convocatoria = row.get("¿Qué estrategias podría implementar la facultad para mejorar la convocatoria de egresados?(Opcional)", "").strip(),
                            opcional_contacto_carrera = row.get("¿Has mantenido contacto con docentes o compañeros de tu carrera para desarrollar oportunidades laborales?(Opcional)", "").strip(),
                            hash_valor = hash_registro,
                            estado=estado,
                        )
                    else:
                        messages.warning(request, f"Registro con C.I. Nº {nro_documento} ya se ha importado a la tabla preliminar. ")

                except Exception as e:
                    return HttpResponse(f"Error procesando el registro Nº {nuevo_nro_registro}: {e}")

            return redirect("ver_borrador")

    else:
        form = CSVUploadForm()

    return render(request, "imp-exp-archivos/importar_csv.html", {"form": form})

def ver_borrador(request):
    if request.method == "POST":
        seleccionadas = request.POST.getlist("seleccionadas")

        accion = request.POST.get("accion")  #  Detectar si se quiere exportar o eliminar

        if accion == "eliminar":
            # Eliminar los registros seleccionados
            registros_eliminados = Respuesta_borrador.objects.filter(id__in=seleccionadas).delete()
            messages.success(request, f"{registros_eliminados[0]} registros eliminados correctamente.")
            return redirect("ver_borrador")

        registros_exportados = 0

        for id_respuesta in seleccionadas:
            try:
                borrador = Respuesta_borrador.objects.get(id=id_respuesta)



                #  Convertir normalizadas a sus respectivos IDs
                facultad_obj = Facultad.objects.filter(descripcion=borrador.facultad).first()
                carrera_obj = Carrera.objects.filter(descripcion=borrador.carrera).first()
                campus_sede_obj = CampusSede.objects.filter(descripcion=borrador.campus_sede).first()
                genero_obj = Genero.objects.filter(descripcion=borrador.genero).first()
                estado_civil_obj = EstadoCivil.objects.filter(descripcion=borrador.estado_civil).first()
                pais_obj = Pais.objects.filter(descripcion=borrador.pais).first()
                tipo_posgrado_obj = TipoPosgrado.objects.filter(descripcion=borrador.tipo_posgrado).first()

                #  Validaciónes para evitar errores si no encuentra los IDs

                if not campus_sede_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Campus/Sede no encontrado.")
                    continue


                if not facultad_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Facultad no encontrada.")
                    continue

                if not carrera_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Carrera no encontrada.")
                    continue

                if not genero_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Género no encontrado.")
                    continue

                if not estado_civil_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Estado Civil no encontrado.")
                    continue

                if not pais_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: País no encontrado.")
                    continue

                if not tipo_posgrado_obj:
                    messages.error(request, f"Existe un registro con una respuesta no definida para el tipo de posgrado. Verifique el Google Forms con la lista de tipos de posgrado.")
                    continue


                registro_existente = Respuesta_oficial.objects.filter(
                    nro_documento=borrador.nro_documento,
                    facultad=facultad_obj,
                    carrera=carrera_obj,
                    campus_sede=campus_sede_obj
                ).first()


                #  Crear el registro en `Respuesta_oficial` con los IDs en lugar de los nombres
                if registro_existente:
                    #  Actualizar registro existente en lugar de crear uno nuevo
                    registro_existente.fecha_hora_encuesta = borrador.fecha_hora_encuesta
                    registro_existente.correo = borrador.correo
                    registro_existente.nro_telefono = borrador.nro_telefono
                    registro_existente.nombres = borrador.nombres
                    registro_existente.apellidos = borrador.apellidos
                    registro_existente.genero = genero_obj
                    registro_existente.pais = pais_obj
                    registro_existente.ciudad = borrador.ciudad
                    registro_existente.estado_civil = estado_civil_obj
                    registro_existente.ano_ingreso = borrador.ano_ingreso
                    registro_existente.ano_egreso = borrador.ano_egreso
                    registro_existente.ind_trabaja = borrador.ind_trabaja
                    registro_existente.ano_primer_empleo = borrador.ano_primer_empleo
                    registro_existente.ind_empleo_relacionado_carrera = borrador.ind_empleo_relacionado_carrera
                    registro_existente.ind_plan_curricular_optimo = borrador.ind_plan_curricular_optimo
                    registro_existente.valoracion_aprendizaje_docente = borrador.valoracion_aprendizaje_docente
                    registro_existente.ind_materias_utiles = borrador.ind_materias_utiles
                    registro_existente.valoracion_impacto_formacion_academica_laboral = borrador.valoracion_impacto_formacion_academica_laboral
                    registro_existente.opcional_aprendizajes_no_curriculares = borrador.opcional_aprendizajes_no_curriculares
                    registro_existente.ano_primer_empleo_carrera = borrador.ano_primer_empleo_carrera
                    registro_existente.ind_oportunidad_desarrollo_profesional = borrador.ind_oportunidad_desarrollo_profesional
                    registro_existente.valoracion_estudios_trayectoria_profesional = borrador.valoracion_estudios_trayectoria_profesional
                    registro_existente.opcional_influencia_en_trayectoria = borrador.opcional_influencia_en_trayectoria
                    registro_existente.ind_participa_actividad_egresado = borrador.ind_participa_actividad_egresado
                    registro_existente.ind_interes_participar_actividad_egresado = borrador.ind_interes_participar_actividad_egresado
                    registro_existente.ind_interes_posgrado = borrador.ind_interes_posgrado
                    registro_existente.tipo_posgrado = tipo_posgrado_obj
                    registro_existente.opcional_area_posgrado = borrador.opcional_area_posgrado
                    registro_existente.opcional_estrategia_convocatoria = borrador.opcional_estrategia_convocatoria
                    registro_existente.opcional_contacto_carrera = borrador.opcional_contacto_carrera
                    registro_existente.save()  # Guardar cambios en `Respuesta_oficial`
                else:
                    #  Crear nuevo registro si no existe en `Respuesta_oficial`
                    Respuesta_oficial.objects.create(
                        fecha_hora_encuesta=borrador.fecha_hora_encuesta,
                        correo=borrador.correo,
                        nro_telefono=borrador.nro_telefono,
                        nombres=borrador.nombres,
                        apellidos=borrador.apellidos,
                        nro_documento=borrador.nro_documento,
                        genero=genero_obj,
                        pais=pais_obj,
                        ciudad=borrador.ciudad,
                        estado_civil=estado_civil_obj,
                        campus_sede=campus_sede_obj,
                        facultad=facultad_obj,
                        carrera=carrera_obj,
                        ano_ingreso=borrador.ano_ingreso,
                        ano_egreso=borrador.ano_egreso,
                        ind_trabaja=borrador.ind_trabaja,
                        ano_primer_empleo=borrador.ano_primer_empleo,
                        ind_empleo_relacionado_carrera = borrador.ind_empleo_relacionado_carrera,
                        ind_plan_curricular_optimo = borrador.ind_plan_curricular_optimo,
                        valoracion_aprendizaje_docente = borrador.valoracion_aprendizaje_docente,
                        ind_materias_utiles = borrador.ind_materias_utiles,
                        valoracion_impacto_formacion_academica_laboral = borrador.valoracion_impacto_formacion_academica_laboral,
                        opcional_aprendizajes_no_curriculares = borrador.opcional_aprendizajes_no_curriculares,

                        ano_primer_empleo_carrera=borrador.ano_primer_empleo_carrera,
                        ind_oportunidad_desarrollo_profesional = borrador.ind_oportunidad_desarrollo_profesional,
                        valoracion_estudios_trayectoria_profesional = borrador.valoracion_estudios_trayectoria_profesional,
                        opcional_influencia_en_trayectoria = borrador.opcional_influencia_en_trayectoria,

                        ind_participa_actividad_egresado=borrador.ind_participa_actividad_egresado,
                        ind_interes_participar_actividad_egresado=borrador.ind_interes_participar_actividad_egresado,
                        ind_interes_posgrado = borrador.ind_interes_posgrado,
                        tipo_posgrado=tipo_posgrado_obj,
                        opcional_area_posgrado=borrador.opcional_area_posgrado,
                        opcional_estrategia_convocatoria=borrador.opcional_estrategia_convocatoria,
                        opcional_contacto_carrera=borrador.opcional_contacto_carrera,

                    )
                # Marcar el registro como exportado
                borrador.estado = "E"
                borrador.save()
                registros_exportados += 1



            except Exception as e:
                messages.error(request, f"Error procesando registro Nº {borrador.nro_registro}: {str(e)}")

        if registros_exportados > 0:
            messages.success(request, f"Se han exportado correctamente {registros_exportados} respuestas.")
        else:
            messages.warning(request, "No se exportaron respuestas. Verifica los errores.")
        return redirect("ver_borrador")

    estado_filtro = request.GET.get("estado", "T")  # Obtener el estado desde la URL (por defecto "T"(PENDIENTES Y DUPLICADOS))

    # Aplicar el filtro según el estado seleccionado
    if estado_filtro == "P":
        respuestas_borrador = Respuesta_borrador.objects.filter(estado="P")
    elif estado_filtro == "D":
        respuestas_borrador = Respuesta_borrador.objects.filter(estado="D")
    else:
        respuestas_borrador = Respuesta_borrador.objects.filter(estado__in= ['P','D'])

    return render(request, "imp-exp-archivos/ver_borrador.html",
                  {"respuestas": respuestas_borrador, "estado_filtro": estado_filtro})

def ver_exportados(request):
    if request.method == "POST":
        seleccionadas = request.POST.getlist("seleccionadas")

        accion = request.POST.get("accion")  #  Detectar si se quiere eliminar

        if accion == "eliminar":
            # Eliminar los registros seleccionados
            registros_eliminados = Respuesta_borrador.objects.filter(id__in=seleccionadas).delete()
            messages.success(request, f"{registros_eliminados[0]} registros eliminados correctamente.")
            return redirect("ver_exportados")

    query = request.GET.get("q", "")  # Capturar el texto de búsqueda desde el formulario

    # Filtrar por búsqueda si hay un término ingresado
    respuestas_borrador = Respuesta_borrador.objects.filter(estado="E")
    if query:
        respuestas_borrador = respuestas_borrador.filter(
            nombres__icontains=query
        ) | respuestas_borrador.filter(
            apellidos__icontains=query
        ) | respuestas_borrador.filter(
            nro_documento__icontains=query
        )

    return render(request, "imp-exp-archivos/ver_exportados.html",
                  {"respuestas": respuestas_borrador,
                           "query": query,
                   })
