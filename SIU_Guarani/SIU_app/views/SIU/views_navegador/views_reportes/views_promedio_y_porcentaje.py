from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import HISTORIAL_ACADEMICO, ALUMNO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class PromedioYPorcentaje(TemplateView):
    template_name = "SIU/reportes/promedio_y_porcentaje.html"

    def materias_aprobadas(self):
        historial_academico = HISTORIAL_ACADEMICO.objects.filter(id_alumno=self.request.session.get('usuario_id'))
        total_notas = 0
        total_materias = 0
        materias_aprobadas = 0
        for tupla_historial in historial_academico:
            if tupla_historial.id_cursada_alumno.aprobo:
                total_materias += 1
                nota_total_materia = (
                        tupla_historial.id_cursada_alumno.id_materia_con_parcial.id_primer_parcial.nota_parcial +
                        tupla_historial.id_cursada_alumno.id_materia_con_parcial.id_segundo_parcial.nota_parcial
                )
                total_notas += nota_total_materia
                materias_aprobadas += 1

        promedio = round((total_notas / total_materias if total_materias > 0 else 0), 2)
        porcentaje_aprobadas = round(((total_materias / 36) * 100), 2)

        return {
            'materias_aprobadas': materias_aprobadas,
            'total_materias': total_materias,
            'promedio': promedio,
            'porcentaje_aprobadas': porcentaje_aprobadas,
        }

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['materias_aprobadas'] = self.materias_aprobadas()
        contexto['usuario'] = ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))
        return contexto
