import csv
from django.core.management.base import BaseCommand
from estadistica_egresados.models import Respuesta

class Command(BaseCommand):
    help = "Importar datos desde un CSV a la base de datos"

    def handle(self, *args, **kwargs):
        with open("estadistica_egresados/csv/respuestas.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Respuesta.objects.create(
                    correo=row['Nombre de usuario'],
                    sede = row['SEDE'],
                    facultad = row['Facultad'],
                    carrera = row['Carrera'],
                    tipo_de_documento = row['Tipo de Documento'],
                    pais_documento = row['Pais Origen'],
                    nro_documento = row['Nro de Documento'],
                )

        self.stdout.write(self.style.SUCCESS("Datos importados correctamente"))