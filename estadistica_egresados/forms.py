from django import forms

class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField(label="Selecciona un archivo CSV")