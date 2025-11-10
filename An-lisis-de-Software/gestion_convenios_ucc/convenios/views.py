from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Convenio, Informe, ActividadConvenio
from usuarios.models import PerfilUsuario, Notificacion
from supervisores.models import Supervisor


def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas generales
    total_convenios = Convenio.objects.count()
    convenios_activos = Convenio.objects.filter(estado='activo').count()
    convenios_por_vencer = Convenio.objects.filter(estado='por_vencer').count()
    convenios_vencidos = Convenio.objects.filter(estado='vencido').count()
    
    # Informes
    total_informes = Informe.objects.count()
    informes_pendientes = Informe.objects.filter(estado='pendiente').count()
    informes_aprobados = Informe.objects.filter(estado='aprobado').count()
    
    # Supervisores
    supervisores_activos = Supervisor.objects.filter(estado='activo').count()
    
    # Propuestas de estudiantes (simulado)
    propuestas_estudiantes = 3  # Este valor se puede calcular basado en actividades pendientes
    
    # Actividades recientes
    actividades_recientes = ActividadConvenio.objects.select_related('convenio', 'responsable').order_by('-fecha_creacion')[:5]
    
    # Convenios por vencer (próximos 2 meses)
    fecha_limite = timezone.now().date() + timedelta(days=60)
    convenios_por_vencer_detalle = Convenio.objects.filter(
        fecha_vencimiento__lte=fecha_limite,
        fecha_vencimiento__gte=timezone.now().date()
    ).select_related('supervisor')[:5]
    
    # Distribución por tipo de convenio
    distribucion_tipos = Convenio.objects.values('tipo').annotate(total=Count('id'))
    
    context = {
        'total_convenios': total_convenios,
        'convenios_activos': convenios_activos,
        'convenios_por_vencer': convenios_por_vencer,
        'convenios_vencidos': convenios_vencidos,
        'total_informes': total_informes,
        'informes_pendientes': informes_pendientes,
        'informes_aprobados': informes_aprobados,
        'supervisores_activos': supervisores_activos,
        'propuestas_estudiantes': propuestas_estudiantes,
        'actividades_recientes': actividades_recientes,
        'convenios_por_vencer_detalle': convenios_por_vencer_detalle,
        'distribucion_tipos': distribucion_tipos,
    }
    
    return render(request, 'convenios/dashboard.html', context)


@login_required
def lista_convenios(request):
    """Vista para listar todos los convenios"""
    convenios = Convenio.objects.select_related('supervisor').order_by('-fecha_creacion')
    
    # Filtros
    estado = request.GET.get('estado')
    tipo = request.GET.get('tipo')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    busqueda = request.GET.get('busqueda')
    
    if estado and estado != 'todos':
        convenios = convenios.filter(estado=estado)
    
    if tipo and tipo != 'todos':
        convenios = convenios.filter(tipo=tipo)
    
    if fecha_desde:
        convenios = convenios.filter(fecha_inicio__gte=fecha_desde)
    
    if fecha_hasta:
        convenios = convenios.filter(fecha_inicio__lte=fecha_hasta)
    
    if busqueda:
        convenios = convenios.filter(
            Q(empresa_entidad__icontains=busqueda) |
            Q(supervisor__first_name__icontains=busqueda) |
            Q(supervisor__last_name__icontains=busqueda)
        )
    
    # Estadísticas para las tarjetas
    convenios_activos_count = Convenio.objects.filter(estado='activo').count()
    convenios_por_vencer_count = Convenio.objects.filter(estado='por_vencer').count()
    convenios_vencidos_count = Convenio.objects.filter(estado='vencido').count()
    
    context = {
        'convenios': convenios,
        'convenios_activos_count': convenios_activos_count,
        'convenios_por_vencer_count': convenios_por_vencer_count,
        'convenios_vencidos_count': convenios_vencidos_count,
        'filtros': {
            'estado': estado,
            'tipo': tipo,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'busqueda': busqueda,
        }
    }
    
    return render(request, 'convenios/lista_convenios.html', context)


@login_required
def detalle_convenio(request, convenio_id):
    """Vista para mostrar el detalle de un convenio"""
    convenio = get_object_or_404(Convenio, id=convenio_id)
    informes = convenio.informes.all().order_by('-fecha_creacion')
    actividades = convenio.actividades.all().order_by('-fecha_creacion')
    
    context = {
        'convenio': convenio,
        'informes': informes,
        'actividades': actividades,
    }
    
    return render(request, 'convenios/detalle_convenio.html', context)


@login_required
def crear_convenio(request):
    """Vista para crear un nuevo convenio"""
    if request.method == 'POST':
        # Aquí se procesaría el formulario
        pass
    
    supervisores = User.objects.filter(perfilusuario__rol='supervisor')
    
    context = {
        'supervisores': supervisores,
    }
    
    return render(request, 'convenios/crear_convenio.html', context)


@login_required
def editar_convenio(request, convenio_id):
    """Vista para editar un convenio existente"""
    convenio = get_object_or_404(Convenio, id=convenio_id)
    
    if request.method == 'POST':
        # Aquí se procesaría el formulario
        pass
    
    supervisores = User.objects.filter(perfilusuario__rol='supervisor')
    
    context = {
        'convenio': convenio,
        'supervisores': supervisores,
    }
    
    return render(request, 'convenios/editar_convenio.html', context)


@login_required
def eliminar_convenio(request, convenio_id):
    """Vista para eliminar un convenio"""
    convenio = get_object_or_404(Convenio, id=convenio_id)
    
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios:lista_convenios')
    
    context = {
        'convenio': convenio,
    }
    
    return render(request, 'convenios/eliminar_convenio.html', context)