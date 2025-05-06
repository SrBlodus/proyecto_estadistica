from django.urls import path
from .parametros import (FacultadListView, FacultadCreateView, FacultadUpdateView, FacultadDeleteView, CarreraListView,
                         CarreraCreateView, CarreraUpdateView, CarreraDeleteView,CampusSedeListView,CampusSedeCreateView,
                         CampusSedeUpdateView,CampusSedeDeleteView,parametros_inicio,
                         GeneroListView,GeneroCreateView,GeneroDeleteView,GeneroUpdateView,
                         EstadoCivilListView, EstadoCivilCreateView,
                         EstadoCivilUpdateView, EstadoCivilDeleteView
                         )
from .views import inicio
from .csv import importar_csv, ver_borrador, imp_exp_archivos_inicio, ver_exportados

urlpatterns = [
    path("",inicio, name="inicio"),

    # URLs para la parte de la importación y exportación de los archivos
    path("importar_archivo", importar_csv, name="importar_csv"),
    path("ver_borrador",ver_borrador,name="ver_borrador"),
    path("ver_exportados",ver_exportados,name="ver_exportados"),
    path("imp-exp-archivos",imp_exp_archivos_inicio,name="inicio_imp_exp_archivos"),

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

    # URLs para Genero
    path("generos/", GeneroListView.as_view(), name="genero_list"),
    path("generos/nuevo/", GeneroCreateView.as_view(), name="genero_create"),
    path("generos/editar/<pk>/", GeneroUpdateView.as_view(), name="genero_update"),
    path("generos/eliminar/<pk>/", GeneroDeleteView.as_view(), name="genero_delete"),

    # URLs para Estado Civil
    path("estado_civil/", EstadoCivilListView.as_view(), name="estado_civil_list"),
    path("estado_civil/nuevo/", EstadoCivilCreateView.as_view(), name="estado_civil_create"),
    path("estado_civil/editar/<pk>/", EstadoCivilUpdateView.as_view(), name="estado_civil_update"),
    path("estado_civil/eliminar/<pk>/", EstadoCivilDeleteView.as_view(), name="estado_civil_delete"),


]