from django.contrib import admin
from ....models import MATERIA_CON_EXAMEN
from ..actions import cargo_notas_examen


class MateriaConExamenAdmin(admin.ModelAdmin):
    list_display = ('nombre_materia', 'nombre_examen')
    actions = [cargo_notas_examen]

    def nombre_examen(self, obj):
        return obj.id_examen
    nombre_examen.short_description = 'Examen'

    def nombre_materia(self, obj):
        return obj.id_materia
    nombre_materia.short_description = 'Materia'


admin.site.register(MATERIA_CON_EXAMEN, MateriaConExamenAdmin)
