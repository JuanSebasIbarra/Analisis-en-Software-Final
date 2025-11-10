from django.db import models
from django.contrib.auth.models import User
from convenios.models import Convenio, Informe


class Supervisor(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    codigo_supervisor = models.CharField(max_length=20, unique=True, verbose_name="Código de Supervisor")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    experiencia_anos = models.PositiveIntegerField(default=0, verbose_name="Años de Experiencia")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado")
    convenios_asignados = models.ManyToManyField(Convenio, blank=True, related_name='supervisores_asignados', verbose_name="Convenios Asignados")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.codigo_supervisor}"
    
    @property
    def nombre_completo(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def iniciales(self):
        """Genera las iniciales del supervisor para el avatar"""
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
    
    @property
    def total_informes(self):
        """Cuenta el total de informes del supervisor"""
        return Informe.objects.filter(supervisor=self.user).count()
    
    @property
    def informes_pendientes(self):
        """Cuenta los informes pendientes del supervisor"""
        return Informe.objects.filter(supervisor=self.user, estado='pendiente').count()
    
    @property
    def informes_aprobados(self):
        """Cuenta los informes aprobados del supervisor"""
        return Informe.objects.filter(supervisor=self.user, estado='aprobado').count()


class EvaluacionSupervisor(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, related_name='evaluaciones', verbose_name="Supervisor")
    evaluador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Evaluador")
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, verbose_name="Convenio")
    calificacion_general = models.PositiveIntegerField(verbose_name="Calificación General (1-10)")
    puntualidad = models.PositiveIntegerField(verbose_name="Puntualidad (1-10)")
    calidad_informes = models.PositiveIntegerField(verbose_name="Calidad de Informes (1-10)")
    comunicacion = models.PositiveIntegerField(verbose_name="Comunicación (1-10)")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_evaluacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Evaluación")
    
    class Meta:
        verbose_name = "Evaluación de Supervisor"
        verbose_name_plural = "Evaluaciones de Supervisores"
        ordering = ['-fecha_evaluacion']
    
    def __str__(self):
        return f"Evaluación de {self.supervisor.nombre_completo} - {self.convenio.empresa_entidad}"
    
    @property
    def promedio_calificacion(self):
        """Calcula el promedio de todas las calificaciones"""
        calificaciones = [
            self.calificacion_general,
            self.puntualidad,
            self.calidad_informes,
            self.comunicacion
        ]
        return sum(calificaciones) / len(calificaciones)