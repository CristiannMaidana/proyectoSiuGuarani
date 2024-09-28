from django.contrib import admin
from ....models import ALUMNO
from ... import mostrar_carrera_universitaria, mostrar_historial_academico


class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'nombre_carrera')
    list_filter = ('dni', 'id_carrera')
    search_fields = ('nombre', 'apellido', 'dni')
    actions = [mostrar_carrera_universitaria, mostrar_historial_academico]

    def nombre_carrera(self, obj):
        return obj.id_carrera
    nombre_carrera.short_description = "Carrera del alumno"


admin.site.register(ALUMNO, AlumnoAdmin)
