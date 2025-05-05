from dateutil import parser
from django.shortcuts import render,redirect
from django.http import HttpResponse
import csv
from .models import Respuesta_borrador, Respuesta_oficial, Facultad, Carrera, CampusSede, Genero, EstadoCivil
from .forms import CSVUploadForm
from django.contrib import messages

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
                        fecha_hora_encuesta = None  # 🔹 Si hay error, guarda `None`

                    #print(f"Fecha convertida: {fecha_hora_encuesta}")


                    # Aquí buscamos el siguiente nro. de registro
                    ultimo_nro_registro = Respuesta_borrador.objects.order_by("-nro_registro").first()
                    nuevo_nro_registro = (ultimo_nro_registro.nro_registro + 1) if ultimo_nro_registro else 1


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
                        ciudad=row.get("Ciudad actual de residencia", "").strip(),
                        estado_civil=row.get("Estado Civil", "").strip(),
                        campus_sede=row.get("Campus o sede de promoción", "").strip(),
                        facultad=row.get("Facultad", "").strip(),
                        carrera=row.get("Carrera", "").strip(),
                        ano_ingreso=row.get("Año de ingreso", ""),
                        ano_egreso=row.get("Año de egreso", ""),
                        ano_primer_empleo=row.get("Año en obtener primer empleo o emprendimiento", ""),
                        ano_primer_empleo_carrera=row.get("Año en obtener primer empleo o emprendimiento relacionado a su carrera", ""),
                        estado=estado,
                    )

                except Exception as e:
                    return HttpResponse(f"Error procesando el registro Nº {nuevo_nro_registro}: {e}")

            return redirect("ver_borrador")

    else:
        form = CSVUploadForm()

    return render(request, "imp-exp-archivos/importar_csv.html", {"form": form})

def ver_borrador(request):
    if request.method == "POST":
        seleccionadas = request.POST.getlist("seleccionadas")

        accion = request.POST.get("accion")  # 🔹 Detectar si se quiere exportar o eliminar

        if accion == "eliminar":
            # Eliminar los registros seleccionados
            registros_eliminados = Respuesta_borrador.objects.filter(id__in=seleccionadas).delete()
            messages.success(request, f"{registros_eliminados[0]} registros eliminados correctamente.")
            return redirect("ver_borrador")

        registros_exportados = 0

        for id_respuesta in seleccionadas:
            try:
                borrador = Respuesta_borrador.objects.get(id=id_respuesta)

                # 🔹 Convertir facultad, carrera, sexo y campus_sede a sus respectivos IDs
                facultad_obj = Facultad.objects.filter(descripcion=borrador.facultad).first()
                carrera_obj = Carrera.objects.filter(descripcion=borrador.carrera).first()
                campus_sede_obj = CampusSede.objects.filter(descripcion=borrador.campus_sede).first()
                genero_obj = Genero.objects.filter(descripcion=borrador.genero).first()
                estado_civil_obj = EstadoCivil.objects.filter(descripcion=borrador.estado_civil).first()

                # 🔹 Validaciónes para evitar errores si no encuentra los IDs
                if not facultad_obj or not carrera_obj or not campus_sede_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Facultad, Carrera o Campus no encontrados.")
                    continue  # Saltar al siguiente registro

                if not genero_obj or not estado_civil_obj:
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Género o Estado Civil no encontrado.")
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
                    registro_existente.ciudad = borrador.ciudad
                    registro_existente.estado_civil = estado_civil_obj
                    registro_existente.ano_ingreso = borrador.ano_ingreso
                    registro_existente.ano_egreso = borrador.ano_egreso
                    registro_existente.ano_primer_empleo = borrador.ano_primer_empleo
                    registro_existente.ano_primer_empleo_carrera = borrador.ano_primer_empleo_carrera
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
                        ciudad=borrador.ciudad,
                        estado_civil=estado_civil_obj,
                        campus_sede=campus_sede_obj,
                        facultad=facultad_obj,
                        carrera=carrera_obj,
                        ano_ingreso=borrador.ano_ingreso,
                        ano_egreso=borrador.ano_egreso,
                        ano_primer_empleo=borrador.ano_primer_empleo,
                        ano_primer_empleo_carrera=borrador.ano_primer_empleo_carrera,
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
