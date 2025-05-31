from .models import Respuesta_oficial
from django.db.models import Count

encuestados_por_genero = (
    Respuesta_oficial.objects
    .values("facultad__descripcion", "genero__descripcion")
    .annotate(total=Count("id"))
)

print(encuestados_por_genero)
