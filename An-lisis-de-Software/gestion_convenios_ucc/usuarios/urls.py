from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),
    path('<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('notificaciones/<int:notificacion_id>/leer/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
]
