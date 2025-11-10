from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Supervisor, EvaluacionSupervisor
from convenios.models import Convenio, Informe


@login_required
def lista_supervisores(request):
    """Vista para listar todos los supervisores con sus convenios asignados"""
    supervisores = Supervisor.objects.select_related('user').prefetch_related('convenios_asignados').all()
    
    # Estadísticas para las tarjetas
    supervisores_activos = Supervisor.objects.filter(estado='activo').count()
    informes_aprobados = Informe.objects.filter(estado='aprobado').count()
    informes_pendientes = Informe.objects.filter(estado='pendiente').count()
    
    context = {
        'supervisores': supervisores,
        'supervisores_activos': supervisores_activos,
        'informes_aprobados': informes_aprobados,
        'informes_pendientes': informes_pendientes,
    }
    
    return render(request, 'supervisores/lista_supervisores.html', context)


@login_required
def detalle_supervisor(request, supervisor_id):
    """Vista para mostrar el detalle de un supervisor y sus informes"""
    supervisor = get_object_or_404(Supervisor, id=supervisor_id)
    informes = Informe.objects.filter(supervisor=supervisor.user).order_by('-fecha_creacion')
    convenios_asignados = supervisor.convenios_asignados.all()
    evaluaciones = EvaluacionSupervisor.objects.filter(supervisor=supervisor).order_by('-fecha_evaluacion')
    
    context = {
        'supervisor': supervisor,
        'informes': informes,
        'convenios_asignados': convenios_asignados,
        'evaluaciones': evaluaciones,
    }
    
    return render(request, 'supervisores/detalle_supervisor.html', context)


@login_required
def crear_supervisor(request):
    """Vista para crear un nuevo supervisor"""
    if request.method == 'POST':
        # Aquí se procesaría el formulario
        pass
    
    usuarios_disponibles = User.objects.filter(perfilusuario__rol='supervisor', supervisor__isnull=True)
    
    context = {
        'usuarios_disponibles': usuarios_disponibles,
    }
    
    return render(request, 'supervisores/crear_supervisor.html', context)


@login_required
def editar_supervisor(request, supervisor_id):
    """Vista para editar un supervisor existente"""
    supervisor = get_object_or_404(Supervisor, id=supervisor_id)
    
    if request.method == 'POST':
        # Aquí se procesaría el formulario
        pass
    
    context = {
        'supervisor': supervisor,
    }
    
    return render(request, 'supervisores/editar_supervisor.html', context)


@login_required
def asignar_convenio_supervisor(request, supervisor_id):
    """Vista para asignar convenios a un supervisor"""
    supervisor = get_object_or_404(Supervisor, id=supervisor_id)
    
    if request.method == 'POST':
        convenio_id = request.POST.get('convenio_id')
        if convenio_id:
            convenio = get_object_or_404(Convenio, id=convenio_id)
            supervisor.convenios_asignados.add(convenio)
            messages.success(request, f'Convenio {convenio.empresa_entidad} asignado exitosamente.')
            return redirect('supervisores:detalle_supervisor', supervisor_id=supervisor_id)
    
    convenios_disponibles = Convenio.objects.exclude(supervisores_asignados=supervisor)
    
    context = {
        'supervisor': supervisor,
        'convenios_disponibles': convenios_disponibles,
    }
    
    return render(request, 'supervisores/asignar_convenio.html', context)


@login_required
def quitar_convenio_supervisor(request, supervisor_id, convenio_id):
    """Vista para quitar un convenio de un supervisor"""
    supervisor = get_object_or_404(Supervisor, id=supervisor_id)
    convenio = get_object_or_404(Convenio, id=convenio_id)
    
    if request.method == 'POST':
        supervisor.convenios_asignados.remove(convenio)
        messages.success(request, f'Convenio {convenio.empresa_entidad} removido exitosamente.')
        return redirect('supervisores:detalle_supervisor', supervisor_id=supervisor_id)
    
    context = {
        'supervisor': supervisor,
        'convenio': convenio,
    }
    
    return render(request, 'supervisores/quitar_convenio.html', context)


@login_required
def evaluar_supervisor(request, supervisor_id):
    """Vista para evaluar un supervisor"""
    supervisor = get_object_or_404(Supervisor, id=supervisor_id)
    
    if request.method == 'POST':
        # Aquí se procesaría el formulario de evaluación
        pass
    
    convenios_supervisor = supervisor.convenios_asignados.all()
    
    context = {
        'supervisor': supervisor,
        'convenios_supervisor': convenios_supervisor,
    }
    
    return render(request, 'supervisores/evaluar_supervisor.html', context)


@login_required
def enviar_alerta_supervisor(request, supervisor_id):
    """Vista para enviar una alerta a un supervisor"""
    supervisor = get_object_or_404(Supervisor, id=supervisor_id)
    
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        if mensaje:
            # Crear notificación
            from usuarios.models import Notificacion
            Notificacion.objects.create(
                usuario=supervisor.user,
                titulo="Alerta del Sistema",
                mensaje=mensaje,
                tipo='sistema'
            )
            messages.success(request, 'Alerta enviada exitosamente.')
            return redirect('supervisores:detalle_supervisor', supervisor_id=supervisor_id)
    
    context = {
        'supervisor': supervisor,
    }
    
    return render(request, 'supervisores/enviar_alerta.html', context)