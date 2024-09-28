from django import forms


class DatosPersonalesForm(forms.Form):
    apellido = forms.CharField(label='Apellido', required=False,
                               widget=forms.TextInput(attrs={'id': 'apellido', 'class': 'input'}))

    nombre = forms.CharField(label='Nombres', required=False,
                             widget=forms.TextInput(attrs={'id': 'nombre', 'class': 'input'}))

    tipo_de_documento = forms.CharField(label='Tipo de documento', required=False,
                                        widget=forms.TextInput(attrs={'id': 'tipo_documento', 'class': 'input'}))
    numero_de_documento = forms.IntegerField(label='Número de documento', required=False,
                                             widget=forms.NumberInput
                                             (attrs={'id': 'numero_documento', 'class': 'input'}))
    numero_de_cuil = forms.IntegerField(label='Número de CUIL (sin guiones)', required=False,
                                        widget=forms.NumberInput(attrs={'id': 'numero_cuil', 'class': 'input'}))
    genero = forms.CharField(label='Género', required=False,
                             widget=forms.TextInput(attrs={'id': 'genero', 'class': 'input'}))

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apellido'].initial = usuario.apellido
        self.fields['nombre'].initial = usuario.nombre
        self.fields['tipo_de_documento'].initial = 'Documento Nacional de Identidad'
        self.fields['numero_de_documento'].initial = usuario.dni
        self.fields['numero_de_cuil'].initial = usuario.cuil
        self.fields['genero'].initial = usuario.genero

    def save_datos_personales(self, usuario):
        usuario.dni = self.cleaned_data['dni']
        usuario.apellido = self.cleaned_data['apellido']
        usuario.nombre = self.cleaned_data['nombre']
        usuario.cuil = self.cleaned_data['cuil']
        usuario.genero = self.cleaned_data['genero']
        usuario.save()
