from django.apps import AppConfig


class EstadisticaEgresadosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estadistica_egresados'

    def ready(self):
        import estadistica_egresados.signals  # Cargar señales
