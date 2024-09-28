from datetime import datetime, date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Subquery
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import ALUMNO, HISTORIAL_ACADEMICO, CURSADA_ALUMNO, MATERIA_CON_PARCIAL, MATERIA, PARCIAL, \
    PLAN_DE_ESTUDIO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class InscripcionMaterias(TemplateView):
    template_name = 'SIU/inscripciones/inscripcion_materias.html'

    def get_usuario(self):
        return ALUMNO.objects.get(id_alumno=self.request.session.get('usuario_id'))

    @staticmethod
    def get_periodo_inscripcion_materias_regulares(start_date, end_date, period_days=15):
        """
        Verifica si la fecha actual está dentro de un período de tiempo definido desde la fecha de inicio.

        Args:
        - start_date (datetime): Fecha de inicio del período.
        - end_date (datetime): Fecha de fin del período.
        - period_days (int): Número de días que define el período de tiempo (por defecto, 15 días).

        Returns:
        - bool: True si la fecha actual está dentro del período, False en caso contrario.
        """
        current_date = datetime.now()

        # Definir el periodo como una duración de tiempo
        period_duration = timedelta(days=period_days)

        # Calcular la fecha final del periodo desde la fecha de inicio
        period_end_date = start_date + period_duration

        # Verificar si la fecha actual está dentro del periodo de tiempo definido
        return start_date <= current_date <= end_date and current_date <= period_end_date

    def get_historial_academico_de_alumno(self):
        usuario = self.get_usuario()
        return HISTORIAL_ACADEMICO.objects.filter(id_alumno=usuario.id_alumno)

    def get_materias_pendientes(self):
        historial_academico_alumno = self.get_historial_academico_de_alumno()

        materias_aprobadas_subquery = historial_academico_alumno.filter(
            Q(id_cursada_alumno__aprobo=True) | Q(id_cursada_alumno__inscripto=True)
        ).values('id_cursada_alumno__id_materia_con_parcial__id_materia')

        materias_pendientes = PLAN_DE_ESTUDIO.objects.exclude(
            id_materia__in=Subquery(materias_aprobadas_subquery)
        )
        return materias_pendientes

    def get_cursada_alumno(self):
        materias_inscriptas = HISTORIAL_ACADEMICO.objects.filter(
            Q(id_alumno=self.request.session.get('usuario_id')) &
            Q(id_cursada_alumno__inscripto=True)
        ).values_list('id_cursada_alumno__id_materia_con_parcial__id_materia__nombre_materia', flat=True)
        return materias_inscriptas

    def get_context_data(self, **kwargs):
        #La fecha de inicio de inscripcion de materias
        start_date = datetime(2024, 6, 30)

        #La fecha de fin de inscripcion de materias
        end_date = datetime(2024, 7, 15)

        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = self.get_usuario()
        contexto['periodo_inscripcion'] = self.get_periodo_inscripcion_materias_regulares(start_date, end_date)
        contexto['mi_lista'] = self.get_materias_pendientes()
        contexto['historial_academico'] = self.get_historial_academico_de_alumno()
        contexto['usuario_cursada'] = self.get_cursada_alumno()
        return contexto

    @staticmethod
    def creo_materia_con_parcial(materia_seleccionado):
        materia = MATERIA.objects.get(nombre_materia=materia_seleccionado)
        nueva_materia_notas = MATERIA_CON_PARCIAL(
            id_materia=MATERIA.objects.get(nombre_materia=materia_seleccionado),
            id_primer_parcial=PARCIAL(
                nombre_parcial="primer_parcial_prueba",
                id_materia=materia,
                nota_parcial=0,
                nota_recuperatorio=0,
                nota_promocion=0
            ),
            id_segundo_parcial=PARCIAL(
                nombre_parcial="segundo_parcial_prueba",
                id_materia=materia,
                nota_parcial=0,
                nota_recuperatorio=0,
                nota_promocion=0
            ),
        )
        nueva_materia_notas.id_primer_parcial.save()
        nueva_materia_notas.id_segundo_parcial.save()
        nueva_materia_notas.save()
        return nueva_materia_notas

    def creo_cursada_alumno(self, materia_seleccionado):
        nueva_tupla_cursada = CURSADA_ALUMNO(
            fecha=datetime.now(),
            aprobo=False,
            inscripto=True,
            id_alumno=self.get_usuario(),
            id_materia_con_parcial=self.creo_materia_con_parcial(materia_seleccionado)
        )
        nueva_tupla_cursada.save()
        return nueva_tupla_cursada

    def creo_historial_academico(self, nombre_materia_inscripta):
        #Busco la correlativa de la materia a inscribirse
        correlativa = MATERIA.objects.get(nombre_materia=nombre_materia_inscripta).correlativa
        if correlativa:
            try:
                curso_correlativa = HISTORIAL_ACADEMICO.objects.get(
                    Q(id_plan_de_estudio__id_materia__nombre_materia=correlativa) &
                    Q(id_alumno=self.request.session.get('usuario_id')) &
                    Q(id_cursada_alumno__aprobo=True)
                )
                if curso_correlativa:
                    nuevo_historial = HISTORIAL_ACADEMICO(
                        id_alumno=self.get_usuario(),
                        fecha=date.today(),
                        id_cursada_alumno=self.creo_cursada_alumno(nombre_materia_inscripta),
                        id_plan_de_estudio=PLAN_DE_ESTUDIO.objects.get(
                            id_materia__nombre_materia=nombre_materia_inscripta),
                    )
                    nuevo_historial.save()  # crea un nuevo historial del alumno
                    return True, correlativa
                else:
                    return False, correlativa
            except HISTORIAL_ACADEMICO.DoesNotExist:
                return False, correlativa
        else:
            nuevo_historial = HISTORIAL_ACADEMICO(
                id_alumno=self.get_usuario(),
                fecha=date.today(),
                id_cursada_alumno=self.creo_cursada_alumno(nombre_materia_inscripta),
                id_plan_de_estudio=PLAN_DE_ESTUDIO.objects.get(id_materia__nombre_materia=nombre_materia_inscripta),
            )
            nuevo_historial.save()  # crea un nuevo historial del alumno
            return True, correlativa

    @staticmethod
    def elimino_historial_academico(id_eliminar):
        tupla_a_eliminar = HISTORIAL_ACADEMICO.objects.get(id_historial_academico=id_eliminar)
        primer_parcial_eliminar = tupla_a_eliminar.id_cursada_alumno.id_materia_con_parcial.id_primer_parcial
        segundo_parcial_eliminar = tupla_a_eliminar.id_cursada_alumno.id_materia_con_parcial.id_segundo_parcial
        relacion_materias_notas_eliminar = tupla_a_eliminar.id_cursada_alumno.id_materia_con_parcial
        relacion_cursada_alumno = tupla_a_eliminar.id_cursada_alumno
        tupla_a_eliminar.delete()
        relacion_cursada_alumno.delete()
        relacion_materias_notas_eliminar.delete()
        segundo_parcial_eliminar.delete()
        primer_parcial_eliminar.delete()

    def post(self, request, *args, **kwargs):
        nombre_nueva_materia_inscripta = request.POST.get('elemento_seleccionado')
        id_materia_a_dar_baja = request.POST.get('dar_de_baja_materia_id')
        boton_dar_de_baja = request.POST.get('confirmar_baja')
        id_historial_academico_eliminar = request.POST.get('id_eliminar')

        if id_materia_a_dar_baja is not None:
            contexto = self.get_context_data()
            contexto['dar_de_baja'] = True
            contexto['nombre_materia_baja'] = HISTORIAL_ACADEMICO.objects.get(
                id_historial_academico=id_materia_a_dar_baja).id_plan_de_estudio.id_materia.nombre_materia
            contexto['id_eliminar'] = id_materia_a_dar_baja
            return render(request, self.template_name, contexto)

        if nombre_nueva_materia_inscripta is not None:
            historial_academico_creado, correlativa = self.creo_historial_academico(nombre_nueva_materia_inscripta)
            if historial_academico_creado:
                contexto = self.get_context_data()
                return render(request, self.template_name, contexto)
            else:
                contexto = self.get_context_data()
                contexto['no_curso_correlativa'] = True
                contexto['nombre_correlativa'] = correlativa.nombre_materia
                return render(request, self.template_name, contexto)

        if boton_dar_de_baja == "True":
            self.elimino_historial_academico(id_historial_academico_eliminar)
            contexto = self.get_context_data()
            return render(request, self.template_name, contexto)

        else:
            contexto = self.get_context_data()
            return render(request, self.template_name, contexto)
