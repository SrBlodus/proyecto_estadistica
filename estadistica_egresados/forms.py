from django import forms
from .models import Facultad, Carrera, Pais, TipoPosgrado

class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField(label="Selecciona un archivo CSV")


class EstadisticasFiltroForm(forms.Form):
    #carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), required=False, label="Carrera")
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        required=False,
        label="Carrera",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    facultad = forms.ModelChoiceField(queryset=Facultad.objects.all(), required=False, label="Facultad")
    trabaja_actualmente = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False, label="¿Trabaja actualmente?")
    exterior = forms.ModelChoiceField(queryset=Pais.objects.all(), required=False, label="Ubicación (Solo egresados en el exterior)")
    valoracion_minima = forms.IntegerField(min_value=1, max_value=5, required=False, label="Valoración mínima (1-5)")
    mostrar_comentarios = forms.BooleanField(required=False, label="Incluir comentarios opcionales")
    tipo_posgrado = forms.ModelChoiceField(queryset=TipoPosgrado.objects.all(), required=False, label="Tipo de Posgrado")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["carrera"].label_from_instance = lambda obj: obj.descripcion
