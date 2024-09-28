from django import forms

from SIU_app.models import FAMILIA


class SituacionFamiliarForm(forms.Form):
    opciones_estado_civil = [
        ('', '--Seleccione--'),
        ('Casado', 'Casado'),
        ('Divorciado', 'Divorciado'),
        ('Separado', 'Separado'),
        ('Soltero', 'Soltero'),
        ('Unión consensual', 'Unión consensual'),
        ('Viudo', 'Viudo')
    ]

    opciones_cantidad_hijos = [
        ('', '--Seleccione--'),
        ('No tiene', 'No tiene'),
        ('Uno', 'Uno'),
        ('Dos', 'Dos'),
        ('Mas de uno', 'Mas de uno'),
    ]

    opciones_cantidad_familiares = [
        ('', '--Seleccione--'),
        ('No tiene', 'No tiene'),
        ('Uno', 'Uno'),
        ('Dos', 'Dos'),
        ('Mas de uno', 'Mas de uno'),
    ]

    opciones_situacion_padre = [
        ('', '--Seleccione--'),
        ('Vive', 'Vive'),
        ('No vive', 'No vive'),
        ('Desconoce', 'Desconoce'),
    ]

    opciones_situacion_madre = [
        ('', '--Seleccione--'),
        ('Vive', 'Vive'),
        ('No vive', 'No vive'),
        ('Desconoce', 'Desconoce'),
    ]

    estado_civil = forms.ChoiceField(label='Estado civil (*)', choices=opciones_estado_civil, required=False,
                                     widget=forms.Select(attrs={'class': 'selec'}))
    cantidad_hijos = forms.ChoiceField(label='Cantidad de hijos', choices=opciones_cantidad_hijos, required=False,
                                       widget=forms.Select(attrs={'class': 'selec'}))
    cantidad_familiares = forms.ChoiceField(label='Cantidad de familiares a cargo',
                                            choices=opciones_cantidad_familiares, required=False,
                                            widget=forms.Select(attrs={'class': 'selec'}))
    situacion_padre = forms.ChoiceField(label='Situación de tu padre (*)', choices=opciones_situacion_padre,
                                        required=False, widget=forms.Select(attrs={'class': 'selec'}))
    situacion_madre = forms.ChoiceField(label='Situación de tu madre (*)', choices=opciones_situacion_madre,
                                        required=False, widget=forms.Select(attrs={'class': 'selec'}))

    def __init__(self, usuario, *args, **kwargs):
        super(SituacionFamiliarForm, self).__init__(*args, **kwargs)
        if usuario.id_familia:
            if usuario.id_familia.estado_civil:
                self.fields['estado_civil'].initial = usuario.id_familia.estado_civil
            if usuario.id_familia.hijos:
                self.fields['cantidad_hijos'].initial = usuario.id_familia.hijos
            if usuario.id_familia.cantidad_familia_cargo:
                self.fields['cantidad_familiares'].initial = usuario.id_familia.cantidad_familia_cargo
            if usuario.id_familia.papa:
                self.fields['situacion_padre'].initial = usuario.id_familia.papa
            if usuario.id_familia.mama:
                self.fields['situacion_madre'].initial = usuario.id_familia.mama
        else:
            self.fields['estado_civil'].initial = '--Seleccione--'
            self.fields['cantidad_hijos'].initial = '--Seleccione--'
            self.fields['cantidad_familiares'].initial = '--Seleccione--'
            self.fields['situacion_padre'].initial = '--Seleccione--'
            self.fields['situacion_madre'].initial = '--Seleccione--'

    def save_datos_familia(self, usuario):
        if usuario.id_familia:
            usuario.id_familia.estado_civil = self.cleaned_data['estado_civil']
            usuario.id_familia.hijos = self.cleaned_data['cantidad_hijos']
            usuario.id_familia.cantidad_familia_cargo = self.cleaned_data['cantidad_familiares']
            usuario.id_familia.mama = self.cleaned_data['situacion_madre']
            usuario.id_familia.papa = self.cleaned_data['situacion_padre']
            usuario.id_familia.save()
            usuario.save()
        else:
            nueva_familia = FAMILIA(
                estado_civil=self.cleaned_data['estado_civil'],
                hijos=self.cleaned_data['cantidad_hijos'],
                cantidad_familia_cargo=self.cleaned_data['cantidad_familiares'],
                mama=self.cleaned_data['situacion_madre'],
                papa=self.cleaned_data['situacion_padre'],
            )
            nueva_familia.save()
            usuario.id_familia = nueva_familia
            usuario.save()
