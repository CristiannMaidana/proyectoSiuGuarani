from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import HISTORIAL_ACADEMICO, ALUMNO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class InicioAlumno(TemplateView):
    template_name = "SIU/acceso/inicio_alumno.html"

    def get_cursada_alumno(self):
        materias_inscriptas = HISTORIAL_ACADEMICO.objects.filter(
            Q(id_alumno=self.request.session.get('usuario_id')) &
            Q(id_cursada_alumno__inscripto=True)
        ).values_list('id_cursada_alumno__id_materia_con_parcial__id_materia__nombre_materia', flat=True)
        return materias_inscriptas

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))
        contexto['usuario_cursada'] = self.get_cursada_alumno()
        return contexto
