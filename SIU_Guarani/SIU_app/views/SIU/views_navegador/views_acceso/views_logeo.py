from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from SIU_app.forms import LogeoForm
from SIU_app.models import ALUMNO


class Logeo(TemplateView):
    template_name = "SIU/acceso/acceso.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LogeoForm()
        return context

    def post(self, request, *args, **kwargs):
        form = LogeoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['usuario_id'] = ALUMNO.objects.get(id_usuario=user).id_alumno
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('SIU:inicio_alumno')
            else:
                usuario_incorrecto = True
                return render(request, self.template_name, {'form': form, 'usuario_incorrecto': usuario_incorrecto})
        else:
            return redirect(self.template_name)
