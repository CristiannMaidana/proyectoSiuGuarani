from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages


def mostrar_carrera_universitaria(modeladmin, request, queryset):
    carreras = []
    for alumno in queryset:
        carreras.append(alumno.id_carrera.id_carrera)
    if carreras:
        url = reverse('admin:SIU_app_carrera_change', args=[carreras[0]])
    else:
        return HttpResponse("No se encontraron carreras para los alumnos seleccionados.")
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_carrera_universitaria.short_description = "Mostrar carrera universitaria de los alumnos seleccionados"


def mostrar_cursada_alumno(modeladmin, request, queryset):
    for historial in queryset:
        historial_id_alumno = historial.id_alumno.id_alumno
        historial_id_cursada = historial.id_cursada_alumno.id_cursada_alumno
    url = reverse('admin:SIU_app_cursada_alumno_changelist') + f'?id_alumno__id_alumno__exact={historial_id_alumno}&id_cursada_alumno={historial_id_cursada}'
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_cursada_alumno.short_description = "Mostrar cursada alumno"


def mostrar_historial_academico(modeladmin, request, queryset):
    for alumno in queryset:
        alumno = alumno.id_alumno
    url = reverse('admin:SIU_app_historial_academico_changelist') + f'?id_alumno__id_alumno__exact={alumno}'
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_historial_academico.short_description = "Mostrar historial academico del alumno seleccionado"


def mostrar_materia_con_parcial(modeladmin, request, queryset):
    for cursada_alumno in queryset:
        materia_con_parcial = cursada_alumno.id_materia_con_parcial.id_materia_con_parcial
    url = reverse('admin:SIU_app_materia_con_parcial_changelist') + f'?id_materia_con_parcial={materia_con_parcial}'
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_materia_con_parcial.short_description = "Mostrar las notas de la materia"


def mostrar_parciales(modeladmin, request, queryset):
    for parciales in queryset:
        parcial_uno = parciales.id_primer_parcial.id_parcial
        parcial_dos = parciales.id_segundo_parcial.id_parcial
    url = reverse('admin:SIU_app_parcial_changelist') + f'?id_parcial__in={parcial_uno}&id_parcial__in={parcial_dos}'
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_parciales.short_description = "Muestro Parciales"


def mostrar_materia_con_examen(modeladmin, request, queryset):
    for examen_alumno in queryset:
        examen_con_nota = examen_alumno.id_materia_con_examen.id_materia_con_examen
    url = reverse('admin:SIU_app_materia_con_examen_changelist') + f'?id_materia_con_examen={examen_con_nota}'
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_materia_con_examen.short_description = "Mostrar materia con examen"


def mostrar_examen_alumno(modeladmin, request, queryset):
    for historial in queryset:
        if historial.id_examen_alumno:
            historial_id_alumno = historial.id_alumno.id_alumno
            historial_examen_alumno = historial.id_examen_alumno.id_examen_alumno
            url = reverse('admin:SIU_app_examen_alumno_changelist') + f'?id_alumno__id_alumno__exact={historial_id_alumno}&id_examen_alumno={historial_examen_alumno}'
            return HttpResponse(f'<script>window.location.href="{url}"</script>')
        else:
            alumno = historial.id_alumno.id_alumno
            url = reverse('admin:SIU_app_historial_academico_changelist') + f'?id_alumno__id_alumno__exact={alumno}'
            modeladmin.message_user(request, 'Ocurrió un error: el historial no tiene un examen asignado.', level=messages.ERROR)
            return HttpResponse(f'<script>window.location.href="{url}"</script>')


mostrar_examen_alumno.short_description = "Mostrar examen alumno"


def cargo_notas_examen(modeladmin, request, queryset):
    for examen in queryset:
        examen = examen.id_examen.id_examen
    url = reverse('admin:SIU_app_examen_changelist') + f'?id_examen__in={examen}'
    return HttpResponse(f'<script>window.location.href="{url}"</script>')


cargo_notas_examen.short_description = "Cargar notas examen"
