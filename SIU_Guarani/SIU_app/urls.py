from django.urls import path
from .views import *

app_name = 'SIU' #Se especifica un nombre, para distinguir las urls similares de diferentes apps.
urlpatterns = [
    path('logout/', CerrarSesion.as_view(), name='cerrar_sesion'),
    path('acceso/', Logeo.as_view(), name='acceso'),
    path('acceso/recuperar', OlvidoContrasenna.as_view(), name='recuperar'),
    path('acceso/alta_usuario_cursos', CreoUsuario.as_view(), name='alta_usuario'),
    path('inicio_alumno/', InicioAlumno.as_view(), name='inicio_alumno'),
    path('materia/', InscripcionMaterias.as_view(), name='materia'),
    path('examen/', InscripcionExamenes.as_view(), name='examen'),
    path('plan_estudio/', ReportesPlanDeEstudio.as_view(), name='plan_estudio'),
    path('inscripciones/', ReportesMisInscripciones.as_view(), name='inscripciones'),
    path('porcentaje_avance_carrera/', PromedioYPorcentaje.as_view(), name='porcentaje_avance_carrera'),
    path('datos_censales/', MisDatosPersonales.as_view(), name='datos_censales'),
    path('datos_censales/domicilio/', Domicilio.as_view(), name='domicilio'),
    path('datos_censales/datos_contacto', DatosContacto.as_view(), name='datos_contacto'),
    path('datos_censales/editar_datos_contacto/datos_contacto/', ConfiguracionDatosCelular.as_view(),
         name='editar_datos_contacto'),
    path('datos_censales/discapacidad', Discapacidad.as_view(), name='discapacidad'),
    path('configuracion/', Configuracion.as_view(), name='configuracion'),
]
