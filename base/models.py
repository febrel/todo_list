from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Tarea(models.Model):
    # Para cuando elimine el usuario se borre todas las tareas
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    completo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    # Retorna solo el titulo de la tarea
    def __str__(self):
        return self.titulo

    # Ordena por atributo completo
    class Meta:
        ordering = ['completo']
