# Create your models here.
from django.db import models

class Facultad(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre de la facultad

class Carrera(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre de la carrera

class CampusSede(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre del campus o sede

class Genero(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre de la carrera

class EstadoCivil(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre de la carrera


class Respuesta_borrador(models.Model):
    nro_registro = models.IntegerField(unique=True, blank=True, null=True)
    nro_documento = models.CharField(max_length=20)
    correo = models.CharField(max_length=255)
    nro_telefono = models.CharField(max_length=50)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    genero = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=255)
    estado_civil = models.CharField(max_length=50)
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
    nro_documento = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50)

    # Guarda las referencias a los IDs correctos
    campus_sede = models.ForeignKey(CampusSede, on_delete=models.PROTECT)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.PROTECT)

    ano_ingreso = models.IntegerField()
    ano_egreso = models.IntegerField()
    ano_primer_empleo = models.IntegerField()
    ano_primer_empleo_carrera = models.IntegerField()
