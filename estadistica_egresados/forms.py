from django import forms
from .models import Facultad, Carrera, Pais, TipoPosgrado, Genero, EstadoCivil

# FORMULARIO PARA LA CARGA DEL ARCHIVO CSV
class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField(label="Selecciona un archivo CSV")


# FORMULARIO PARA REALIZAR LA CONSULTA PAR QUITAR DATOS ESTADISTICOS
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

    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        required=False,
        label="País Residencia",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    mostrar_comentarios_ciudad_residencia = forms.BooleanField(required=False,label="Mostrar Ciudades de Residencia")

    estado_civil = forms.ModelChoiceField(
        queryset=EstadoCivil.objects.all(),
        required=False,
        label="Estado Civil",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    ano_ingreso_min = forms.IntegerField(required=False, label="Año de ingreso (desde)")
    ano_ingreso_max = forms.IntegerField(required=False, label="Año de ingreso (hasta)")
    ano_egreso_min = forms.IntegerField(required=False, label="Año de egreso (desde)")
    ano_egreso_max = forms.IntegerField(required=False, label="Año de egreso (hasta)")

    trabaja_actualmente = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False, label="¿Trabaja o emprende actualmente?")


    ano_primer_empleo_min = forms.IntegerField(required=False, label="Año de primer empleo/emprendimiento (desde)")
    ano_primer_empleo_max = forms.IntegerField(required=False, label="Año de empleo/emprendimiento (hasta)")

    trabajo_relacionado = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="¿Trabajo o emprendimiento relacionado a carrera?")

    plan_curricular_optimo= forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="¿Plan curricular óptimo para enfrentar desafíos laborales?")

    valoracion_aprendizaje_docente = forms.IntegerField(min_value=1, max_value=5, required=False, label="Valoración mínima (1-5) de los aprendizajes brindados por los docentes para el desarrollo profesional")

    ind_materias_utiles= forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="Materias en general útiles para desempeño laboral")

    valoracion_impacto_formacion_academica_laboral = forms.IntegerField(min_value=1, max_value=5, required=False, label="Valoración mínima (1-5) del impacto de la formación académica en la situación laboral actual?")

    mostrar_comentarios_aprendizajes_no_curriculares = forms.BooleanField(required=False,label="Mostrar Aprendizajes no curriculares que se consideraron fundamentales para el desarrollo laboral")

    ano_primer_empleo_carrera_min = forms.IntegerField(required=False, label="Año de primer empleo/emprendimiento relacionado a la carrera(desde)")
    ano_primer_empleo_carrera_max = forms.IntegerField(required=False, label="Año de empleo/emprendimiento relacionado a la carrera (hasta)")

    ind_oportunidad_desarrollo_profesional = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="Oportunidad de desarrollo profesional")

    valoracion_estudios_trayectoria_profesional = forms.IntegerField(min_value=1, max_value=5, required=False, label="Valoración mínima (1-5) en el impacto de los estudios en la trayectoria profesional")

    opcional_influencia_en_trayectoria = forms.BooleanField(required=False,label="Comentarios de influencia de la educación recibida en la trayectoria profesional")

    ind_participa_actividad_egresado = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="Participación en actividades organizadas por la facultad")


    ind_interes_participar_actividad_egresado = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="Interesados en seguir participando de actividades organizadas por la facultad")

    ind_interes_posgrado = forms.ChoiceField(choices=[("", "Todos"), ("S", "Sí"), ("N", "No")], required=False,
                                            label="Interesados en participar de posgrados")

    tipo_posgrado = forms.ModelChoiceField(
        queryset=TipoPosgrado.objects.all(),
        required=False,
        label="Tipo de Posgrado",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    opcional_area_posgrado = forms.BooleanField(required=False,label="Ver áreas/temas sugeridos para para los posgrados")

    opcional_estrategia_convocatoria = forms.BooleanField(required=False,label="Ver estrategias/actividades sugeridas para la convocatoria de estudiantes")

    opcional_contacto_carrera = forms.BooleanField(required=False,label="Ver comentarios acerca de desarrollo de oportunidades laborales")





    # Esta función trae la descripción del objeto normalizado.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["carrera"].label_from_instance = lambda obj: obj.descripcion
        self.fields["facultad"].label_from_instance = lambda obj: obj.descripcion
        self.fields["genero"].label_from_instance = lambda obj: obj.descripcion
        self.fields["pais"].label_from_instance = lambda obj: obj.descripcion
        self.fields["estado_civil"].label_from_instance = lambda obj: obj.descripcion
        self.fields["tipo_posgrado"].label_from_instance = lambda obj: obj.descripcion
