from django.contrib import admin
from ....models import CARRERA


class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre_carrera',)


admin.site.register(CARRERA, CarreraAdmin)
