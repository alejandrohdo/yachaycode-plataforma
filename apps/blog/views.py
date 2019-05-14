from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import Blog as Blogs, Categoria
from django.db.models import Q
# para paginador
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class Blog(ListView):
    """docstring for ver_todas_tortas"""
    context_object_name = 'blogs'
    template_name = 'blog/blog.html'
    queryset = Blogs.objects.filter(
        estado=True).order_by('fecha_publicacion')

    def get_context_data(self, *args, **kwargs):
        context_data = super(Blog, self).get_context_data(*args, **kwargs)
        # realizamos consulta de todos los categorias de blogs
        context_data['categorias_blog'] = Categoria.objects.all()
        return context_data

class Detalle_blog(DetailView):
    """docstring for Detalle_curso"""
    # ordenar los modulos segun el orden de creacion
    context_object_name = 'detalle_blog'
    template_name = "blog/detalle_blog.html"
    model = Blogs
    slug_field = 'slug'


def buscador_blog(request):


    """docstring for Busqueda"""
    # todo tipo de buscador siempre buscara con cualquier parámetro, 
    # siempre en cuando este estado = TRUE, inidica que está activo
    consulta = request.GET.get('q', '')
    lista_blogs = None
    if consulta:
        lista_blogs = Blogs.objects.filter(
            Q(titulo__icontains=consulta) |
            Q(resumen__icontains=consulta) |
            Q(palabras_clave__icontains=consulta) |
            Q(categorias__nombre__icontains=consulta), estado=True).distinct()
    # else:
        # en caso si alguien entra directamente a /busquedas
        # lista_blogs = Curso.objects.all().order_by('-fecha_creacion')[:2]
    # paginandor
    paginator = Paginator(lista_blogs, 9)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    categorias = Categoria.objects.all()

    return render(request, 'blog/buscador_blog.html',
                  {'blogs': blogs, 'categorias': categorias})


def buscador_categoria(request, slug):
    try:
        consulta = Blogs.objects.filter(
            categorias__slug=slug)
        categorias = Categoria.objects.all()
        return render(request, 'blog/buscador_blog.html',
                      {'blogs': consulta, 'categorias': categorias})
    except Exception as e:
        raise 

class AcercaDe(TemplateView):
    template_name = 'blog/nosotros.html'

@csrf_exempt 
def contador_visitas(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            estado = False
            blog = get_object_or_404(Blogs, 
                estado=True, pk=request.POST.get('id'))
            blog.vistas +=1
            blog.save()
            estado = True
            response = JsonResponse({'estado': estado})
            return HttpResponse(response.content)            
        except Exception as e:
            print ("Error:", e)
            response = JsonResponse({'estado': estado, 'error': str(e)})
            return HttpResponse(response.content)            
    else:
        return redirect('/')

def tags(request, slug):
    try:
        consulta = Blogs.objects.filter(
            categorias__slug=slug)
        categorias = Categoria.objects.all()
        return render(request, 'blog/categorias.html',
                      {'blogs': consulta, 'slug': slug})
    except Exception as e:
        raise e