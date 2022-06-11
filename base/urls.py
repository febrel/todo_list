from django.urls import path
from .views import TareaListas, TareaDetalle, TareaCrear, TareaEditar, TareaEliminar, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),


    path('', TareaListas.as_view(), name='tareas'),
    path('tarea/<int:pk>/', TareaDetalle.as_view(), name='tarea'),
    path('crear-tarea/', TareaCrear.as_view(), name='tarea-crear'),
    path('editar-tarea/<int:pk>/', TareaEditar.as_view(), name='tarea-editar'),
    path('elimina-tarea/<int:pk>/', TareaEliminar.as_view(), name='tarea-elimina'),
]
