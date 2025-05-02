from django.db import models

# Create your models here.
class Respuesta(models.Model):
    correo = models.EmailField()
    nro_telefono = models.IntegerField()
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nro_documento = models.IntegerField()
    genero = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    estado_civil = models.CharField(max_length=50)
    campus_sede = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    ano_ingreso = models.IntegerField()
    ano_egreso = models.IntegerField()
    ano_primer_empleo = models.IntegerField()
    ano_primer_empleo_carrera = models.CharField(max_length=100)
    estado = models.CharField(max_length=1)

    def __str__(self):
        return self.nro_documento

