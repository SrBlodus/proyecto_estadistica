from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
import csv
import os
from .models import Respuesta
from .forms import CSVUploadForm

def importar_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES["archivo_csv"]
            reader = csv.DictReader(archivo.read().decode("utf-8").splitlines())



            for row in reader:
                try:
                    Respuesta.objects.create(
                        correo=row.get("Nombre de usuario", "").strip(),
                        nro_telefono=row.get("Número de teléfono", ""),
                        nombres = row.get("Nombres", ""),
                        apellidos = row.get("Apellidos", ""),
                        nro_documento = row.get("Cédula de Identidad Paraguaya Nº", ""),
                        genero = row.get("Género", ""),
                        ciudad = row.get("Ciudad actual de residencia", ""),
                        estado_civil = row.get("Estado Civil", ""),
                        campus_sede = row.get("Campus o sede de promoción", ""),
                        facultad = row.get("Facultad", ""),
                        carrera = row.get("Carrera", ""),
                        ano_ingreso = row.get("Año de ingreso", ""),
                        ano_egreso = row.get("Año de egreso", ""),
                        ano_primer_empleo = row.get("Año en obtener primer empleo o emprendimiento", ""),
                        ano_primer_empleo_carrera = row.get("Año en obtener primer empleo o emprendimiento relacionado a su carrera", ""),
                        estado = 'P' #Pendiente









                    )
                except Exception as e:
                    return HttpResponse(f"Error procesando la fila {row}: {e}")

            return HttpResponse("Datos importados correctamente")

    else:
        form = CSVUploadForm()

    return render(request, "importar_csv.html", {"form": form})