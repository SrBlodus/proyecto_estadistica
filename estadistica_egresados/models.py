# Create your models here.
from django.db import models

class Facultad(models.Model):
    id_facultad = models.CharField(primary_key=True, max_length=7)  # ID manual tipo VARCHAR(7)
    descripcion = models.CharField(max_length=255)  # Nombre de la facultad

class Carrera(models.Model):
    id_carrera = models.CharField(primary_key=True, max_length=7)  # ID manual tipo VARCHAR(7)
    descripcion = models.CharField(max_length=255)  # Nombre de la carrera

class CampusSede(models.Model):
    id_campus_sede = models.CharField(primary_key=True, max_length=7)  # ID manual tipo VARCHAR(7)
    descripcion = models.CharField(max_length=255)  # Nombre del campus o sede

class Respuesta_borrador(models.Model):
    nro_documento = models.CharField(max_length=20)  # Puede haber múltiples registros con el mismo documento
    correo = models.CharField(max_length=255)
    nro_telefono = models.CharField(max_length=50)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    genero = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=255)
    estado_civil = models.CharField(max_length=50)

    # Guardar la descripción y no el ID en el borrador
    facultad = models.CharField(max_length=255)
    carrera = models.CharField(max_length=255)
    campus_sede = models.CharField(max_length=255)

    ano_ingreso = models.IntegerField()
    ano_egreso = models.IntegerField()
    ano_primer_empleo = models.IntegerField()
    ano_primer_empleo_carrera = models.IntegerField()
    estado = models.CharField(max_length=1) # P: PENDIENTE, E: EXPORTADO, D: DUPLICADO

class Respuesta_oficial(models.Model):
    correo = models.EmailField()
    nro_telefono = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nro_documento = models.CharField(max_length=20)  # Eliminamos `unique=True`
    genero = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    estado_civil = models.CharField(max_length=50)

    # Ahora guarda las referencias a los IDs correctos
    campus_sede = models.ForeignKey(CampusSede, on_delete=models.PROTECT)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)

    ano_ingreso = models.IntegerField()
    ano_egreso = models.IntegerField()
    ano_primer_empleo = models.IntegerField()
    ano_primer_empleo_carrera = models.IntegerField()
