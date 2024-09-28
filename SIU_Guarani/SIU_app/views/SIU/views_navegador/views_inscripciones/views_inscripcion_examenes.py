from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from SIU_app.models import ALUMNO, EXAMEN_ALUMNO, MATERIA_CON_EXAMEN, EXAMEN, MATERIA, HISTORIAL_ACADEMICO, \
    PLAN_DE_ESTUDIO


@method_decorator(login_required(login_url='/acceso/'), name='dispatch')
class InscripcionExamenes(TemplateView):
    template_name = "SIU/inscripciones/inscripcion_examenes.html"

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
        return HISTORIAL_ACADEMICO.objects.filter(id_alumno=self.request.session.get('usuario_id'))

    def get_examenes_pendientes(self):
        historial_academico_alumno = self.get_historial_academico_de_alumno()

        # Crear subconsulta para obtener los ID de materias aprobadas o inscritas
        materias_aprobadas_subquery = historial_academico_alumno.filter(
            Q(id_examen_alumno__aprobo=True) | Q(id_examen_alumno__inscripto=True)
        ).values('id_examen_alumno__id_materia_con_examen__id_materia')

        # Filtrar las materias pendientes
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
        end_date = datetime(2024, 7, 10)

        contexto = super().get_context_data(**kwargs)
        contexto['usuario'] = self.get_usuario()
        contexto['periodo_inscripcion'] = self.get_periodo_inscripcion_materias_regulares(start_date, end_date)
        contexto['mi_lista'] = self.get_examenes_pendientes()
        contexto['historial_academico'] = self.get_historial_academico_de_alumno()
        contexto['usuario_cursada'] = self.get_cursada_alumno()
        return contexto

    @staticmethod
    def creo_materia_con_examen(materia_seleccionado):
        materia = MATERIA.objects.get(nombre_materia=materia_seleccionado)
        nueva_materia_con_examen = MATERIA_CON_EXAMEN(
            id_examen=EXAMEN(
                nombre_examen="Examne_final_1",
                nota_examen=0,
                id_materia=materia,
            ),
            id_materia=materia,
        )
        nueva_materia_con_examen.id_examen.save()
        nueva_materia_con_examen.save()
        return nueva_materia_con_examen

    def creo_examen_alumno(self, materia_seleccionado):
        nueva_tupla_examen_alumno = EXAMEN_ALUMNO(
            fecha=datetime.now(),
            aprobo=False,
            inscripto=True,
            id_alumno=self.get_usuario(),
            id_materia_con_examen=self.creo_materia_con_examen(materia_seleccionado),
        )
        nueva_tupla_examen_alumno.save()
        return nueva_tupla_examen_alumno

    def creo_historial_academico(self, nombre_examen):
        #Busco el historial academico del alumno
        curso_materia = self.get_historial_academico_de_alumno()

        #Busco en su historial academico si curso la materia que se quiere inscribir
        query_tupla_curso_materia = curso_materia.filter(id_plan_de_estudio__id_materia__nombre_materia=nombre_examen)

        #Busco en la materia encontrada si la aprobo
        query_materia_aprobada = query_tupla_curso_materia.filter(id_cursada_alumno__aprobo=True)

        if query_materia_aprobada.exists():
            tupla_curso_materia = query_materia_aprobada.get()
            tupla_curso_materia.id_examen_alumno = self.creo_examen_alumno(nombre_examen)
            tupla_curso_materia.save()
            return True
        else:
            return False

    @staticmethod
    def elimino_historial_academico(id_eliminar):
        # Obtiene la entrada del historial académico
        historial = HISTORIAL_ACADEMICO.objects.get(id_historial_academico=id_eliminar)

        # Almacena las referencias antes de eliminar el historial
        examen_alumno_a_eliminar = historial.id_examen_alumno
        relacion_materia_con_examen_a_eliminar = historial.id_examen_alumno.id_materia_con_examen
        examen = historial.id_examen_alumno.id_materia_con_examen.id_examen

        # Actualiza el historial académico para eliminar la referencia
        historial.id_examen_alumno = None
        historial.save()

        # Ahora, elimina las otras tablas en el orden correcto
        examen_alumno_a_eliminar.delete()
        relacion_materia_con_examen_a_eliminar.delete()
        examen.delete()

    def post(self, request, *args, **kwargs):
        nombre_examen_a_inscribirse = request.POST.get('elemento_seleccionado')
        id_materia_dar_de_baja = request.POST.get('dar_de_baja_materia_id')
        boton_dar_de_baja = request.POST.get('confirmar_baja')
        id_eliminar = request.POST.get('id_eliminar')

        if id_materia_dar_de_baja is not None:
            contexto = self.get_context_data()
            contexto['dar_de_baja'] = True
            contexto['id_eliminar'] = id_materia_dar_de_baja
            return render(request, self.template_name, contexto)

        if nombre_examen_a_inscribirse is not None:
            inscripcion_examen_realizada = self.creo_historial_academico(nombre_examen_a_inscribirse)
            if inscripcion_examen_realizada:
                contexto = self.get_context_data()
                return render(request, self.template_name, contexto)
            else:
                contexto = self.get_context_data()
                contexto['no_curso'] = True
                contexto['nombre_materia'] = nombre_examen_a_inscribirse
                return render(request, self.template_name, contexto)

        if boton_dar_de_baja == "True":
            self.elimino_historial_academico(id_eliminar)
            contexto = self.get_context_data()
            return render(request, self.template_name, contexto)
        else:
            contexto = self.get_context_data()
            return render(request, self.template_name, contexto)
