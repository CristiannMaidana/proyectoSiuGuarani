from django.contrib import admin
from ....models import EXAMEN, EXAMEN_ALUMNO
from ..filters import RecentDateFilter


class ExamenAdmin(admin.ModelAdmin):
    list_display = ('nombre_examen', 'nota_examen', 'nombre_materia')
    list_filter = (RecentDateFilter,)

    def nombre_materia(self, obj):
        return obj.id_materia
    nombre_materia.short_description = 'Materia'

    @staticmethod
    def actualizo_examen_alumno(tabla_examen_alumno):
        nota_examen = tabla_examen_alumno.id_materia_con_examen.id_examen.nota_examen

        if nota_examen >= 4:
            tabla_examen_alumno.aprobo = True
            tabla_examen_alumno.inscripto = False
            tabla_examen_alumno.save()
        else:
            tabla_examen_alumno.aprobo = False
            tabla_examen_alumno.inscripto = False
            tabla_examen_alumno.save()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        tabla_examen_alumno = EXAMEN_ALUMNO.objects.get(id_materia_con_examen__id_examen__id_examen=obj.id_examen)
        self.actualizo_examen_alumno(tabla_examen_alumno)


admin.site.register(EXAMEN, ExamenAdmin)
