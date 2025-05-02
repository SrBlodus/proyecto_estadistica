from django.db import models

# Create your models here.
class Respuesta(models.Model):
    correo = models.EmailField()
    sede = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    tipo_de_documento = models.CharField(max_length=100)
    pais_documento = models.CharField(max_length=100)
    nro_documento = models.CharField(max_length=100)

    def __str__(self):
        return self.nro_documento

