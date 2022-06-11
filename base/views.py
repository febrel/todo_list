from django.shortcuts import render, redirect
# Para todas las vitas list
from django.views.generic.list import ListView
# Para vista detallada
from django.views.generic.detail import DetailView
# Para vista edit
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Para dar atras den page
from django.urls import reverse_lazy

# Para loguin
from django.contrib.auth.views import LoginView
# Para que solo aparezca si esta autenticado
from django.contrib.auth.mixins import LoginRequiredMixin

# Para registro
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .models import Tarea


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    # Captura los forms
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tareas')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    # Funcion valida que sea correcto el registro de usuario
    def form_valid(self, form):
        user = form.save()

        if(user is not None):
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # Evita que los usarios logeados vuelvan mendiante redireccion a login
    def get(self, *args, **kwgars):
        if(self.request.user.is_authenticated):
            return redirect('tareas')
        return super(RegisterPage, self).get(*args, **kwgars)


class TareaListas(LoginRequiredMixin, ListView):
    # Debe quedar con model
    model = Tarea
    # Para cambiar el nombre en for
    context_object_name = 'tareas'

    # Metodo que filtra que solo se muestren las tareas del usuario logueado
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()

        # Retorna mediante el det
        search_input = self.request.GET.get('search-area') or ''

        # Cambia la forma como filtra
        if(search_input):
            context['tareas'] = context['tareas'].filter(
                titulo__startswith=search_input)

        # Entrada de busqueda
        context['search_input'] = search_input

        return context


class TareaDetalle(LoginRequiredMixin, DetailView):
    # Debe quedar con model
    model = Tarea
    # Para cambiar el nombre en for
    context_object_name = 'tarea'
    # template_name = 'base/tarea.html'


class TareaCrear(LoginRequiredMixin, CreateView):
    # Debe quedar con model
    model = Tarea
    # Captura los forms
    fields = ['titulo', 'descripcion', 'completo']
    # Para retroceder
    success_url = reverse_lazy('tareas')

    # Metodo para aceptar solo forms validos
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(TareaCrear, self).form_valid(form)


class TareaEditar(LoginRequiredMixin, UpdateView):
    # Debe quedar con model
    model = Tarea
    # Captura los forms
    fields = ['titulo', 'descripcion', 'completo']
    # Para retroceder
    success_url = reverse_lazy('tareas')


class TareaEliminar(LoginRequiredMixin, DeleteView):
    # Debe quedar con model
    model = Tarea
   # Para cambiar el nombre en for
    context_object_name = 'tarea'
    # Para retroceder
    success_url = reverse_lazy('tareas')
