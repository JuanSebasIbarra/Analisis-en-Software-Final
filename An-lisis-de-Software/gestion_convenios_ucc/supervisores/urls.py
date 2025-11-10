from django.urls import path
from . import views

app_name = 'supervisores'

urlpatterns = [
    path('', views.lista_supervisores, name='lista_supervisores'),
    path('<int:supervisor_id>/', views.detalle_supervisor, name='detalle_supervisor'),
    path('crear/', views.crear_supervisor, name='crear_supervisor'),
    path('<int:supervisor_id>/editar/', views.editar_supervisor, name='editar_supervisor'),
    path('<int:supervisor_id>/asignar-convenio/', views.asignar_convenio_supervisor, name='asignar_convenio'),
    path('<int:supervisor_id>/quitar-convenio/<int:convenio_id>/', views.quitar_convenio_supervisor, name='quitar_convenio'),
    path('<int:supervisor_id>/evaluar/', views.evaluar_supervisor, name='evaluar_supervisor'),
    path('<int:supervisor_id>/enviar-alerta/', views.enviar_alerta_supervisor, name='enviar_alerta'),
]
