from django.contrib import admin
from ....models import CURSADA_ALUMNO
from ..actions import mostrar_materia_con_parcial


class CursadaAlumnoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'aprobo', 'inscripto', 'id_alumno', 'cursada_del_alumno')
    list_filter = ('id_alumno', 'inscripto', 'aprobo')
    search_fields = ('fecha',)
    actions = [mostrar_materia_con_parcial]

    def cursada_del_alumno(self, obj):
        return obj.id_materia_con_parcial
    cursada_del_alumno.short_description = 'Materias inscriptas del alumno'


admin.site.register(CURSADA_ALUMNO, CursadaAlumnoAdmin)
