from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

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

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.esta_agotado:
        messages.error(request, "❌ Este producto está agotado y no se puede agregar al carrito.")
        return redirect('detalle_producto', producto_id=producto.id)

    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    request.session['carrito'] = carrito
    messages.success(request, "Producto agregado al carrito.")
    return redirect('detalle_producto', producto_id=producto.id)

def carrito(request):
    carrito = request.session.get('carrito', {})
    productos_en_carrito = []

    total = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)

        # Validación: si no tiene precio, se ignora o se asigna 0
        if producto.precio_contado is None or producto.precio_lista is None:
            subtotal = 0
        else:
            subtotal = float(producto.precio_contado) * cantidad

        total += subtotal

        productos_en_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    context = {
        'productos_en_carrito': productos_en_carrito,
        'total': total,
    }

    return render(request, 'carrito.html', context)

def quitar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        return redirect('carrito')  # Redirigimos a la vista del carrito

    return JsonResponse({'error': 'Producto no encontrado en el carrito'}, status=404)

def checkout(request):
    carrito = request.session.get('carrito', {})
    productos_en_carrito = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        if producto.precio_contado:
            subtotal = float(producto.precio_contado) * cantidad
            total += subtotal
            productos_en_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal,
            })

    import json
    from django.core.serializers.json import DjangoJSONEncoder

    context = {
        'productos_en_carrito': productos_en_carrito,
        'total': total,
        'productos_json': json.dumps([
            {
                'nombre': item['producto'].nombre,
                'cantidad': item['cantidad'],
                'subtotal': item['subtotal']
            } for item in productos_en_carrito
        ], cls=DjangoJSONEncoder),
    }

    return render(request, 'checkout.html', context)

