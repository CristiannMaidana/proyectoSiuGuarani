from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.forms import *
from SIU_app.models import *

@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class Configuracion(TemplateView):
    template_name = "SIU/datos_alumno/configuracion/configuracion.html"

    def get_usuario(self):
        return ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))

    def get_context_data(self, **kwargs):
        usuario = self.get_usuario()
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = usuario
        contexto['form'] = ConfiguracionForm(usuario)
        return contexto

    def post(self, request, *args, **kwargs):
        usuario = self.get_usuario()
        form_contrasenna = ConfiguracionForm(usuario=usuario, data=request.POST)

        if form_contrasenna.is_valid():
            contrasenna_actual_ingresada = form_contrasenna.cleaned_data['contrasenna_actual']
            correo_actual_ingresado = form_contrasenna.cleaned_data['mail']
            correo_actual_usuario = usuario.id_datos_contacto.correo

            contexto = self.get_context_data(**kwargs)

            if correo_actual_usuario != correo_actual_ingresado:
                contexto['cambio_mail'] = True
                form_contrasenna.save_mail(usuario)
                return render(request, self.template_name, contexto)

            if check_password(contrasenna_actual_ingresada, usuario.id_usuario.password):
                if self.actualizo_contrasenna(form_contrasenna, usuario):
                    contexto['cambio'] = True
                    update_session_auth_hash(request, usuario.id_usuario)
                else:
                    contexto['cambio'] = False
            else:
                contexto['no_coincide_contrasenna_actual'] = True
            return render(request, self.template_name, contexto)
        else:
            return render(request, self.template_name, {'form': form_contrasenna})

    @staticmethod
    def actualizo_contrasenna(form_contrasenna, usuario):
        if (form_contrasenna.cleaned_data['contrasenna_nueva'] ==
                form_contrasenna.cleaned_data['confirmar_contrasenna_nueva']):
            form_contrasenna.save_contrasenna(usuario=usuario)
            return True
        else:
            return False
