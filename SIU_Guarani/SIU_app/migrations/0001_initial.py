# Generated by Django 5.1.1 on 2024-09-27 23:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ANNIO',
            fields=[
                ('id_annio', models.AutoField(primary_key=True, serialize=False)),
                ('numero_annio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CARRERA',
            fields=[
                ('id_carrera', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_carrera', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DATOS_CONTACTO',
            fields=[
                ('id_datos_contacto', models.AutoField(primary_key=True, serialize=False)),
                ('numero_celular', models.BigIntegerField(unique=True)),
                ('correo', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DIRECCION',
            fields=[
                ('id_direccion', models.AutoField(primary_key=True, serialize=False)),
                ('calle', models.CharField(blank=True, max_length=100, null=True)),
                ('barrio', models.CharField(blank=True, max_length=100, null=True)),
                ('piso', models.CharField(blank=True, max_length=100, null=True)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
                ('unidad', models.CharField(blank=True, max_length=100, null=True)),
                ('localida', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_de_vivienda', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('codigo_postal', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FAMILIA',
            fields=[
                ('id_familia', models.AutoField(primary_key=True, serialize=False)),
                ('mama', models.CharField(blank=True, max_length=10, null=True)),
                ('papa', models.CharField(blank=True, max_length=10, null=True)),
                ('hijos', models.CharField(blank=True, max_length=10, null=True)),
                ('cantidad_familia_cargo', models.CharField(blank=True, max_length=10, null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UNIVERSIDAD',
            fields=[
                ('id_universidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_universidad', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ALUMNO',
            fields=[
                ('id_alumno', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('dni', models.BigIntegerField(unique=True)),
                ('legajo', models.BigIntegerField(unique=True)),
                ('cuil', models.BigIntegerField(unique=True)),
                ('genero', models.CharField(blank=True, max_length=30, null=True)),
                ('discapacidad', models.BooleanField(blank=True, null=True)),
                ('id_usuario', models.OneToOneField(db_column='id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('id_carrera', models.ForeignKey(db_column='id_carrera', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.carrera')),
                ('id_datos_contacto', models.ForeignKey(blank=True, db_column='id_datos_contacto', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.datos_contacto')),
                ('id_direccion', models.ForeignKey(blank=True, db_column='id_direccion', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.direccion')),
                ('id_familia', models.ForeignKey(blank=True, db_column='id_familia', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.familia')),
                ('id_universidad', models.ForeignKey(db_column='id_universidad', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.universidad')),
            ],
        ),
        migrations.CreateModel(
            name='CUATRIMESTRE',
            fields=[
                ('id_cuatrimestre', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cuatrimestre', models.CharField(max_length=30)),
                ('id_annio', models.ForeignKey(db_column='id_annio', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.annio')),
            ],
        ),
        migrations.CreateModel(
            name='DURACION',
            fields=[
                ('id_duracion', models.AutoField(primary_key=True, serialize=False)),
                ('id_annio', models.ForeignKey(db_column='id_annio', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.annio')),
                ('id_carrea', models.ForeignKey(db_column='id_carrea', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='MATERIA',
            fields=[
                ('id_materia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_materia', models.CharField(max_length=100, unique=True)),
                ('correlativa', models.ForeignKey(blank=True, db_column='correlativa', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia')),
                ('id_cuatrimestre', models.ForeignKey(db_column='id_cuatrimestre', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.cuatrimestre')),
            ],
        ),
        migrations.CreateModel(
            name='EXAMEN',
            fields=[
                ('id_examen', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_examen', models.CharField(max_length=40)),
                ('nota_examen', models.FloatField(blank=True, null=True)),
                ('id_materia', models.ForeignKey(db_column='id_materia', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia')),
            ],
        ),
        migrations.CreateModel(
            name='MATERIA_CON_EXAMEN',
            fields=[
                ('id_materia_con_examen', models.AutoField(primary_key=True, serialize=False)),
                ('id_examen', models.ForeignKey(db_column='id_examen', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.examen')),
                ('id_materia', models.ForeignKey(db_column='id_materia', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia')),
            ],
        ),
        migrations.CreateModel(
            name='EXAMEN_ALUMNO',
            fields=[
                ('id_examen_alumno', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('aprobo', models.BooleanField(blank=True, null=True)),
                ('inscripto', models.BooleanField(blank=True, null=True)),
                ('id_alumno', models.ForeignKey(db_column='id_alumno', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.alumno')),
                ('id_materia_con_examen', models.ForeignKey(blank=True, db_column='id_materia_con_examen', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia_con_examen')),
            ],
        ),
        migrations.CreateModel(
            name='MATERIA_CON_PARCIAL',
            fields=[
                ('id_materia_con_parcial', models.AutoField(primary_key=True, serialize=False)),
                ('id_materia', models.ForeignKey(db_column='id_materia', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia')),
            ],
        ),
        migrations.CreateModel(
            name='CURSADA_ALUMNO',
            fields=[
                ('id_cursada_alumno', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('aprobo', models.BooleanField(blank=True, null=True)),
                ('inscripto', models.BooleanField(blank=True, null=True)),
                ('id_alumno', models.ForeignKey(db_column='id_alumno', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.alumno')),
                ('id_materia_con_parcial', models.ForeignKey(db_column='id_materia_con_parcial', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia_con_parcial')),
            ],
        ),
        migrations.CreateModel(
            name='PARCIAL',
            fields=[
                ('id_parcial', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_parcial', models.CharField(blank=True, max_length=40, null=True)),
                ('nota_parcial', models.FloatField(blank=True, null=True)),
                ('nota_recuperatorio', models.FloatField(blank=True, null=True)),
                ('nota_promocion', models.FloatField(blank=True, null=True)),
                ('id_materia', models.ForeignKey(db_column='id_materia', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia')),
            ],
        ),
        migrations.AddField(
            model_name='materia_con_parcial',
            name='id_primer_parcial',
            field=models.ForeignKey(db_column='id_primer_parcial', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.parcial'),
        ),
        migrations.AddField(
            model_name='materia_con_parcial',
            name='id_segundo_parcial',
            field=models.ForeignKey(db_column='id_segundo_parcial', on_delete=django.db.models.deletion.DO_NOTHING, related_name='materiasconparciales_id_segundo_parcial_set', to='SIU_app.parcial'),
        ),
        migrations.CreateModel(
            name='PLAN_DE_ESTUDIO',
            fields=[
                ('id_plan_de_estudio', models.AutoField(primary_key=True, serialize=False)),
                ('id_annio', models.ForeignKey(db_column='id_annio', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.annio')),
                ('id_cuatrimestre', models.ForeignKey(db_column='id_cuatrimestre', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.cuatrimestre')),
                ('id_materia', models.ForeignKey(db_column='id_materia', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.materia')),
            ],
        ),
        migrations.CreateModel(
            name='HISTORIAL_ACADEMICO',
            fields=[
                ('id_historial_academico', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('id_alumno', models.ForeignKey(db_column='id_alumno', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.alumno')),
                ('id_cursada_alumno', models.ForeignKey(blank=True, db_column='id_cursada_alumno', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.cursada_alumno')),
                ('id_examen_alumno', models.ForeignKey(blank=True, db_column='id_examen_alumno', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.examen_alumno')),
                ('id_plan_de_estudio', models.ForeignKey(db_column='id_plan_de_estudio', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.plan_de_estudio')),
            ],
        ),
        migrations.AddField(
            model_name='carrera',
            name='id_universidad',
            field=models.ForeignKey(db_column='id_universidad', on_delete=django.db.models.deletion.DO_NOTHING, to='SIU_app.universidad'),
        ),
    ]
