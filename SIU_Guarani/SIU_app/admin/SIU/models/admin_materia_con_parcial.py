from django.contrib import admin
from ....models import MATERIA_CON_PARCIAL
from ..actions import mostrar_parciales


class MateriaConParcialAdmin(admin.ModelAdmin):
    list_display = ('nombre_materia', 'nombre_primer_parcial', 'nombre_segundo_parcial')
    list_filter = ('id_materia', 'id_materia_con_parcial')
    actions = [mostrar_parciales]

    def nombre_materia(self, obj):
        return obj.id_materia
    nombre_materia.short_description = 'Materia'

    def nombre_primer_parcial(self, obj):
        return obj.id_primer_parcial
    nombre_primer_parcial.short_description = "Pimer parcial"

    def nombre_segundo_parcial(self, obj):
        return obj.id_segundo_parcial
    nombre_segundo_parcial.short_description = "Segundo parcial"


admin.site.register(MATERIA_CON_PARCIAL, MateriaConParcialAdmin)
