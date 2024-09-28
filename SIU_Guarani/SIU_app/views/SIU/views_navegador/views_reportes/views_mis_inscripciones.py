from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import ALUMNO, HISTORIAL_ACADEMICO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class ReportesMisInscripciones(TemplateView):
    template_name = "SIU/reportes/inscripciones_usuario.html"

    def materias_inscriptas(self):
        cursadas_regulares = HISTORIAL_ACADEMICO.objects.filter(
            Q(id_alumno=self.request.session.get('usuario_id')) &
            (Q(id_cursada_alumno__inscripto=True) |
             Q(id_cursada_alumno__inscripto=False))
        )

        inscripto = False
        for cursada in cursadas_regulares:
            if cursada.id_cursada_alumno.inscripto:
                inscripto = True
                break

        return cursadas_regulares, inscripto

    def examenes_inscriptos(self):
        cursadas_examenes = HISTORIAL_ACADEMICO.objects.filter(
            Q(id_alumno=self.request.session.get('usuario_id')) &
            (Q(id_examen_alumno__inscripto=True) |
             Q(id_examen_alumno__inscripto=False))
        )

        inscripto = False
        for cursada in cursadas_examenes:
            if cursada.id_examen_alumno.inscripto:
                inscripto = True
                break

        return cursadas_examenes, inscripto

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        inscripciones_materias_historicas, inscripciones_materia_activas = self.materias_inscriptas()
        inscripciones_examenes_historicas, inscripciones_examenes_activos = self.examenes_inscriptos()

        contexto['inscripciones_alumno_materias'] = inscripciones_materias_historicas
        contexto['inscripciones_materia_activas'] = inscripciones_materia_activas
        contexto['inscripciones_alumno_examenes'] = inscripciones_examenes_historicas
        contexto['inscripciones_examenes_activas'] = inscripciones_examenes_activos
        contexto['usuario'] = ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))
        return contexto
