from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('estudiante', 'Estudiante'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('pendiente', 'Pendiente'),
        ('inactivo', 'Inactivo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante', verbose_name="Rol")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True, verbose_name="Foto de Perfil")
    ultimo_acceso = models.DateTimeField(null=True, blank=True, verbose_name="Último Acceso")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_rol_display()}"
    
    @property
    def nombre_completo(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def iniciales(self):
        """Genera las iniciales del usuario para el avatar"""
        nombre = self.user.first_name or ''
        apellido = self.user.last_name or ''
        if nombre and apellido:
            return f"{nombre[0]}{apellido[0]}".upper()
        elif nombre:
            return nombre[0].upper()
        elif apellido:
            return apellido[0].upper()
        else:
            return self.user.username[:2].upper()


class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('convenio_vencimiento', 'Convenio por Vencer'),
        ('informe_pendiente', 'Informe Pendiente'),
        ('actividad_asignada', 'Actividad Asignada'),
        ('sistema', 'Notificación del Sistema'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones', verbose_name="Usuario")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, verbose_name="Tipo")
    leida = models.BooleanField(default=False, verbose_name="Leída")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Lectura")
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"