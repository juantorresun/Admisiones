from django.db import models
import hashlib
from datetime import datetime
import pytz

class Producto():
    def __init__(self, codigo, nombre, categoria,marca,stock,min_stock):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.marca = marca
        self.stock = stock
        self.min_stock = min_stock
        self.izquierda = None
        self.derecha = None

class Inventario:
    def __init__(self):
        self.raiz = None

    def insertar(self, producto):
        self.raiz = self._insertar_recursivo(self.raiz, producto)

    def _insertar_recursivo(self, nodo, producto):
        if nodo is None:
            return Producto(producto.codigo, producto.nombre, producto.categoria,producto.marca,producto.stock,producto.min_stock)

        if producto.codigo < nodo.codigo:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, producto)
        elif producto.codigo > nodo.codigo:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, producto)
        #else:
            # Actualizar la cantidad si el producto ya existe
            #nodo.nombre = producto.nombre

        return nodo

    def buscar(self, codigo):
        return self._buscar_recursivo(self.raiz, codigo)

    def _buscar_recursivo(self, nodo, codigo):
        if nodo is None or nodo.codigo == codigo:
            return nodo
        if codigo < nodo.codigo:
            return self._buscar_recursivo(nodo.izquierda, codigo)
        return self._buscar_recursivo(nodo.derecha, codigo)
 
    
    def obtener_productos(self):
        productos = []
        self._obtener_productos_recursivo(self.raiz, productos)
        return productos

    def _obtener_productos_recursivo(self, nodo, lista_productos):
        if nodo is not None:
            # Recorrer el subárbol izquierdo
            self._obtener_productos_recursivo(nodo.izquierda, lista_productos)
            
            # Agregar el producto actual a la lista
            lista_productos.append({
                "codigo": nodo.codigo,
                "nombre": nodo.nombre,
                "categoria": nodo.categoria,
                "marca": nodo.marca,
                "stock": nodo.stock,
                "min_stock": nodo.min_stock
            })

            # Recorrer el subárbol derecho
            self._obtener_productos_recursivo(nodo.derecha, lista_productos)
    def actualizar_stock(self, codigo, cantidad):
        producto = self.buscar(codigo)
        producto.stock += cantidad


import hashlib

class Usuario:
    def __init__(self):
        self.nombre = ""
        self.correo = ""
        self.contraseña = ""
        self.rol = ""
    def __init__(self, nombre, correo, contraseña, rol):
        self.nombre = nombre
        self.correo = correo
        self.contraseña = self._encriptar_contraseña(contraseña)
        self.rol = rol

    def _encriptar_contraseña(self, contraseña):
        # Utilizamos hashlib para encriptar la contraseña (puedes mejorar esto según tus necesidades)
        return hashlib.sha256(contraseña.encode()).hexdigest()

    def obtener_informacion_completa(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "contraseña": self.contraseña,
            "rol": self.rol
        }
    def verificar_contraseña(self, contraseña_ingresada):
        # Verificar si el hash de la contraseña ingresada coincide con el hash almacenado
        return self._encriptar_contraseña(contraseña_ingresada) == self.contraseña


class TablaHashUsuarios:
    def __init__(self, tamaño_tabla=10):
        self.tamaño_tabla = tamaño_tabla
        self.tabla = [None] * tamaño_tabla

    def _hash(self, clave):
        # Simple función hash para demostración
        return hash(clave) % self.tamaño_tabla

    def agregar_usuario(self, usuario):
        indice = self._hash(usuario.correo)
        if self.tabla[indice] is None:
            self.tabla[indice] = [usuario]
        else:
            for u in self.tabla[indice]:
                if u.correo == usuario.correo:
                    # El usuario ya existe, puedes manejar esto según tus necesidades
                    print(f"¡Error! El usuario con correo {usuario.correo} ya existe.")
                    return
            self.tabla[indice].append(usuario)

    def obtener_usuario(self, correo):
        indice = self._hash(correo)
        if self.tabla[indice] is not None:
            for usuario in self.tabla[indice]:
                if usuario.correo == correo:
                    return usuario
        # El usuario no fue encontrado
        print(f"No se encontró el usuario con correo {correo}.")
        return None

    def obtener_todos_los_usuarios(self):
        todos_los_usuarios = []
        for lista_usuarios in self.tabla:
            if lista_usuarios is not None:
                todos_los_usuarios.extend(lista_usuarios)
        return todos_los_usuarios

class Proveedor:
    def __init__(self, id, nombre, direccion,telefono,email):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.siguiente = None

class ListaProveedores:
    def __init__(self):
        self.cabeza = None

    def agregar_proveedor(self, id, nombre, direccion,telefono,email):
        nuevo_proveedor = Proveedor(id, nombre, direccion,telefono,email)
        nuevo_proveedor.siguiente = self.cabeza
        self.cabeza = nuevo_proveedor

    def mostrar_proveedores(self):
        proveedores = []
        actual = self.cabeza
        while actual:
            proveedor_info = {
                'id': actual.id,
                'nombre': actual.nombre,               
                'direccion': actual.direccion,
                'telefono': actual.telefono,
                'email': actual.email
            }
            proveedores.append(proveedor_info)
            actual = actual.siguiente
        return proveedores
    def buscar_proveedor_por_codigo(self, id):
        actual = self.cabeza
        while actual:
            if actual.id == id:
                return actual  # Devuelve el objeto Proveedor si se encuentra
            actual = actual.siguiente
        return None  # Retorna None si no se encuentra el proveedor con el código dado


class OrdenCompra:
    def __init__(self, producto, proveedor, cantidad):
        self.producto = producto
        self.proveedor = proveedor
        self.cantidad = cantidad
        self.fecha_hora = datetime.now(pytz.timezone('America/Bogota'))
    def actualizar_fecha_hora(self):
        self.fecha_hora = datetime.now(pytz.timezone('America/Bogota'))

class PilaOrdenes:
    def __init__(self):
        self.ordenes = []

    def agregar_orden(self, orden):
        orden.actualizar_fecha_hora()
        self.ordenes.append(orden)

    def obtener_ordenes_como_diccionario(self,inventario,lista_proveedores):
        lista_ordenes = []
        for orden in self.ordenes:
            orden_dict = {
                'Producto': orden.producto,
                "nombre_producto":(inventario.buscar(int(orden.producto))).nombre,
                'Proveedor': orden.proveedor,
                'nombre_proveedor': lista_proveedores.buscar_proveedor_por_codigo(int(orden.proveedor)).nombre,
                'Cantidad': orden.cantidad,
                'fecha_hora': orden.fecha_hora.strftime('%Y-%m-%d %H:%M:%S %Z')
            }
            lista_ordenes.append(orden_dict)
        lista_revertida = lista_ordenes[::-1]
        return lista_revertida


class ventas:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.fecha_hora = datetime.now(pytz.timezone('America/Bogota'))


class Pilaventas:
    def __init__(self):
        self.ventas = []

    def agregar_compra(self, ventas):
        self.ventas.append(ventas)

    def obtener_ventas_como_diccionario(self,inventario):
        lista_ventas = []
        for orden in self.ventas:
            orden_dict = {
                'Producto': orden.producto,
                "nombre_producto":(inventario.buscar(int(orden.producto))).nombre,
                "categoria":(inventario.buscar(int(orden.producto))).categoria,
                "marca":(inventario.buscar(int(orden.producto))).marca,
                'Cantidad': orden.cantidad,
                'fecha_hora': orden.fecha_hora.strftime('%Y-%m-%d %H:%M:%S %Z')
            }
            lista_ventas.append(orden_dict)
        lista_revertida = lista_ventas[::-1]
        return lista_revertida

