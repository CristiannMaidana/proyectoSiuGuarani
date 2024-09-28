from django import forms

from SIU_app.models import DIRECCION


class DomicilioForm(forms.Form):
    calle = forms.CharField(label='Calle(*)', max_length=100, required=False,
                            widget=forms.TextInput(attrs={'class': 'input'}))
    numero_calle = forms.IntegerField(label='Número(*)', required=False, widget=forms.NumberInput
                                      (attrs={'class': 'input input_compuesto input_sin_flechas'}))
    piso = forms.CharField(label='Piso', max_length=100, required=False,
                           widget=forms.TextInput(attrs={'class': 'input input_compuesto'}))
    departamento = forms.CharField(label='Departamento', max_length=100, required=False,
                                   widget=forms.TextInput(attrs={'class': 'input input_compuesto'}))
    unidad = forms.CharField(label='Unidad', max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'input input_compuesto'}))
    localidad = forms.CharField(label='Localidad(*)', max_length=100, required=False,
                                widget=forms.TextInput(attrs={'class': 'input'}))
    codigo_postal = forms.IntegerField(label='Código Postal(*)', required=False, widget=forms.NumberInput
                                       (attrs={'class': 'input input_compuesto input_sin_flechas'}))
    barrio = forms.CharField(label='Barrio', max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'input'}))
    opciones_vivienda = [
        ('', '--Seleccione--'),
        ('Casa / Departamento propio', 'Casa / Departamento propio'),
        ('Casa / Departamento alquilado', 'Casa / Departamento alquilado'),
        ('Residencia Universitaria', 'Residencia Universitaria'),
        ('Pensión', 'Pensión'),
        ('Otro', 'Otro'),
    ]

    tipo_vivienda = forms.ChoiceField(label='Tipo de vivienda', choices=opciones_vivienda, required=False,
                                      widget=forms.Select(attrs={'class': 'selec'}))

    opciones_convivencia = (
        ('', '--Seleccione--'),
        ('Con compañeros', 'Con compañeros'),
        ('Con familia de origen (padres, hermanos, abuelos)', 'Con familia de origen (padres, hermanos, abuelos)'),
        ('Con su pareja/hijos', 'Con su pareja/hijos'),
        ('Otros', 'Otros'),
        ('Solo', 'Solo'),
    )
    tipo_convivencia = forms.ChoiceField(label='¿Con quién vivis durante este período?', choices=opciones_convivencia,
                                         required=False, widget=forms.Select(attrs={'class': 'selec'}))

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario.id_direccion:
            if usuario.id_direccion.calle:
                self.fields['calle'].initial = usuario.id_direccion.calle
            if usuario.id_direccion.numero:
                self.fields['numero_calle'].initial = usuario.id_direccion.numero
            if usuario.id_direccion.piso:
                self.fields['piso'].initial = usuario.id_direccion.piso
            if usuario.id_direccion.departamento:
                self.fields['departamento'].initial = usuario.id_direccion.departamento
            if usuario.id_direccion.unidad:
                self.fields['unidad'].initial = usuario.id_direccion.unidad
            if usuario.id_direccion.localida:
                self.fields['localidad'].initial = usuario.id_direccion.localida
            if usuario.id_direccion.codigo_postal:
                self.fields['codigo_postal'].initial = usuario.id_direccion.codigo_postal
            if usuario.id_direccion.barrio:
                self.fields['barrio'].initial = usuario.id_direccion.barrio
            if usuario.id_direccion.tipo_de_vivienda:
                self.fields['tipo_vivienda'].initial = usuario.id_direccion.tipo_de_vivienda

    def save_domicilio(self, usuario):
        if usuario.id_direccion:
            usuario.id_direccion.calle = self.cleaned_data['calle']
            usuario.id_direccion.numero = self.cleaned_data['numero_calle']
            usuario.id_direccion.piso = self.cleaned_data['piso']
            usuario.id_direccion.departamento = self.cleaned_data['departamento']
            usuario.id_direccion.unidad = self.cleaned_data['unidad']
            usuario.id_direccion.localida = self.cleaned_data['localidad']
            usuario.id_direccion.codigo_postal = self.cleaned_data['codigo_postal']
            usuario.id_direccion.barrio = self.cleaned_data['barrio']
            usuario.id_direccion.tipo_de_vivienda = self.cleaned_data['tipo_vivienda']
            usuario.id_direccion.save()
            usuario.save()
        else:
            new_direccion = DIRECCION(
                calle=self.cleaned_data['calle'],
                numero=self.cleaned_data['numero_calle'],
                piso=self.cleaned_data['piso'],
                departamento=self.cleaned_data['departamento'],
                unidad=self.cleaned_data['unidad'],
                localida=self.cleaned_data['localidad'],
                codigo_postal=self.cleaned_data['codigo_postal'],
                barrio=self.cleaned_data['barrio'],
                tipo_de_vivienda=self.cleaned_data['tipo_vivienda'],
            )
            new_direccion.save()
            usuario.id_direccion = new_direccion
            usuario.save()
