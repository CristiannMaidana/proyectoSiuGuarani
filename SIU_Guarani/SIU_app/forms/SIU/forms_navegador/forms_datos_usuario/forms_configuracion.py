from django import forms


class ConfiguracionForm(forms.Form):
    contrasenna_actual = forms.CharField(label='Contraseña actual', required=False, widget=forms.PasswordInput(
        attrs={'class': 'input', 'id': 'contrasenna_actual'}))
    contrasenna_nueva = forms.CharField(label='Nueva contraseña', required=False, widget=forms.PasswordInput(
        attrs={'class': 'input', 'id': 'contrasenna_nueva'}))
    confirmar_contrasenna_nueva = forms.CharField(label='Confirmar contraseña', required=False,
                                                  widget=forms.PasswordInput
                                                  (attrs={'class': 'input', 'id': 'confirmar_contrasenna'}))
    mail = forms.CharField(label='E-mail', required=False,
                           widget=forms.EmailInput(attrs={'class': 'input', 'id': 'mail'}))

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mail'].initial = usuario.id_datos_contacto.correo

    def save_contrasenna(self, usuario):
        usuario.id_usuario.set_password(self.cleaned_data['contrasenna_nueva'])
        usuario.id_usuario.save()

    def save_mail(self, usuario):
        usuario.id_datos_contacto.correo = self.cleaned_data['mail']
        usuario.id_datos_contacto.save()
