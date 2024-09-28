from django.contrib import admin

from ....models import HISTORIAL_ACADEMICO
from ..filters import RecentDateFilter, InscriptoMateriasFilter, InscriptoExamenesFilter
from ..actions import mostrar_cursada_alumno, mostrar_examen_alumno


class HistorialAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_alumno', 'fecha', 'nombre_cursada_alumno', 'nombre_examen_alumno')
    list_filter = (RecentDateFilter, InscriptoMateriasFilter, InscriptoExamenesFilter)
    search_fields = ('id_alumno__dni',)
    actions = [mostrar_cursada_alumno, mostrar_examen_alumno]

    def nombre_alumno(self, obj):
        return obj.id_alumno
    nombre_alumno.short_description = 'Alumnos'

    def nombre_cursada_alumno(self, obj):
        return obj.id_cursada_alumno
    nombre_cursada_alumno.short_description = 'Cursada regular del alumno'

    def nombre_examen_alumno(self, obj):
        return obj.id_examen_alumno
    nombre_examen_alumno.short_description = 'Mesa de examen del alumno'


admin.site.register(HISTORIAL_ACADEMICO, HistorialAcademicoAdmin)
