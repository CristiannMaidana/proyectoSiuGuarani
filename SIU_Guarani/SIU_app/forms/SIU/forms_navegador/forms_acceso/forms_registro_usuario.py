from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from SIU_app.models import CARRERA, DATOS_CONTACTO, ALUMNO, UNIVERSIDAD


class CreoUsuarioForm(UserCreationForm):
    opciones_genero = (
        ('', '--Seleccione--'),
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    )
    genero_select = forms.ChoiceField(label='Género(*)', choices=opciones_genero, required=False,
                                      widget=forms.Select(attrs={'class': 'selec'}))

    opciones_nacionalidad = (
        ('', '--Seleccione--'),
        ('Argentina', 'Argentino'),
    )
    nacionalidad_select = forms.ChoiceField(label='Nacionalidad(*)', choices=opciones_nacionalidad, required=False,
                                            widget=forms.Select(attrs={'class': 'selec'}))

    opciones_documento = (
        ('', '--Seleccione--'),
        ('DNI', 'Documento Nacional de Identidad'),
    )
    documento_select = forms.ChoiceField(label='Tipo de documento(*)', choices=opciones_documento, required=False,
                                         widget=forms.Select(attrs={'class': 'selec'}))

    carreras = CARRERA.objects.all().values_list('nombre_carrera', 'nombre_carrera')

    carrera_select = forms.ChoiceField(label='Tipo de carrera que pensás cursar(*)', choices=carreras, required=False,
                                       widget=forms.Select(attrs={'class': 'selec'}))

    documento_usuario = forms.IntegerField(label='Número de documento(*)', required=False,
                                           widget=forms.NumberInput(attrs={'class': 'input input_sin_flechas'}))

    cuil_usuario = forms.IntegerField(label='Número de cuil(*)', required=False,
                                      widget=forms.NumberInput(attrs={'class': 'input input_sin_flechas'}))

    apellido_usuario = forms.CharField(label='Apellido(*)', max_length=30, required=False,
                                       widget=forms.TextInput(attrs={'class': 'input'}))

    nombre_usuario = forms.CharField(label='Nombres(*)', max_length=30, required=False,
                                     widget=forms.TextInput(attrs={'class': 'input'}))

    numero_usuario = forms.IntegerField(label='Número de contacto(*)', required=False,
                                        widget=forms.NumberInput(attrs={'class': 'input input_sin_flechas'}))

    localidad_usuario = forms.CharField(label='Localidad(*)', max_length=50, required=False,
                                        widget=forms.TextInput(attrs={'class': 'input'}))

    pais_usuario = forms.CharField(label='País', max_length=50, required=False,
                                   widget=forms.TextInput(attrs={'id': 'pais', 'class': 'input'}))

    mail_usuario = forms.EmailField(label='E-mail(*)', max_length=30, required=False,
                                    widget=forms.EmailInput(attrs={'class': 'input'})
                                    )

    repito_mail_usuario = forms.EmailField(label='Repetir e-mail(*)', max_length=30, required=False,
                                           widget=forms.EmailInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "genero_select", "nacionalidad_select", "documento_select",
                  "cuil_usuario", "apellido_usuario", "nombre_usuario", "numero_usuario", "localidad_usuario",
                  "mail_usuario", "repito_mail_usuario", "documento_usuario",
                  "carrera_select"]

    def clean(self):
        cleaned_data = super().clean()

        documento = cleaned_data.get("documento_usuario")

        nombre = cleaned_data.get("nombre_usuario")
        apellido = cleaned_data.get("apellido_usuario")

        localidad = cleaned_data.get("localidad_usuario")

        email = cleaned_data.get("mail_usuario")
        repito_email = cleaned_data.get("repito_mail_usuario")

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        username = cleaned_data.get('username')

        numero = cleaned_data.get('numero_usuario')

        "Validacion de los correos"
        if email and repito_email:
            if DATOS_CONTACTO.objects.filter(correo=email).exists():
                self.add_error('repito_mail_usuario', "El mail ya esta registrado")
            if '@gmail.com' not in email and '@hotmail.com' not in email:
                self.add_error('repito_mail_usuario', "El formato del mail es invalido")
            if email and repito_email and email != repito_email:
                self.add_error('repito_mail_usuario', "No coinciden los correos")
        else:
            self.add_error('repito_mail_usuario', "El formato del mail es invalido")

        "Validacion del documento"
        if documento:
            if ALUMNO.objects.filter(dni=documento).exists():
                self.add_error('documento_usuario', "El documento ya esta registrado")
            elif len(str(documento)) > 8:
                self.add_error('documento_usuario', "El formato del documento es invalido")
        else:
            self.add_error('documento_usuario', "El formato del documento es invalido")

        "Validacion del nombre"
        if not nombre or any(char.isdigit() for char in nombre):
            self.add_error('nombre_usuario', "El formato del nombre es invalido")

        "Validacion del apellido"
        if not apellido or any(char.isdigit() for char in apellido):
            self.add_error('apellido_usuario', "El formato del apellido es invalido")

        "Validación de la contraseña"
        if not password1:
            self.add_error('password1', "El formato de contraseña es invalido")
        elif len(str(password1)) < 8:
            self.add_error('password1', "La contraseña es demasiado corta. Debe contener por lo menos 8 caracteres.")
        elif password2 != password1:
            self.add_error('password1', 'Los dos campos de contraseñas no coinciden entre si.')

        "Validación de la localidad"
        if any(char.isdigit() for char in localidad):
            self.add_error('localidad_usuario', "El formato del localidad es invalido")

        "Validación del usuario"
        if not username:
            self.add_error('username', "El formato del usuario es invalido")

        "Validación del numero"
        if numero:
            if DATOS_CONTACTO.objects.filter(numero_celular=numero).exists():
                self.add_error('numero_usuario', 'El numero ya esta registrado')
        else:
            self.add_error('numero_usuario', 'El formato del numero es invalido')
        return cleaned_data

    def save_datos_de_contacto(self):
        nuevo_datos_contacto = DATOS_CONTACTO(
            correo=self.cleaned_data['mail_usuario'],
            numero_celular=self.cleaned_data['numero_usuario'],
        )
        nuevo_datos_contacto.save()
        return nuevo_datos_contacto

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        self.save_nuevo_usuario(user)
        return user

    def save_nuevo_usuario(self, user):
        nuevo_usuario = ALUMNO(
            id_usuario=user,
            nombre=self.cleaned_data['nombre_usuario'],
            apellido=self.cleaned_data['apellido_usuario'],
            dni=self.cleaned_data['documento_usuario'],
            cuil=self.cleaned_data['documento_usuario'],
            legajo=self.cleaned_data['documento_usuario'],
            genero=self.cleaned_data['genero_select'],
            discapacidad=False,
            id_universidad=UNIVERSIDAD.objects.get(id_universidad=1),
            id_carrera=CARRERA.objects.get(nombre_carrera=self.cleaned_data['carrera_select']),
            id_datos_contacto=self.save_datos_de_contacto()
        )
        nuevo_usuario.save()

    def __init__(self, *args, **kwargs):
        super(CreoUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['class'] = 'input'
        self.fields['pais_usuario'].initial = 'Argentina'
