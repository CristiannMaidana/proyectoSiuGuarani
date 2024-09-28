from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.forms import DatosDeContactoForm
from SIU_app.models import ALUMNO
from ..views_datos_contacto import DatosContacto


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class ConfiguracionDatosCelular(TemplateView):
    template_name = "SIU/datos_alumno/configuracion/configuracion_datos_celular.html"

    def get_usuario(self):
        return ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))

    def get_context_data(self, **kwargs):
        usuario = self.get_usuario()
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = usuario
        contexto['form'] = DatosDeContactoForm(usuario)
        return contexto

    def actualizo_celular(self, form_datos_celular):
        usuario = self.get_usuario()
        numero = form_datos_celular.cleaned_data['numero']

        if usuario.id_datos_contacto.numero_celular != numero:
            form_datos_celular.save_numero(usuario=usuario)
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        usuario = self.get_usuario()
        form_datos_celular = DatosDeContactoForm(usuario=usuario, data=request.POST)
        if form_datos_celular.is_valid():
            if self.actualizo_celular(form_datos_celular):
                contexto = self.get_context_data(**kwargs)
                contexto['cambio'] = True
                return render(request, DatosContacto.template_name, contexto)
            else:
                contexto = self.get_context_data(**kwargs)
                contexto['no_hay_cambio'] = True
                return render(request, DatosContacto.template_name, contexto)
        else:
            return render(request, self.template_name, {'form': form_datos_celular})
