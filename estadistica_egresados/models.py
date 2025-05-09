# Create your models here.
from django.db import models

class Facultad(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre de la facultad

class Carrera(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre de la carrera

class CampusSede(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)  # Nombre del campus o sede

class Genero(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)

class EstadoCivil(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)

class Pais(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)

class TipoPosgrado(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)

class Respuesta_borrador(models.Model):
    fecha_hora_encuesta = models.DateTimeField(null=True, blank=True)
    fecha_hora_encuesta_anterior = models.DateTimeField(null=True, blank=True)
    nro_registro = models.IntegerField(unique=True, blank=True, null=True)
    correo = models.CharField(max_length=255)
    nro_telefono = models.CharField(max_length=50)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    nro_documento = models.CharField(max_length=20)
    genero = models.CharField(max_length=50)
    pais = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    estado_civil = models.CharField(max_length=50)

    campus_sede = models.CharField(max_length=255)
    facultad = models.CharField(max_length=255)
    carrera = models.CharField(max_length=255)

    ano_ingreso = models.IntegerField()
    ano_egreso = models.IntegerField()
    ind_trabaja = models.CharField(max_length=2)

    #sección 2 del formulario
    ano_primer_empleo = models.IntegerField(null=True, blank=True)
    ind_empleo_relacionado_carrera = models.CharField(max_length=2, null=True, blank=True)
    ind_plan_curricular_optimo = models.CharField(max_length=2, null=True, blank=True)
    valoracion_aprendizaje_docente = models.IntegerField(null=True, blank=True)
    ind_materias_utiles = models.CharField(max_length=2, null=True, blank=True)
    valoracion_impacto_formacion_academica_laboral = models.IntegerField(null=True, blank=True)
    opcional_aprendizajes_no_curriculares = models.TextField(null=True, blank=True)

    # sección 3 del formulario
    ano_primer_empleo_carrera = models.IntegerField(null=True, blank=True)
    ind_oportunidad_desarrollo_profesional = models.CharField(max_length=2, null=True, blank=True)
    valoracion_estudios_trayectoria_profesional = models.IntegerField(null=True, blank=True)
    opcional_influencia_en_trayectoria = models.TextField(null=True, blank=True)






    ind_participa_actividad_egresado = models.CharField(max_length=2)
    ind_interes_participar_actividad_egresado = models.CharField(max_length=2)
    ind_interes_posgrado = models.CharField(max_length=2)
    tipo_posgrado = models.CharField(max_length=255)
    opcional_area_posgrado = models.TextField(null=True, blank=True)
    opcional_estrategia_convocatoria = models.TextField(null=True, blank=True)
    opcional_contacto_carrera = models.TextField(null=True, blank=True)

    hash_valor = models.CharField(max_length=32, unique=True, null=True, blank=True)
    estado = models.CharField(max_length=1) # P: PENDIENTE, E: EXPORTADO, D: DUPLICADO

class Respuesta_oficial(models.Model):
    fecha_hora_encuesta = models.DateTimeField(null=True, blank=True)
    correo = models.EmailField()
    nro_telefono = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nro_documento = models.CharField(max_length=20)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT) #referencia a tabla
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT) #referencia a tabla
    ciudad = models.CharField(max_length=255)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.PROTECT)#referencia a tabla

    campus_sede = models.ForeignKey(CampusSede, on_delete=models.PROTECT)  #referencia a tabla
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT)#referencia a tabla
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)#referencia a tabla

    ano_ingreso = models.IntegerField()
    ano_egreso = models.IntegerField()
    ind_trabaja = models.CharField(max_length=2)

    ano_primer_empleo = models.IntegerField(null=True, blank=True)
    ind_empleo_relacionado_carrera = models.CharField(max_length=2,null=True, blank=True)
    ind_plan_curricular_optimo = models.CharField(max_length=2,null=True, blank=True)
    valoracion_aprendizaje_docente = models.IntegerField(null=True, blank=True)
    ind_materias_utiles = models.CharField(max_length=2,null=True, blank=True)
    valoracion_impacto_formacion_academica_laboral = models.IntegerField(null=True, blank=True)
    opcional_aprendizajes_no_curriculares = models.TextField(null=True, blank=True)


    ano_primer_empleo_carrera = models.IntegerField(null=True, blank=True)
    ind_oportunidad_desarrollo_profesional = models.CharField(max_length=2, null=True, blank=True)
    valoracion_estudios_trayectoria_profesional = models.IntegerField(null=True, blank=True)
    opcional_influencia_en_trayectoria = models.TextField(null=True, blank=True)

    ind_participa_actividad_egresado = models.CharField(max_length=2)
    ind_interes_participar_actividad_egresado = models.CharField(max_length=2)
    ind_interes_posgrado = models.CharField(max_length=2)
    tipo_posgrado = models.ForeignKey(TipoPosgrado, on_delete=models.PROTECT) #referencia a tabla
    opcional_area_posgrado = models.TextField(null=True, blank=True)
    opcional_estrategia_convocatoria = models.TextField(null=True, blank=True)
    opcional_contacto_carrera = models.TextField(null=True, blank=True)
