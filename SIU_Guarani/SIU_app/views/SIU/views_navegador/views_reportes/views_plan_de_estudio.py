from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import HISTORIAL_ACADEMICO, PLAN_DE_ESTUDIO, ALUMNO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class ReportesPlanDeEstudio(TemplateView):
    template_name = "SIU/reportes/plan_de_estudio.html"

    def get_alumno(self):
        return ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))

    @staticmethod
    def get_plan_estudio():
        return PLAN_DE_ESTUDIO.objects.all()

    def get_historial_academico_de_alumno(self):
        return HISTORIAL_ACADEMICO.objects.filter(id_alumno=self.request.session.get('usuario_id'))

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = self.get_alumno()
        contexto['plan_de_estudio'] = self.get_plan_estudio()
        contexto['correlativa_llamado'] = False
        contexto['historial_academico'] = self.get_historial_academico_de_alumno()
        return contexto

    def get_materia_regularizada(self, nombre_correlativa):
        historial_academico = HISTORIAL_ACADEMICO.objects.filter(
            id_alumno=self.request.session.get('usuario_id'),
            id_cursada_alumno__id_materia_con_parcial__id_materia__nombre_materia=nombre_correlativa,
            id_cursada_alumno__aprobo=True)

        if historial_academico.exists():
            return True
        return False

    def get_examen_regularizada(self, nombre_correlativa):
        historial_academico = HISTORIAL_ACADEMICO.objects.filter(
            id_alumno=self.request.session.get('usuario_id'),
            id_examen_alumno__id_materia_con_examen__id_materia__nombre_materia=nombre_correlativa,
            id_examen_alumno__aprobo=True
        )

        if historial_academico.exists():
            return True
        return False

    def post(self, request, *args, **kwargs):
        nombre_correlativa = request.POST.get('materia_correlativa')
        solicitud_correlativa = request.POST.get('solicitud_correlativa')
        solicitud_examen = request.POST.get('solicitud_examen')

        if solicitud_correlativa:
            cumple_regularizada = self.get_materia_regularizada(nombre_correlativa)
            return JsonResponse({
                'cumple_regularizada': cumple_regularizada,
                'correlativa_llamado': True,
                'nombre_correlativa': nombre_correlativa
            })

        if solicitud_examen:
            cumple_examen = self.get_examen_regularizada(nombre_correlativa)
            return JsonResponse({
                'cumple_examen': cumple_examen,
                'correlativa_llamado': True,
                'nombre_correlativa': nombre_correlativa
            })
