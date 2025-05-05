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
                    ultimo_nro_registro = Respuesta_borrador.objects.order_by("-nro_registro").first()
                    nuevo_nro_registro = (ultimo_nro_registro.nro_registro + 1) if ultimo_nro_registro else 1

                    nro_documento = row.get("Cédula de Identidad Paraguaya Nº", "").strip()

                    # Obtener los IDs correspondientes
                    facultad_obj = Facultad.objects.filter(descripcion=row.get("Facultad", "").strip()).first()
                    carrera_obj = Carrera.objects.filter(descripcion=row.get("Carrera", "").strip()).first()
                    campus_sede_obj = CampusSede.objects.filter(descripcion=row.get("Campus o sede de promoción", "").strip()).first()

                    # Verificar si el registro ya existe en `Respuesta_oficial`
                    existe = Respuesta_oficial.objects.filter(
                        nro_documento=nro_documento,
                        facultad=facultad_obj,
                        carrera=carrera_obj,
                        campus_sede=campus_sede_obj
                    ).exists()


                    estado = "D" if existe else "P"

                    # Guardar en el borrador con valores sin convertir
                    Respuesta_borrador.objects.create(
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
                    messages.error(request, f"Error en registro Nº {borrador.nro_registro}: Genero o Estado Civil no encontrado.")
                    continue

                # 🔹 Crear el registro en `Respuesta_oficial` con los IDs en lugar de los nombres
                Respuesta_oficial.objects.create(
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

                # 🔹 Marcar el registro como exportado
                borrador.estado = "E"
                borrador.save()

            except Exception as e:
                messages.error(request, f"Error procesando registro Nº {borrador.nro_registro}: {str(e)}")

        messages.success(request, "Las respuestas seleccionadas se han exportado correctamente. ✅")
        return redirect("ver_borrador")

    respuestas_borrador = Respuesta_borrador.objects.filter(estado__in=["P", "D"])
    return render(request, "imp-exp-archivos/ver_borrador.html", {"respuestas": respuestas_borrador})