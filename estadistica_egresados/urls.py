from django.urls import path
from .parametros import (FacultadListView, FacultadCreateView, FacultadUpdateView, FacultadDeleteView, CarreraListView,
                         CarreraCreateView, CarreraUpdateView, CarreraDeleteView,CampusSedeListView,CampusSedeCreateView,
                         CampusSedeUpdateView,CampusSedeDeleteView,parametros_inicio)
from .views import inicio
from .csv import importar_csv,ver_borrador

urlpatterns = [
    path("importar_archivo", importar_csv, name="importar_csv"),
    path("",inicio, name="inicio"),
    path("ver_borrador",ver_borrador,name="ver_borrador"),

    # URLs para el inicio de parámetros
    path("parametros/", parametros_inicio, name="parametros_inicio"),
    # URLs para Facultad
    path("facultades/", FacultadListView.as_view(), name="facultad_list"),
    path("facultades/nuevo/", FacultadCreateView.as_view(), name="facultad_create"),
    path("facultades/editar/<pk>/", FacultadUpdateView.as_view(), name="facultad_update"),
    path("facultades/eliminar/<pk>/", FacultadDeleteView.as_view(), name="facultad_delete"),

    # URLs para Carrera
    path("carreras/", CarreraListView.as_view(), name="carrera_list"),
    path("carreras/nuevo/", CarreraCreateView.as_view(), name="carrera_create"),
    path("carreras/editar/<pk>/", CarreraUpdateView.as_view(), name="carrera_update"),
    path("carreras/eliminar/<pk>/", CarreraDeleteView.as_view(), name="carrera_delete"),

    # URLs para CampusSede
    path("campus_sedes/", CampusSedeListView.as_view(), name="campus_sede_list"),
    path("campus_sedes/nuevo/", CampusSedeCreateView.as_view(), name="campus_sede_create"),
    path("campus_sedes/editar/<pk>/", CampusSedeUpdateView.as_view(), name="campus_sede_update"),
    path("campus_sedes/eliminar/<pk>/", CampusSedeDeleteView.as_view(), name="campus_sede_delete"),

]