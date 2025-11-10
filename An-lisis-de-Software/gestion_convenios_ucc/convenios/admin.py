from django.contrib import admin
from .models import Convenio, Informe, ActividadConvenio


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ['empresa_entidad', 'tipo', 'fecha_inicio', 'fecha_vencimiento', 'estado', 'supervisor']
    list_filter = ['tipo', 'estado', 'fecha_inicio', 'fecha_vencimiento']
    search_fields = ['empresa_entidad', 'descripcion']
    list_editable = ['estado']
    date_hierarchy = 'fecha_inicio'
    ordering = ['-fecha_creacion']


@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'convenio', 'supervisor', 'estado', 'fecha_entrega']
    list_filter = ['estado', 'fecha_entrega', 'convenio__tipo']
    search_fields = ['titulo', 'descripcion']
    list_editable = ['estado']
    date_hierarchy = 'fecha_entrega'
    ordering = ['-fecha_creacion']


@admin.register(ActividadConvenio)
class ActividadConvenioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'convenio', 'fecha_inicio', 'fecha_fin', 'responsable', 'completada']
    list_filter = ['completada', 'fecha_inicio', 'convenio__tipo']
    search_fields = ['titulo', 'descripcion']
    list_editable = ['completada']
    date_hierarchy = 'fecha_inicio'
    ordering = ['-fecha_creacion']