from django.contrib import admin
from .models import Supervisor, EvaluacionSupervisor


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ['user', 'codigo_supervisor', 'especialidad', 'experiencia_anos', 'estado']
    list_filter = ['estado', 'especialidad', 'fecha_ingreso']
    search_fields = ['user__first_name', 'user__last_name', 'codigo_supervisor', 'especialidad']
    list_editable = ['estado']
    date_hierarchy = 'fecha_ingreso'
    ordering = ['-fecha_creacion']
    filter_horizontal = ['convenios_asignados']


@admin.register(EvaluacionSupervisor)
class EvaluacionSupervisorAdmin(admin.ModelAdmin):
    list_display = ['supervisor', 'evaluador', 'convenio', 'calificacion_general', 'fecha_evaluacion']
    list_filter = ['calificacion_general', 'fecha_evaluacion']
    search_fields = ['supervisor__user__first_name', 'supervisor__user__last_name', 'evaluador__username']
    date_hierarchy = 'fecha_evaluacion'
    ordering = ['-fecha_evaluacion']