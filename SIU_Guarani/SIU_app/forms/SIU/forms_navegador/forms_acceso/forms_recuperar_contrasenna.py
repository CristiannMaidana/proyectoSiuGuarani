from django import forms


class RecuperarContrasennaForm(forms.Form):
    opciones_documento = (
        ('DNI', '(DNI) Documetno Nacional de Identidad'),
        ('CUIL', '(CUIL) CUIL/CUIT')
    )

    tipo_de_documento = forms.ChoiceField(choices=opciones_documento, label='Tipo de documento', required=False,
                                          widget=forms.Select(attrs={'class': 'selec'}))
    numero_documento = forms.IntegerField(label='Número de documento (sin puntos ni guiones)', required=False,
                                          widget=forms.NumberInput(attrs={'class': 'input input_sin_flechas'}))
