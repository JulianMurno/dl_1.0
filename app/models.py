from django.db import models

class Producto(models.Model):
    CATEGORIAS_CHOICES = [
        ('Covertores', 'Covertores - Cubrecamas'),
        ('Acolchado', 'Acolchado'),
        ('Bebe', 'Linea Bebé'),
        ('Hogar', 'Cocina'),
        ('Alimentación', 'Sábanas'),
        ('Juguetes', 'Accesorios'),
        ('Toallas', 'Toallas y Toallones'),
        ('Bano', 'Baño'),
        ('Almohadas', 'Almohadas'),
        ('Cortinas', 'Cortinas'),
        ('Frazadas', 'Frazadas'),
    ]
    DISPONIBILIDAD = [
        ("Disponible", "Disponible"),
        ("Sin stock", "Sin stock")
    ]

    codigo_proveedor = models.CharField(max_length=5, blank=True, default='/')
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_CHOICES)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    material = models.TextField(blank=True)
    medida = models.TextField(blank=True)
    tiene_stock = models.CharField(max_length=20, choices=DISPONIBILIDAD)
    precio_lista = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_contado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    es_oferta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.codigo_proveedor} - {self.nombre}"

    def get_categoria_display(self):
        return dict(self.CATEGORIAS_CHOICES).get(self.categoria)
