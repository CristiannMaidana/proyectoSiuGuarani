from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ALUMNO(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.BigIntegerField(unique=True)
    legajo = models.BigIntegerField(unique=True)
    cuil = models.BigIntegerField(unique=True)
    genero = models.CharField(max_length=30, blank=True, null=True)
    discapacidad = models.BooleanField(blank=True, null=True)
    id_universidad = models.ForeignKey('UNIVERSIDAD', models.DO_NOTHING, db_column='id_universidad')
    id_carrera = models.ForeignKey('CARRERA', models.DO_NOTHING, db_column='id_carrera')
    id_familia = models.ForeignKey('FAMILIA', models.DO_NOTHING, db_column='id_familia', blank=True, null=True)
    id_direccion = models.ForeignKey('DIRECCION', models.DO_NOTHING, db_column='id_direccion', blank=True,
                                     null=True)
    id_datos_contacto = models.ForeignKey('DATOS_CONTACTO', models.DO_NOTHING, db_column='id_datos_contacto',
                                          blank=True, null=True)
    id_usuario = models.OneToOneField(User, models.DO_NOTHING, db_column='id', null=True)

    def __str__(self):
        return f"{self.dni} {self.nombre} {self.apellido}"


class ANNIO(models.Model):
    id_annio = models.AutoField(primary_key=True)
    numero_annio = models.IntegerField()


class CARRERA(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre_carrera = models.CharField(max_length=30)
    id_universidad = models.ForeignKey('UNIVERSIDAD', models.DO_NOTHING, db_column='id_universidad')

    def __str__(self):
        return f"{self.nombre_carrera}"


class CUATRIMESTRE(models.Model):
    id_cuatrimestre = models.AutoField(primary_key=True)
    nombre_cuatrimestre = models.CharField(max_length=30)
    id_annio = models.ForeignKey(ANNIO, models.DO_NOTHING, db_column='id_annio')


class DATOS_CONTACTO(models.Model):
    id_datos_contacto = models.AutoField(primary_key=True)
    numero_celular = models.BigIntegerField(unique=True)
    correo = models.CharField(unique=True, max_length=100)


class DIRECCION(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=100, blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    piso = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    unidad = models.CharField(max_length=100, blank=True, null=True)
    localida = models.CharField(max_length=200, blank=True, null=True)
    tipo_de_vivienda = models.CharField(max_length=100, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    codigo_postal = models.IntegerField(blank=True, null=True)


class DURACION(models.Model):
    id_duracion = models.AutoField(primary_key=True)
    id_carrea = models.ForeignKey(CARRERA, models.DO_NOTHING, db_column='id_carrea')
    id_annio = models.ForeignKey(ANNIO, models.DO_NOTHING, db_column='id_annio')


class FAMILIA(models.Model):
    id_familia = models.AutoField(primary_key=True)
    mama = models.CharField(max_length=10, blank=True, null=True)
    papa = models.CharField(max_length=10, blank=True, null=True)
    hijos = models.CharField(max_length=10, blank=True, null=True)
    cantidad_familia_cargo = models.CharField(max_length=10, blank=True, null=True)
    estado_civil = models.CharField(max_length=10, blank=True, null=True)


class MATERIA(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(unique=True, max_length=100)
    id_cuatrimestre = models.ForeignKey(CUATRIMESTRE, models.DO_NOTHING, db_column='id_cuatrimestre')
    correlativa = models.ForeignKey('self', models.DO_NOTHING, db_column='correlativa', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_materia}"


class PARCIAL(models.Model):
    id_parcial = models.AutoField(primary_key=True)
    nombre_parcial = models.CharField(max_length=40, blank=True, null=True)
    nota_parcial = models.FloatField(blank=True, null=True)
    nota_recuperatorio = models.FloatField(blank=True, null=True)
    nota_promocion = models.FloatField(blank=True, null=True)
    id_materia = models.ForeignKey(MATERIA, models.DO_NOTHING, db_column='id_materia')

    def __str__(self):
        return f"Parcial para: {self.id_materia.nombre_materia}"


class UNIVERSIDAD(models.Model):
    id_universidad = models.AutoField(primary_key=True)
    nombre_universidad = models.CharField(max_length=100, blank=True, null=True)


class PLAN_DE_ESTUDIO(models.Model):
    id_plan_de_estudio = models.AutoField(primary_key=True)
    id_materia = models.ForeignKey(MATERIA, models.DO_NOTHING, db_column='id_materia')
    id_annio = models.ForeignKey(ANNIO, models.DO_NOTHING, db_column='id_annio')
    id_cuatrimestre = models.ForeignKey(CUATRIMESTRE, models.DO_NOTHING, db_column='id_cuatrimestre')


class MATERIA_CON_PARCIAL(models.Model):
    id_materia_con_parcial = models.AutoField(primary_key=True)
    id_materia = models.ForeignKey(MATERIA, models.DO_NOTHING, db_column='id_materia')
    id_primer_parcial = models.ForeignKey(PARCIAL, models.DO_NOTHING, db_column='id_primer_parcial')
    id_segundo_parcial = models.ForeignKey(PARCIAL, models.DO_NOTHING, db_column='id_segundo_parcial',
                                           related_name='materiasconparciales_id_segundo_parcial_set')

    def __str__(self):
        return f"{self.id_materia.nombre_materia}"


class CURSADA_ALUMNO(models.Model):
    id_cursada_alumno = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(ALUMNO, models.DO_NOTHING, db_column='id_alumno')
    id_materia_con_parcial = models.ForeignKey(MATERIA_CON_PARCIAL, models.DO_NOTHING,
                                               db_column='id_materia_con_parcial')
    fecha = models.DateField(blank=True, null=True)
    aprobo = models.BooleanField(blank=True, null=True)
    inscripto = models.BooleanField(blank=True, null=True)

    def __str__(self):
        if self.inscripto:
            return f"Inscripto a: {self.id_materia_con_parcial.id_materia.nombre_materia}, {self.fecha}"
        else:
            return f"No inscripto {self.fecha}"


class EXAMEN(models.Model):
    id_examen = models.AutoField(primary_key=True)
    nombre_examen = models.CharField(max_length=40)
    nota_examen = models.FloatField(blank=True, null=True)
    id_materia = models.ForeignKey(MATERIA, models.DO_NOTHING, db_column='id_materia')

    def __str__(self):
        return f"Examen para: {self.id_materia.nombre_materia}"


class MATERIA_CON_EXAMEN(models.Model):
    id_materia_con_examen = models.AutoField(primary_key=True)
    id_materia = models.ForeignKey(MATERIA, models.DO_NOTHING, db_column='id_materia')
    id_examen = models.ForeignKey(EXAMEN, models.DO_NOTHING, db_column='id_examen')

    def __str__(self):
        return f"{self.id_materia.nombre_materia}"


class EXAMEN_ALUMNO(models.Model):
    id_examen_alumno = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(ALUMNO, models.DO_NOTHING, db_column='id_alumno')
    id_materia_con_examen = models.ForeignKey(MATERIA_CON_EXAMEN, models.DO_NOTHING, db_column='id_materia_con_examen',
                                              blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    aprobo = models.BooleanField(blank=True, null=True)
    inscripto = models.BooleanField(blank=True, null=True)

    def __str__(self):
        if self.inscripto:
            return f"Inscripto {self.fecha}"
        else:
            return f"No inscripto {self.fecha}"


class HISTORIAL_ACADEMICO(models.Model):
    id_historial_academico = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    id_alumno = models.ForeignKey(ALUMNO, models.DO_NOTHING, db_column='id_alumno')
    id_cursada_alumno = models.ForeignKey(CURSADA_ALUMNO, models.DO_NOTHING, db_column='id_cursada_alumno', blank=True,
                                          null=True)
    id_examen_alumno = models.ForeignKey(EXAMEN_ALUMNO, models.DO_NOTHING, db_column='id_examen_alumno', blank=True,
                                         null=True)
    id_plan_de_estudio = models.ForeignKey(PLAN_DE_ESTUDIO, models.DO_NOTHING, db_column='id_plan_de_estudio')
