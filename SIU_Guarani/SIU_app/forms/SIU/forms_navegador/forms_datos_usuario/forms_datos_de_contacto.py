from django import forms


class DatosDeContactoForm(forms.Form):
    tipo_de_contacto = forms.CharField(label='Tipo(*)', required=False,
                                       widget=forms.TextInput(attrs={'class': 'input'}))
    cod_area = forms.IntegerField(label='Cod.área', required=False,
                                  widget=forms.NumberInput(attrs={'class': 'input input_compuesto input_sin_flechas'}))
    numero = forms.IntegerField(label='Número', required=False,
                                widget=forms.NumberInput(attrs={'class': 'input input_sin_flechas'}))

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_de_contacto'].initial = 'Teléfono Celular'
        self.fields['cod_area'].initial = '2901'
        self.fields['numero'].initial = usuario.id_datos_contacto.numero_celular

    def save_numero(self, usuario):
        usuario.id_datos_contacto.numero_celular = self.cleaned_data['numero']
        usuario.id_datos_contacto.save()
        usuario.save()
