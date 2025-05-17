from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Facultad, CampusSede, Carrera, Genero, Pais, EstadoCivil, TipoPosgrado

@receiver(post_migrate)
def insertar_datos_iniciales(sender, **kwargs):
    if not Facultad.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Ciencias De La Salud", "Ciencias Económicas", "Ciencias Jurídicas", "Ciencias y Tecnología", "Filosofía y Ciencias Humanas",]
        for descripcion in descripciones:
            Facultad.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en Facultad")

    if not CampusSede.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Campus Itapúa, Encarnación"]
        for descripcion in descripciones:
            CampusSede.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en CampusSede")

    if not Carrera.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Enfermería","Kinesiología y Fisiatría","Odontología","Administración de Empresas","Contador Público Nacional","Comercio Internacional","Economía","Derecho","Notariado","Arquitectura","Ingeniería Informática","Ciencias de la Comunicación","Psicología","Educación Física, Deportes y Recreación"]
        for descripcion in descripciones:
            Carrera.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en Carrera")

    if not Genero.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Masculino", "Femenino", "Otros"]
        for descripcion in descripciones:
            Genero.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en Genero")

    if not Pais.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Paraguay", "Argentina", "Brasil"]
        for descripcion in descripciones:
            Pais.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en Pais")

    if not EstadoCivil.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Soltero/a", "Casado/a", "Divorciado/a","Viudo/a"]
        for descripcion in descripciones:
            EstadoCivil.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en EstadoCivil")


    if not TipoPosgrado.objects.exists():  # Solo ejecuta si la tabla está vacía
        descripciones = ["Maestría", "Doctorado", "Diplomado","Especialización"]
        for descripcion in descripciones:
            TipoPosgrado.objects.create(descripcion=descripcion)
        print("✅ Datos iniciales insertados en TipoPosgrado")



