from django.db import models
from django.template.defaultfilters import slugify
from apps.usuarios.models import Usuario
# Create your models here.
class Categoria(models.Model):

    nombre = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nombre)
        super(Categoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Blog(models.Model):
    titulo = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(editable=False, null=True, max_length=250)
    resumen = models.TextField(null=True)
    contenido = models.TextField()
    categorias = models.ManyToManyField(Categoria)
    portada = models.ImageField(upload_to='portadas-blog', null=True)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vistas = models.PositiveIntegerField(default=0, blank=True, null=True)
    palabras_clave = models.CharField(max_length=800, null=True, blank=True) 
    estado = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo or u''