from django.contrib import admin
from .models import PerfilUsuario, Notificacion


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'estado', 'ultimo_acceso']
    list_filter = ['rol', 'estado', 'fecha_creacion']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__email']
    list_editable = ['rol', 'estado']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo', 'leida', 'fecha_creacion']
    list_filter = ['tipo', 'leida', 'fecha_creacion']
    search_fields = ['titulo', 'mensaje', 'usuario__username']
    list_editable = ['leida']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']