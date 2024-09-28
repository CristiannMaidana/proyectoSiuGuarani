from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.forms import DatosPersonalesForm, SituacionFamiliarForm
from SIU_app.models import ALUMNO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class MisDatosPersonales(TemplateView):
    template_name = "SIU/datos_alumno/datos_personales.html"

    def get_usuario(self):
        return ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))

    def get_context_data(self, **kwargs):
        usuario = self.get_usuario()
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = usuario
        contexto['form_usuario'] = DatosPersonalesForm(usuario)
        contexto['form_familia'] = SituacionFamiliarForm(usuario)
        return contexto

    def get_cambio_datos_familia(self, form):
        usuario = self.get_usuario()
        if usuario.id_familia:
            datos_usuario = {
                'situacion_madre': usuario.id_familia.mama,
                'situacion_padre': usuario.id_familia.papa,
                'cantidad_hijos': usuario.id_familia.hijos,
                'cantidad_familiares': usuario.id_familia.cantidad_familia_cargo,
                'estado_civil': usuario.id_familia.estado_civil,
            }
        else:
            datos_usuario = {
                'situacion_madre': '',
                'situacion_padre': '',
                'cantidad_hijos': '',
                'cantidad_familiares': '',
                'estado_civil': '',
            }

        datos_familia = form.cleaned_data

        for field in datos_usuario:
            if datos_familia[field] != datos_usuario[field]:
                return True
        return False

    def post(self, request, *args, **kwargs):
        usuario = self.get_usuario()
        form_familia = SituacionFamiliarForm(usuario=usuario, data=request.POST)
        if form_familia.is_valid():
            if self.get_cambio_datos_familia(form_familia):
                form_familia.save_datos_familia(usuario=usuario)
                contexto = self.get_context_data()
                contexto['cambio'] = True
                return render(self.request, self.template_name, contexto)
            else:
                contexto = self.get_context_data()
                contexto['no_hay_cambio'] = True
                return render(self.request, self.template_name, contexto)
        else:
            return redirect(self.request, self.template_name)
