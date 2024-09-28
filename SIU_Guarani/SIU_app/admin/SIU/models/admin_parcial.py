from django.contrib import admin
from django.db.models import Q
from ....models import PARCIAL, CURSADA_ALUMNO


class ParcialAdmin(admin.ModelAdmin):
    list_display = ('nombre_parcial', 'nota_parcial', 'nota_recuperatorio', 'nota_promocion', 'nombre_materia')
    list_filter = ('nombre_parcial',)

    def nombre_materia(self, obj):
        return obj.id_materia

    nombre_materia.short_description = 'Materia'

    @staticmethod
    def actualizo_cursada_alumno(tabla_cursada_alumno):
        nota_primer_promocion = tabla_cursada_alumno.id_materia_con_parcial.id_primer_parcial.nota_promocion
        nota_primer_parcial = tabla_cursada_alumno.id_materia_con_parcial.id_primer_parcial.nota_parcial
        nota_primer_recuperatorio = tabla_cursada_alumno.id_materia_con_parcial.id_primer_parcial.nota_recuperatorio
        nota_segundo_promocion = tabla_cursada_alumno.id_materia_con_parcial.id_segundo_parcial.nota_promocion
        nota_segundo_parcial = tabla_cursada_alumno.id_materia_con_parcial.id_segundo_parcial.nota_parcial
        nota_segundo_recuperatorio = tabla_cursada_alumno.id_materia_con_parcial.id_segundo_parcial.nota_recuperatorio

        if nota_primer_parcial < 4:
            if nota_primer_recuperatorio != 0 and nota_primer_recuperatorio < 4:
                tabla_cursada_alumno.aprobo = False
                tabla_cursada_alumno.inscripto = False
                tabla_cursada_alumno.save()

        if ((nota_primer_parcial >= 4 or nota_primer_recuperatorio >= 4 or nota_primer_promocion >= 4) and
                (nota_segundo_parcial != 0 and nota_segundo_parcial < 4)):
            if nota_segundo_recuperatorio != 0 and nota_segundo_recuperatorio < 4:
                tabla_cursada_alumno.aprobo = False
                tabla_cursada_alumno.inscripto = False
                tabla_cursada_alumno.save()

            elif nota_segundo_recuperatorio >= 4:
                tabla_cursada_alumno.aprobo = True
                tabla_cursada_alumno.inscripto = False
                tabla_cursada_alumno.save()

        if (nota_primer_parcial >= 4 or nota_primer_recuperatorio >= 4 or nota_primer_promocion >= 4 and
                nota_segundo_parcial == 0):
            pass
        if ((nota_primer_parcial >= 4 or nota_primer_recuperatorio >= 4 or nota_primer_promocion >= 4) and
                (nota_segundo_parcial >= 4 or nota_segundo_recuperatorio >= 4 or nota_segundo_promocion >= 4)):
            tabla_cursada_alumno.aprobo = True
            tabla_cursada_alumno.inscripto = False
            tabla_cursada_alumno.save()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        tabla_cursada_alumno = CURSADA_ALUMNO.objects.get(
            Q(id_materia_con_parcial__id_primer_parcial__id_parcial=obj.id_parcial) |
            Q(id_materia_con_parcial__id_segundo_parcial__id_parcial=obj.id_parcial)
        )
        self.actualizo_cursada_alumno(tabla_cursada_alumno)


admin.site.register(PARCIAL, ParcialAdmin)
