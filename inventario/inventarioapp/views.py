from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render 
from .models import Inventario, Producto, TablaHashUsuarios, Usuario, ListaProveedores, Proveedor, OrdenCompra
from django.contrib import messages
tabla_usuarios = TablaHashUsuarios()
usuario1 = Usuario("Juan", "juan@gmail.com", "contraseña123", "comprador")
usuario2 = Usuario("Ana", "ana@gmail.com", "otracontraseña", "vendedor")
usuario3 = Usuario("Admin", "admin@gmail.com", "admin", "admin")

tabla_usuarios.agregar_usuario(usuario1)
tabla_usuarios.agregar_usuario(usuario2)
tabla_usuarios.agregar_usuario(usuario3)

inventario = Inventario()
inventario.insertar(Producto(1, "Manzana", "Frutas", "Manzana", 10, 10000))
inventario.insertar(Producto(2, "Coca Cola", "Bebidas", "Coca Cola", 20, 1000))
inventario.insertar(Producto(3, "Pepsi", "Bebidas", "Pepsi", 30, 10))
inventario.insertar(Producto(4, "Sprite", "Bebidas", "Sprite", 40, 10))
inventario.insertar(Producto(5, "Fanta", "Bebidas", "Fanta", 50, 10))

lista_proveedores = ListaProveedores()
lista_proveedores.agregar_proveedor(1,"pepe","Carrera 42 # 54-77", "31463266","ejemplo1@gmail.com")
lista_proveedores.agregar_proveedor(8,"pepe2","Calle 100 # 11B-27", "31463759","ejemplo2@gmail.com")
lista_proveedores.agregar_proveedor(3,"pepe3","Carrera 20 B # 29-18", "31463581","ejemplo3@gmail.com")

cola_ordenes = []

def agregar_orden(producto, proveedor, cantidad):
    orden = OrdenCompra(producto, proveedor, cantidad)
    cola_ordenes.append(orden)
    print(f"Orden de compra agregada: {orden.producto} - Proveedor: {orden.proveedor} - Cantidad: {orden.cantidad}")

def procesar_ordenes():
    while cola_ordenes:
        orden = cola_ordenes.pop(0)
        print(f"Procesando orden de compra: {orden.producto} - Proveedor: {orden.proveedor} - Cantidad: {orden.cantidad} - Fecha y hora: {orden.fecha_hora}")

def obtener_ordenes_en_diccionario():
    ordenes_en_diccionario = []
    for orden in cola_ordenes:
        orden_dict = {
            'producto': orden.producto,
            "nombre_producto":(inventario.buscar(int(orden.producto))).nombre,
            'proveedor': orden.proveedor,
            'nombre_proveedor': lista_proveedores.buscar_proveedor_por_codigo(int(orden.proveedor)).nombre,
            'cantidad': orden.cantidad,
            'fecha_hora': orden.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
        }
        ordenes_en_diccionario.append(orden_dict)
    return ordenes_en_diccionario

agregar_orden("1", "3", 50)
agregar_orden("2", "8", 30)
agregar_orden("3", "1", 20)

def index(request):
     template = loader.get_template("inventarioapp/login.html")
     return HttpResponse(template.render( {'Periodos': ''}, request))  

def catalogo(request):
     template = loader.get_template("inventarioapp/catalogo.html")

     results =inventario.obtener_productos()
     return HttpResponse(template.render( {'Productos': results}, request))    
  
def nuevo_producto(request):
    context = {"dummy": 'dummy'}
    return render(request, "inventarioapp/nuevo_producto.html", context)

def crear_producto(request):
     if request.method=="POST":
          p=Producto(int(request.POST.get('codigo')),
                     request.POST.get('nombre'),
                     request.POST.get('categoria'),
                     request.POST.get('marca'),
                     int(request.POST.get('stock')),
                     int(request.POST.get('min_stock')))

          inventario.insertar(p)
          messages.success(request, "se creo el nuevo proceso")
          template = loader.get_template("inventarioapp/catalogo.html")
          results =inventario.obtener_productos()
          return HttpResponse(template.render( {'Productos': results}, request))      

def seguridad(request):
     template = loader.get_template("inventarioapp/Usuarios.html")

     results =tabla_usuarios.obtener_todos_los_usuarios()
     return HttpResponse(template.render( {'Productos': results}, request)) 

def nuevo_usuario(request):
    context = {"dummy": 'dummy'}
    return render(request, "inventarioapp/nuevo_usuario.html", context)


def crear_usuario(request):
     if request.method=="POST":
          u=Usuario(request.POST.get('nombre'),
                     request.POST.get('correo'),
                     request.POST.get('contraseña'),
                     request.POST.get('rol'))

          tabla_usuarios.agregar_usuario(u)
          messages.success(request, "se creo el nuevo proceso")
          template = loader.get_template("inventarioapp/Usuarios.html")
          results =tabla_usuarios.obtener_todos_los_usuarios()
          return HttpResponse(template.render( {'Productos': results}, request))          
     
def validar_login(request):
     correo=str(request.POST.get('username'))
     contraseña=str(request.POST.get('password'))
     user=tabla_usuarios.obtener_usuario(correo)
     if user is not None and user.verificar_contraseña(contraseña) :
          template = loader.get_template("inventarioapp/catalogo.html")

          results =inventario.obtener_productos()
          return HttpResponse(template.render( {'Productos': results}, request)) 
     else:
          messages.success(request, "El producto fue creado correctamente")
          template = loader.get_template("inventarioapp/login.html")
          return HttpResponse(template.render( {'Periodos': ''}, request))  
     
def proveedor(request):
     template = loader.get_template("inventarioapp/proveedor.html")
     results =lista_proveedores.mostrar_proveedores()
     return HttpResponse(template.render( {'Productos': results}, request))    

def nuevo_proveedor(request):
    context = {"dummy": 'dummy'}
    return render(request, "inventarioapp/nuevo_proveedor.html", context)


def crear_proveedor(request):
     if request.method=="POST":
          lista_proveedores.agregar_proveedor(int(request.POST.get('id')),
                     request.POST.get('nombre'),
                     request.POST.get('direccion'),
                     request.POST.get('telefono'),
                     request.POST.get('correo'))
          
     template = loader.get_template("inventarioapp/proveedor.html")
     results =lista_proveedores.mostrar_proveedores()
     return HttpResponse(template.render( {'Productos': results}, request))       

def ordenes(request):
     template = loader.get_template("inventarioapp/ordenes.html")
     results = obtener_ordenes_en_diccionario()
     return HttpResponse(template.render( {'Productos': results}, request))    

def nueva_orden(request):
    context = {"dummy": 'dummy'}
    return render(request, "inventarioapp/nueva_orden.html", context)

def crear_orden(request):
     if request.method=="POST":
          agregar_orden(request.POST.get('Codigo producto'),
                     request.POST.get('Codigo proveedor'),
                     request.POST.get('Cantidad'))
          
     template = loader.get_template("inventarioapp/ordenes.html")
     results = obtener_ordenes_en_diccionario()
     return HttpResponse(template.render( {'Productos': results}, request))   