from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import ALUMNO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class DatosContacto(TemplateView):
    template_name = "SIU/datos_alumno/datos_de_contacto.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))
        return contexto
