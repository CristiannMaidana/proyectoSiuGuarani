from django.contrib import admin

from ..filters import RecentDateFilter
from ....models import EXAMEN_ALUMNO
from ..actions import mostrar_materia_con_examen


class ExamenAlumnoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'aprobo', 'inscripto', 'nombre_alumno', 'examen_del_alumno')
    list_filter = ('id_alumno', RecentDateFilter)
    actions = [mostrar_materia_con_examen]

    def examen_del_alumno(self, obj):
        return obj.id_materia_con_examen
    examen_del_alumno.short_description = 'Mesa de examen inscripta del alumno'

    def nombre_alumno(self, obj):
        return obj.id_alumno
    nombre_alumno.short_description = 'Alumnos'


admin.site.register(EXAMEN_ALUMNO, ExamenAlumnoAdmin)
