from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'convenios'

def redirect_to_login(request):
    return redirect('auth:login')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lista/', views.lista_convenios, name='lista_convenios'),
    path('<int:convenio_id>/', views.detalle_convenio, name='detalle_convenio'),
    path('crear/', views.crear_convenio, name='crear_convenio'),
    path('<int:convenio_id>/editar/', views.editar_convenio, name='editar_convenio'),
    path('<int:convenio_id>/eliminar/', views.eliminar_convenio, name='eliminar_convenio'),
]
