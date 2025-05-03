from django.shortcuts import render,redirect
from django.http import HttpResponse
import csv
from .models import Respuesta_borrador, Respuesta_oficial, Facultad, Carrera, CampusSede
from .forms import CSVUploadForm
from django.contrib import messages

def importar_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES["archivo_csv"]
            reader = csv.DictReader(archivo.read().decode("utf-8").splitlines())

            for row in reader:
                try:
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
                    return HttpResponse(f"Error procesando la fila {row}: {e}")

            return redirect("ver_borrador")

    else:
        form = CSVUploadForm()

    return render(request, "importar_csv.html", {"form": form})

def ver_borrador(request):
    if request.method == "POST":
        seleccionadas = request.POST.getlist("seleccionadas")

        for id_respuesta in seleccionadas:
            borrador = Respuesta_borrador.objects.get(id=id_respuesta)


            Respuesta_oficial.objects.create(
                correo = borrador.correo,
                nro_telefono = borrador.nro_telefono,
                nombres = borrador.nombres,
                apellidos= borrador.apellidos,
                nro_documento= borrador.nro_documento,
                genero= borrador.genero,
                ciudad=borrador.ciudad,
                estado_civil=borrador.estado_civil,
                campus_sede=borrador.campus_sede,
                facultad=borrador.facultad,
                carrera=borrador.carrera,
                ano_ingreso=borrador.ano_ingreso,
                ano_egreso=borrador.ano_egreso,
                ano_primer_empleo=borrador.ano_primer_empleo,
                ano_primer_empleo_carrera=borrador.ano_primer_empleo_carrera,
            )
            borrador.estado = "E"  # Marcamos como exportado
            borrador.save()

        messages.success(request, "Las respuestas seleccionadas se han exportado correctamente. ✅")
        return redirect("ver_borrador")

    respuestas_borrador = Respuesta_borrador.objects.filter(estado__in = ["P","D"])
    return render(request, "ver_borrador.html", {"respuestas": respuestas_borrador})