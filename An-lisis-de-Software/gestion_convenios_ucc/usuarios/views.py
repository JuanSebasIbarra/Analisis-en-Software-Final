from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import PerfilUsuario, Notificacion


@login_required
def lista_usuarios(request):
    """Vista para listar todos los usuarios"""
    usuarios = User.objects.select_related('perfilusuario').all().order_by('-date_joined')
    
    # Filtros
    rol = request.GET.get('rol')
    estado = request.GET.get('estado')
    busqueda = request.GET.get('busqueda')
    
    if rol and rol != 'todos':
        usuarios = usuarios.filter(perfilusuario__rol=rol)
    
    if estado and estado != 'todos':
        usuarios = usuarios.filter(perfilusuario__estado=estado)
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(username__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    # Estadísticas para las tarjetas
    total_usuarios = User.objects.count()
    supervisores_activos = User.objects.filter(perfilusuario__rol='supervisor', perfilusuario__estado='activo').count()
    estudiantes = User.objects.filter(perfilusuario__rol='estudiante').count()
    cuentas_inactivas = User.objects.filter(perfilusuario__estado='inactivo').count()
    
    context = {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'supervisores_activos': supervisores_activos,
        'estudiantes': estudiantes,
        'cuentas_inactivas': cuentas_inactivas,
        'filtros': {
            'rol': rol,
            'estado': estado,
            'busqueda': busqueda,
        }
    }
    
    return render(request, 'usuarios/lista_usuarios.html', context)


@login_required
def crear_usuario(request):
    """Vista para crear un nuevo usuario"""
    if request.method == 'POST':
        # Aquí se procesaría el formulario
        pass
    
    context = {}
    return render(request, 'usuarios/crear_usuario.html', context)


@login_required
def editar_usuario(request, usuario_id):
    """Vista para editar un usuario existente"""
    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        # Aquí se procesaría el formulario
        pass
    
    context = {
        'usuario': usuario,
    }
    
    return render(request, 'usuarios/editar_usuario.html', context)


@login_required
def eliminar_usuario(request, usuario_id):
    """Vista para eliminar un usuario"""
    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuario {usuario.username} eliminado exitosamente.')
        return redirect('usuarios:lista_usuarios')
    
    context = {
        'usuario': usuario,
    }
    
    return render(request, 'usuarios/eliminar_usuario.html', context)


@login_required
def perfil_usuario(request, usuario_id):
    """Vista para mostrar el perfil de un usuario"""
    usuario = get_object_or_404(User, id=usuario_id)
    
    try:
        perfil = usuario.perfilusuario
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    # Notificaciones del usuario
    notificaciones = Notificacion.objects.filter(usuario=usuario).order_by('-fecha_creacion')[:10]
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'notificaciones': notificaciones,
    }
    
    return render(request, 'usuarios/perfil_usuario.html', context)


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """Marca una notificación como leída"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    
    if not notificacion.leida:
        notificacion.leida = True
        notificacion.fecha_lectura = timezone.now()
        notificacion.save()
    
    return redirect('usuarios:perfil_usuario', usuario_id=request.user.id)