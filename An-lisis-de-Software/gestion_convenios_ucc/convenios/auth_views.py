from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from usuarios.models import PerfilUsuario


def login_view(request):
    """Vista de login personalizada"""
    if request.user.is_authenticated:
        return redirect('convenios:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Actualizar último acceso en el perfil
                try:
                    perfil = user.perfilusuario
                    perfil.ultimo_acceso = timezone.now()
                    perfil.save()
                except PerfilUsuario.DoesNotExist:
                    pass
                
                # Configurar sesión persistente si "Recordarme" está marcado
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 días
                else:
                    request.session.set_expiry(0)  # Sesión de navegador
                
                messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')
                return redirect('convenios:dashboard')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, verifica tu usuario y contraseña.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('auth:login')


@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    try:
        perfil = request.user.perfilusuario
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    context = {
        'perfil': perfil,
    }
    
    return render(request, 'auth/profile.html', context)
