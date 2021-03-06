from django.db import models
from django.template.defaultfilters import slugify
from apps.users.models import Usuario
from martor.models import MartorField
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
    titulo = models.CharField(max_length=350, unique=True)
    slug = models.SlugField(editable=False, null=True, max_length=250)
    resumen = models.TextField(null=True, max_length=1800)
    contenido = MartorField()
    categorias = models.ManyToManyField(Categoria)
    portada = models.ImageField(upload_to='portadas-blog', null=True)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vistas = models.PositiveIntegerField(default=0, blank=True, null=True)
    palabras_clave = models.CharField(max_length=800, null=True, blank=True) 
    estado = models.BooleanField(default=True)
    es_pricipal = models.BooleanField(default=False)
    posts_relacionados = models.ManyToManyField("self",
                                     verbose_name=("Posts relacionados"), blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo or u''

# De momento no se esta usando
class ContadorVisita(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contador = models.IntegerField()
    fecha_visita = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.blog, self.contador) or u''