from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.forms import DomicilioForm
from SIU_app.models import ALUMNO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class Domicilio(TemplateView):
    template_name = "SIU/datos_alumno/domicilio.html"

    def get_usuario(self):
        return ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))

    def get_context_data(self, **kwargs):
        usuario = self.get_usuario()
        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = usuario
        contexto['form'] = DomicilioForm(usuario)
        return contexto

    def hay_cambio_domicilio(self, form):
        usuario = self.get_usuario()

        if usuario.id_direccion:
            dato_usuario = {
                'calle': usuario.id_direccion.calle,
                'numero_calle': usuario.id_direccion.numero,
                'piso': usuario.id_direccion.piso,
                'departamento': usuario.id_direccion.departamento,
                'unidad': usuario.id_direccion.unidad,
                'localidad': usuario.id_direccion.localida,
                'codigo_postal': usuario.id_direccion.codigo_postal,
                'barrio': usuario.id_direccion.barrio,
                'tipo_vivienda': usuario.id_direccion.tipo_de_vivienda,
                'tipo_convivencia': '',
            }  # Creo un diccionario con los datos del usuario para compararlo
        else:
            dato_usuario = {
                'calle': '',
                'numero_calle': 0,
                'piso': '',
                'departamento': '',
                'unidad': '',
                'localidad': '',
                'codigo_postal': 0,
                'barrio': '',
                'tipo_vivienda': '',
                'tipo_convivencia': '',
            }  # Creo un diccionario con los datos del usuario para compararlo

        #Creo un diccionario con los datos traidos del template
        datos_formulario = form.cleaned_data  # Acceder al cleaned_data después de validar el formulario

        #Comparo los datos de los diccionarios para tomar accion
        for field in datos_formulario:
            if datos_formulario[field] != dato_usuario[field]:  # Compara valores
                return True  # Si encuentra una diferencia, retorna True
        # Si no se encontraron discrepancias, se devuelve False
        return False

    def post(self, request, *args, **kwargs):
        usuario = self.get_usuario()
        form_domicilio = DomicilioForm(usuario=usuario, data=request.POST)

        if form_domicilio.is_valid():
            if self.hay_cambio_domicilio(form_domicilio):
                form_domicilio.save_domicilio(usuario=usuario)
                contexto = self.get_context_data()
                contexto['cambio'] = True
                return render(request, self.template_name, contexto)
            else:
                contexto = self.get_context_data()
                contexto['no_hay_cambio'] = True
                return render(request, self.template_name, contexto)
        else:
            return render(request, self.template_name, {'form': form_domicilio})
