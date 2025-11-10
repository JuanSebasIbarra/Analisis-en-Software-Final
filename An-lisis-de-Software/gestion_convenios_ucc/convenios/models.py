from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Convenio(models.Model):
    TIPO_CHOICES = [
        ('marco', 'Marco'),
        ('practicas', 'Prácticas'),
        ('bienestar', 'Bienestar'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('por_vencer', 'Por vencer'),
        ('vencido', 'Vencido'),
        ('revision', 'En revisión'),
        ('juridico', 'En jurídico'),
        ('firma', 'En firma'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    empresa_entidad = models.CharField(max_length=200, verbose_name="Empresa/Entidad")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado")
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Supervisor")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    archivo_convenio = models.FileField(upload_to='convenios/', blank=True, null=True, verbose_name="Archivo del Convenio")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.empresa_entidad} - {self.get_tipo_display()}"
    
    @property
    def dias_para_vencer(self):
        """Calcula los días restantes para el vencimiento"""
        hoy = timezone.now().date()
        dias = (self.fecha_vencimiento - hoy).days
        return dias
    
    @property
    def esta_por_vencer(self):
        """Verifica si el convenio está por vencer (menos de 60 días)"""
        return 0 <= self.dias_para_vencer <= 60
    
    @property
    def esta_vencido(self):
        """Verifica si el convenio está vencido"""
        return self.dias_para_vencer < 0


class Informe(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='informes', verbose_name="Convenio")
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Supervisor")
    titulo = models.CharField(max_length=200, verbose_name="Título del Informe")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    archivo_informe = models.FileField(upload_to='informes/', verbose_name="Archivo del Informe")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    fecha_entrega = models.DateField(verbose_name="Fecha de Entrega")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = "Informe"
        verbose_name_plural = "Informes"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.convenio.empresa_entidad}"


class ActividadConvenio(models.Model):
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='actividades', verbose_name="Convenio")
    titulo = models.CharField(max_length=200, verbose_name="Título de la Actividad")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsable")
    completada = models.BooleanField(default=False, verbose_name="Completada")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        verbose_name = "Actividad de Convenio"
        verbose_name_plural = "Actividades de Convenios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.convenio.empresa_entidad}"