from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from SIU_app.forms import RecuperarContrasennaForm
from SIU_app.models import ALUMNO


class OlvidoContrasenna(TemplateView):
    template_name = "SIU/acceso/olvido_contrasenna.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['form'] = RecuperarContrasennaForm()
        return contexto

    def post(self, request, *args, **kwargs):
        form_recupero_contrasena = RecuperarContrasennaForm(request.POST)

        if form_recupero_contrasena.is_valid():
            tipo_de_documento_ingresado = form_recupero_contrasena.cleaned_data['tipo_de_documento']
            documento_ingresado = form_recupero_contrasena.cleaned_data['numero_documento']

            if documento_ingresado is None:
                contexto = self.get_context_data(**kwargs)
                contexto['vacio'] = True
                return render(request, self.template_name, contexto)

            else:
                if tipo_de_documento_ingresado == 'DNI' or tipo_de_documento_ingresado == 'CUIL':
                    if ALUMNO.objects.filter(Q(dni=documento_ingresado) | Q(cuil=documento_ingresado)).exists():
                        contexto = self.get_context_data(**kwargs)
                        contexto['usuario_encontrado'] = True
                        contexto['vacio'] = False
                        return render(request, self.template_name, contexto)

                    else:
                        contexto = self.get_context_data(**kwargs)
                        contexto['usuario_encontrado'] = False
                        contexto['vacio'] = False
                        return render(request, self.template_name, contexto)
