from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Facultad, Carrera, CampusSede

# Son vistas que ya proporciona Django mismo para los ABMs

def parametros_inicio(request):
    return render(request, "parametros/parametros_inicio.html")

# 🔹 Vista para listar todas las Facultades
class FacultadListView(ListView):
    model = Facultad
    template_name = "parametros/facultad_list.html"
    context_object_name = "facultades"

# 🔹 Vista para crear una Facultad
class FacultadCreateView(CreateView):
    model = Facultad
    template_name = "parametros/facultad_form.html"
    fields = ["id_facultad", "descripcion"]
    success_url = reverse_lazy("facultad_list")

# 🔹 Vista para modificar una Facultad
class FacultadUpdateView(UpdateView):
    model = Facultad
    template_name = "parametros/facultad_form.html"
    fields = ["id_facultad", "descripcion"]
    success_url = reverse_lazy("facultad_list")

# 🔹 Vista para eliminar una Facultad
class FacultadDeleteView(DeleteView):
    model = Facultad
    template_name = "parametros/facultad_confirm_delete.html"
    success_url = reverse_lazy("facultad_list")

class CarreraListView(ListView):
    model = Carrera
    template_name = "parametros/carrera_list.html"
    context_object_name = "carreras"

class CarreraCreateView(CreateView):
    model = Carrera
    template_name = "parametros/carrera_form.html"
    fields = ["id_carrera", "descripcion"]
    success_url = reverse_lazy("carrera_list")

class CarreraUpdateView(UpdateView):
    model = Carrera
    template_name = "parametros/carrera_form.html"
    fields = ["id_carrera", "descripcion"]
    success_url = reverse_lazy("carrera_list")

class CarreraDeleteView(DeleteView):
    model = Carrera
    template_name = "parametros/carrera_confirm_delete.html"
    success_url = reverse_lazy("carrera_list")


class CampusSedeListView(ListView):
    model = CampusSede
    template_name = "parametros/campus_sede_list.html"
    context_object_name = "campus_sedes"

class CampusSedeCreateView(CreateView):
    model = CampusSede
    template_name = "parametros/campus_sede_form.html"
    fields = ["id_campus_sede", "descripcion"]
    success_url = reverse_lazy("campus_sede_list")

class CampusSedeUpdateView(UpdateView):
    model = CampusSede
    template_name = "parametros/campus_sede_form.html"
    fields = ["id_campus_sede", "descripcion"]
    success_url = reverse_lazy("campus_sede_list")

class CampusSedeDeleteView(DeleteView):
    model = CampusSede
    template_name = "parametros/campus_sede_confirm_delete.html"
    success_url = reverse_lazy("campus_sede_list")