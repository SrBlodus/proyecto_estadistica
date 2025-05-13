from django import forms
from .models import Facultad, Carrera, Pais, TipoPosgrado, Genero

class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField(label="Selecciona un archivo CSV")


class EstadisticasFiltroForm(forms.Form):
    facultad = forms.ModelChoiceField(
        queryset=Facultad.objects.all(),
        required=False,
        label="Facultad",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        required=False,
        label="Carrera",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    genero = forms.ModelChoiceField(
        queryset=Genero.objects.all(),
        required=False,
        label="Género",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    trabaja_actualmente = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False, label="¿Trabaja o emprende actualmente?")
    trabajo_relacionado = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="¿Trabajo o emprendimiento relacionado a carrera?")

    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        required=False,
        label="País Residencia",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    valoracion_minima = forms.IntegerField(min_value=1, max_value=5, required=False, label="Valoración mínima (1-5)")
    mostrar_comentarios_aprendizajes_no_curriculares = forms.BooleanField(required=False, label="Aprendizajes no curriculares")
    tipo_posgrado = forms.ModelChoiceField(queryset=TipoPosgrado.objects.all(), required=False, label="Tipo de Posgrado")




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["carrera"].label_from_instance = lambda obj: obj.descripcion
        self.fields["facultad"].label_from_instance = lambda obj: obj.descripcion
        self.fields["genero"].label_from_instance = lambda obj: obj.descripcion
        self.fields["pais"].label_from_instance = lambda obj: obj.descripcion
