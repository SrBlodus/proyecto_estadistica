from django.urls import path
from .views import inicio
from .csv import importar_csv,ver_borrador

urlpatterns = [
    path("importar_archivo", importar_csv, name="importar_csv"),
    path("",inicio, name="inicio"),
    path("ver_borrador",ver_borrador,name="ver_borrador")
]