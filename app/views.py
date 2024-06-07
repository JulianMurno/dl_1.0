from django.shortcuts import render, redirect
from .models import Producto
from django.db.models import Q
from django.core.paginator import Paginator

def custom_404(request, exception):
    return redirect('home')

def home(request):
    productos_mas_vendidos = Producto.objects.filter(categoria__in=['Covertores', 'Acolchado', 'Bebe'])[:9]
    productos_oferta = Producto.objects.filter(es_oferta=True)[:6]

    return render(request, 'home.html', {'productos_mas_vendidos': productos_mas_vendidos, 'productos_oferta': productos_oferta})


def productos(request):
    nombre = request.GET.get('nombre', '')
    categoria = request.GET.get('categoria', '')
    es_oferta = request.GET.get('es_oferta', '')

    productos = Producto.objects.all()

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    
    if categoria:
        productos = productos.filter(categoria=categoria)
    
    if es_oferta == 'True':
        productos = productos.filter(es_oferta=True)

    productos = productos.order_by('nombre')

    paginator = Paginator(productos, 12)  # Puedes ajustar el número de productos por página según sea necesario
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'selected_nombre': nombre,
        'selected_categoria': categoria,
        'categorias': Producto.CATEGORIAS_CHOICES,
        'disponibilidad': Producto.DISPONIBILIDAD,
        'es_oferta': es_oferta,
    }
    return render(request, 'productos.html', context)
