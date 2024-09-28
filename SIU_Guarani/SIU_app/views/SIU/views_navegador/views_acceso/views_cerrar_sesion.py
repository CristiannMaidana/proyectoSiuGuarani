from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView


class CerrarSesion(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('SIU:acceso')
