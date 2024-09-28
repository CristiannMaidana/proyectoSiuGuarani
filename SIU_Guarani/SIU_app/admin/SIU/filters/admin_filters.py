from datetime import datetime, timedelta
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class RecentDateFilter(SimpleListFilter):
    title = 'Filtrar por fecha'
    parameter_name = 'recent'

    def lookups(self, request, model_admin):
        current_year = datetime.now().year
        return (
            ('last_7_days', 'Últimos 7 días'),
            ('last_30_days', 'Últimos 30 días'),
            ('this_year', f'{current_year}'),
            ('last_year', f'{current_year - 1}'),
            ('last_last_year', f'{current_year - 2}'),
            ('last_last_last_year', f'{current_year - 3}'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'last_7_days':
            return queryset.filter(fecha__gte=datetime.now()-timedelta(days=7))
        if self.value() == 'last_30_days':
            return queryset.filter(fecha__gte=datetime.now()-timedelta(days=30))
        if self.value() == 'this_year':
            return queryset.filter(fecha__year=datetime.now().year)
        if self.value() == 'last_year':
            return queryset.filter(fecha__year=datetime.now().year - 1)
        if self.value() == 'last_last_year':
            return queryset.filter(fecha__year=datetime.now().year - 1)
        if self.value() == 'last_last_last_year':
            return queryset.filter(fecha__year=datetime.now().year - 1)
        return queryset


class InscriptoMateriasFilter(SimpleListFilter):
    title = _('Materias inscriptas')
    parameter_name = 'Materias inscriptas'

    def lookups(self, request, model_admin):
        return (
            ('True', _('Sí')),
            ('False', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(id_cursada_alumno__inscripto=True)
        elif self.value() == 'False':
            return queryset.filter(id_cursada_alumno__inscripto=False)
        return queryset


class InscriptoExamenesFilter(SimpleListFilter):
    title = _('Examenes inscriptos')
    parameter_name = 'Examenes inscriptas'

    def lookups(self, request, model_admin):
        return (
            ('True', _('Sí')),
            ('False', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(id_examen_alumno__inscripto=True)
        elif self.value() == 'False':
            return queryset.filter(id_examen_alumno__inscripto=False)
        return queryset
