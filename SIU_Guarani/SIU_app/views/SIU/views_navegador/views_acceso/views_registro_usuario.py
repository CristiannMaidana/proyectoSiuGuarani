from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from SIU_app.forms import CreoUsuarioForm
from SIU_app.models import CARRERA, ALUMNO


class CreoUsuario(TemplateView):
    template_name = "SIU/acceso/registro_usuario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todas_carreras'] = CARRERA.objects.all()
        context['form'] = CreoUsuarioForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CreoUsuarioForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Se logea automaticamente y se envia a la pagina principal
            request.session['usuario_id'] = ALUMNO.objects.get(id_usuario=user).id_alumno
            return HttpResponseRedirect('/inicio_alumno/')
        else:
            contexto = self.get_context_data(**kwargs)
            contexto['form'] = form
            contexto['error'] = True
            return render(request, self.template_name, contexto)
