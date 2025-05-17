from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Facultad, Carrera, CampusSede, Genero, EstadoCivil, Pais, TipoPosgrado

# Son vistas que ya proporciona Django mismo para los ABMs
@login_required
def parametros_inicio(request):
    return render(request, "parametros/parametros_inicio.html")

# 🔹 Vista para listar todas las Facultades
class FacultadListView(LoginRequiredMixin, ListView):
    model = Facultad
    template_name = "parametros/facultad_list.html"
    context_object_name = "facultades"
    ordering = ["id"]

# 🔹 Vista para crear una Facultad
class FacultadCreateView(LoginRequiredMixin, CreateView):
    model = Facultad
    template_name = "parametros/facultad_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("facultad_list")

# 🔹 Vista para modificar una Facultad
class FacultadUpdateView(LoginRequiredMixin, UpdateView):
    model = Facultad
    template_name = "parametros/facultad_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("facultad_list")

# 🔹 Vista para eliminar una Facultad
class FacultadDeleteView(LoginRequiredMixin, DeleteView):
    model = Facultad
    template_name = "parametros/facultad_confirm_delete.html"
    success_url = reverse_lazy("facultad_list")

class CarreraListView(LoginRequiredMixin, ListView):
    model = Carrera
    template_name = "parametros/carrera_list.html"
    context_object_name = "carreras"
    ordering = ["id"]

class CarreraCreateView(LoginRequiredMixin, CreateView):
    model = Carrera
    template_name = "parametros/carrera_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("carrera_list")

class CarreraUpdateView(LoginRequiredMixin, UpdateView):
    model = Carrera
    template_name = "parametros/carrera_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("carrera_list")

class CarreraDeleteView(LoginRequiredMixin, DeleteView):
    model = Carrera
    template_name = "parametros/carrera_confirm_delete.html"
    success_url = reverse_lazy("carrera_list")


class CampusSedeListView(LoginRequiredMixin, ListView):
    model = CampusSede
    template_name = "parametros/campus_sede_list.html"
    context_object_name = "campus_sedes"
    ordering = ["id"]

class CampusSedeCreateView(LoginRequiredMixin, CreateView):
    model = CampusSede
    template_name = "parametros/campus_sede_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("campus_sede_list")

class CampusSedeUpdateView(LoginRequiredMixin, UpdateView):
    model = CampusSede
    template_name = "parametros/campus_sede_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("campus_sede_list")

class CampusSedeDeleteView(LoginRequiredMixin, DeleteView):
    model = CampusSede
    template_name = "parametros/campus_sede_confirm_delete.html"
    success_url = reverse_lazy("campus_sede_list")

class GeneroListView(LoginRequiredMixin, ListView):
    model = Genero
    template_name = "parametros/genero_list.html"
    context_object_name = "generos"
    ordering = ["id"]

class GeneroCreateView(LoginRequiredMixin, CreateView):
    model = Genero
    template_name = "parametros/genero_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("genero_list")

class GeneroUpdateView(LoginRequiredMixin, UpdateView):
    model = Genero
    template_name = "parametros/genero_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("genero_list")

class GeneroDeleteView(LoginRequiredMixin, DeleteView):
    model = Genero
    template_name = "parametros/genero_confirm_delete.html"
    success_url = reverse_lazy("genero_list")


class EstadoCivilListView(LoginRequiredMixin, ListView):
    model = EstadoCivil
    template_name = "parametros/estado_civil_list.html"
    context_object_name = "estados_civiles"
    ordering = ["id"]

class EstadoCivilCreateView(LoginRequiredMixin, CreateView):
    model = EstadoCivil
    template_name = "parametros/estado_civil_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("estado_civil_list")

class EstadoCivilUpdateView(LoginRequiredMixin, UpdateView):
    model = EstadoCivil
    template_name = "parametros/estado_civil_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("estado_civil_list")

class EstadoCivilDeleteView(LoginRequiredMixin, DeleteView):
    model = EstadoCivil
    template_name = "parametros/estado_civil_confirm_delete.html"
    success_url = reverse_lazy("estado_civil_list")

class PaisListView(LoginRequiredMixin, ListView):
    model = Pais
    template_name = "parametros/pais_list.html"
    context_object_name = "paises"
    ordering = ["id"]

class PaisCreateView(LoginRequiredMixin, CreateView):
    model = Pais
    template_name = "parametros/pais_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("pais_list")

class PaisUpdateView(LoginRequiredMixin, UpdateView):
    model = Pais
    template_name = "parametros/pais_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("pais_list")

class PaisDeleteView(LoginRequiredMixin, DeleteView):
    model = Pais
    template_name = "parametros/pais_confirm_delete.html"
    success_url = reverse_lazy("pais_list")


class TipoPosgradoListView(LoginRequiredMixin, ListView):
    model = TipoPosgrado
    template_name = "parametros/tipo_posgrado_list.html"
    context_object_name = "tipos_posgrado"
    ordering = ["id"]

class TipoPosgradoCreateView(LoginRequiredMixin, CreateView):
    model = TipoPosgrado
    template_name = "parametros/tipo_posgrado_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("tipo_posgrado_list")

class TipoPosgradoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoPosgrado
    template_name = "parametros/tipo_posgrado_form.html"
    fields = ["id", "descripcion"]
    success_url = reverse_lazy("tipo_posgrado_list")

class TipoPosgradoDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoPosgrado
    template_name = "parametros/tipo_posgrado_confirm_delete.html"
    success_url = reverse_lazy("tipo_posgrado_list")
