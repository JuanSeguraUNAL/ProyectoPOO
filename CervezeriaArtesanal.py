import sqlite3
from sqlite3 import Error
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from email.message import EmailMessage
import smtplib
from validate_email_address import validate_email

# Funcion para establecer la conexion con la base de datos
def conexionBD():
    try:
        con=sqlite3.connect('BaseDatosCerveceria.db')
        #establezco el objeto de conexion y creo la BD fisica
        return con
    except Error:
        print(Error)

# Funcion para cerrar la base de datos
def cerrarBD(con):
    con.close()

# Clase EntidadBase (Clase padre de Productos y Clientes)
class EntidadBase:
    def __init__(self):
        # Asignar el atributo privado de ID
        self.__id = None

    # Setter para modificar el ID
    def set_id(self,codigo):
        self.__id = codigo

    # Getter para acceder al ID
    def get_id(self):
        return self.__id

    # Definir el metodo para consultar una entidad (Cliente o producto) dado su identificador unico (Se considera como parametro la tabla a consultar en la BD)
    def consultarEntidad(self,con, ventana, frame, nombretabla):
        # Recorremos la BD con el objeto de Conexion
        cursorObj = con.cursor()

        # Establecer el frame a mostrar
        frame.pack_forget()
        consultarFrame = tk.Frame(ventana)
        consultarFrame.pack()

        # Entrada al usuario para ingresar el codigo de identificador unico
        tk.Label(consultarFrame, text='Codigo:', font=('Arial', 12)).pack(pady=10)
        entradaID = tk.Entry(consultarFrame)
        entradaID.pack()

        # Funcion a ejecutar una vez presionado el boton, manejando los posibles errores
        def consultar():
            try:
                self.set_id(entradaID.get())
            except:
                messagebox.showerror("Error", "Ingrese el codigo.")
                return

            try:
                 self.set_id(int(self.get_id()))
            except ValueError:
                messagebox.showerror("Error", "El codigo debe ser un numero entero.")

            try:
                cursorObj = con.cursor()
                # recorremos la BD con el objeto de Conexion
                cad = f'SELECT * FROM '+nombretabla+f' WHERE Codigo = {self.get_id()}'
                # creamos la cadena con el sql a ejecutar
                cursorObj.execute(cad)
                column_names = [desc[0] for desc in cursorObj.description]
                # ejecutamos la cadena con el metodo execute
                filas = cursorObj.fetchall()
                for row in filas:
                    codigo = row[0]
                    parametro1 = row[1]
                    parametro2 = row[2]
                    parametro3 = row[3]
                    parametro4 = row[4]
                    parametro5 = row[5]
                    tk.Label(consultarFrame, text= column_names[0]+f': {codigo}', font=('Arial', 12)).pack(pady=10)
                    tk.Label(consultarFrame, text= column_names[1]+f': {parametro1}', font=('Arial', 12)).pack(pady=10)
                    tk.Label(consultarFrame, text= column_names[2]+f': {parametro2}', font=('Arial', 12)).pack(pady=10)
                    tk.Label(consultarFrame, text= column_names[3]+f': {parametro3}', font=('Arial', 12)).pack(pady=10)
                    tk.Label(consultarFrame, text= column_names[4]+f': {parametro4}', font=('Arial', 12)).pack(pady=10)
                    tk.Label(consultarFrame, text= column_names[5]+f': {parametro5}', font=('Arial', 12)).pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
                return

        tk.Button(consultarFrame, text="Consultar", font=("Arial", 12, "bold"),
                  command=consultar).pack(pady=10)
        tk.Button(consultarFrame, text="Volver al menu anterior", font=("Arial", 12, "bold"),
                  command=lambda: cambiarFrame(consultarFrame, frame)).pack(pady=10)

# Clase de ventas
class Ventas:
    # Metodo para solicitar el ID del cliente
    def solicitarIDCliente(self, entradaIDcliente,botonSolicitarID, cursorObj):
        id_cliente = entradaIDcliente.get()
        try:
            cursorObj.execute(f"SELECT * FROM clientes WHERE Codigo = {id_cliente}")
            cliente = cursorObj.fetchone()
            if cliente:
                entradaIDcliente.config(state='disabled')
                botonSolicitarID.config(state='disabled')
            else:
                id_cliente = None
            ID = int(id_cliente)
            messagebox.showinfo("Exito", f"Cliente con ID {ID} seleccionado.")
            entradaIDcliente.config(state='disabled')
            botonSolicitarID.config(state='disabled')
        except:
            messagebox.showerror("Error", "Numero de identificacion del cliente no encontrado.")
        return ID

    # Metodo para agregar un producto al carrito de mercado
    def agregarProducto(self,ID,entradaIDcliente,botonSolicitarID, entradaCodigoProducto, entradaCantidad, cursorObj, carrito, actualizarCarrito):
            if ID is None:
                messagebox.showerror("Error", "Primero ingrese el ID del cliente.")
                return

            codigo_producto = entradaCodigoProducto.get()
            cantidad = entradaCantidad.get()

            try:
                codigo_producto = int(codigo_producto)
                cantidad = int(cantidad)
            except ValueError:
                messagebox.showerror("Error", "El código del producto y la cantidad deben ser números enteros.")
                return

            cursorObj.execute(f"SELECT * FROM productos WHERE Codigo = {codigo_producto}")
            producto = list(cursorObj.fetchone())

            if producto:
                for compra in carrito:
                    if compra[0][0] == producto[0]:
                        compra[1] += cantidad
                if producto[0] not in [compra[0][0] for compra in carrito]:
                    carrito.append([producto, cantidad])

                actualizarCarrito()
            else:
                messagebox.showerror("Error", "Producto no encontrado.")

    # Metodo para eliminar un producto del carrito de mercado
    def quitarProducto(self,ID, entradaCodigoProducto, entradaCantidad, carrito, actualizarCarrito):
            if ID is None:
                messagebox.showerror("Error", "Primero ingrese el ID del cliente.")
                return

            codigo_producto = entradaCodigoProducto.get()
            cantidad = entradaCantidad.get()

            try:
                codigo_producto = int(codigo_producto)
            except ValueError:
                messagebox.showerror("Error", "El código del producto debe ser un número entero.")
                return

            try:
                cantidad = int(cantidad)
            except ValueError:
                messagebox.showerror("Error", "La cantidad del producto debe ser un número entero.")
                return

            for compra in carrito:
                if compra[0][0] == codigo_producto:
                    if compra[1] == cantidad or compra[1] < cantidad:
                        carrito.remove(compra)
                    else:
                        compra[1] -= cantidad

                    actualizarCarrito()
                    return

            messagebox.showerror("Error", "Producto no encontrado en el carrito.")

# Clase de Productos que hereda el atributo y metodo de la clase EntidadBase
class Productos(EntidadBase):
    # Atributos de la clase Productos
    def __init__(self):
        super().__init__()
        self.nombreProducto=None
        self.medida=None
        self.fechaVencimiento=None
        self.precioProduccion=None
        self.precioVenta=None

    # Metodo para crear table de productos en la base de datos
    def crearTablaProductos(self,con):
        cursorObj=con.cursor()
        #recorremos la BD con el objeto de Conexion
        cad='''CREATE TABLE IF NOT EXISTS productos(Codigo integer,
                                      Nombre_Producto text NOT NULL,
                                      Medida text NOT NULL,
                                      Fecha_de_vencimiento date NOT NULL,
                                      Precio_de_produccion integer NOT NULL,
                                      Precio_de_venta integer NOT NULL,
                                      PRIMARY KEY(Codigo))'''
        #creamos la cadena con el sql a ejecutar
        cursorObj.execute(cad)
        #ejecutamos la cadena con el metodo execute
        con.commit()
        #aseguramos la persistencia con el commit

    # Metodo para crear u nuevo producto
    def crearNuevoProducto(self,con, ventana, frame):
        # Recorremos la BD con el objeto de Conexion
        cursorObj = con.cursor()

        # Establecer el frame de la interfaz para crear nuevo producto
        frame.pack_forget()
        crearProductoFrame = tk.Frame(ventana)
        crearProductoFrame.pack()

        # Solicitud de entradas
        tk.Label(crearProductoFrame, text='Crear nuevo producto', font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(crearProductoFrame, text="Rellene los siguientes campos:", font=("Arial", 12)).pack(pady=10)

        tk.Label(crearProductoFrame, text="Codigo del producto:", font=("Arial", 12)).pack(pady=10)
        entradaID = tk.Entry(crearProductoFrame)
        entradaID.pack()
        tk.Label(crearProductoFrame, text="Nombre del producto:", font=("Arial", 12)).pack(pady=10)
        entradaNombre = tk.Entry(crearProductoFrame)
        entradaNombre.pack()
        tk.Label(crearProductoFrame, text="Cantidad o volumen:", font=("Arial", 12)).pack(pady=10)
        entradaMedida = tk.Entry(crearProductoFrame)
        entradaMedida.pack()
        tk.Label(crearProductoFrame, text="Fecha de vencimiento (dd/mm/yyyy):", font=("Arial", 12)).pack(pady=10)
        entradaFV = tk.Entry(crearProductoFrame)
        entradaFV.pack()
        tk.Label(crearProductoFrame, text="Precio de produccion:", font=("Arial", 12)).pack(pady=10)
        entradaPP = tk.Entry(crearProductoFrame)
        entradaPP.pack()
        tk.Label(crearProductoFrame, text="Precio de venta:", font=("Arial", 12)).pack(pady=10)
        entradaPV = tk.Entry(crearProductoFrame)
        entradaPV.pack()

        # Funcion a ejecutar una vez presionado el boton de "Guardar producto" con manejo de posibles errores de tipos de dato de entrada
        def guardar():
            try:
                self.set_id(entradaID.get())
                self.nombreProducto = entradaNombre.get().ljust(20)
                self.medida = entradaMedida.get()
                fV = entradaFV.get()
                self.precioProduccion = entradaPP.get()
                self.precioVenta = entradaPV.get()
            except:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                self.set_id(int(self.get_id()))
            except ValueError:
                messagebox.showerror("Error", "El codigo del producto debe ser un numero entero.")
                return

            try:
                self.fechaVencimiento = datetime.strptime(fV, '%d/%m/%Y').date().strftime('%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use dd/mm/yyyy")
                return

            try:
                self.precioProduccion = float(self.precioProduccion)
                self.precioVenta = float(self.precioVenta)
            except ValueError:
                messagebox.showerror("Error", "Los precios deben ser numeros")
                return

            try:
                # Creamos la cadena con el sql a ejecutar
                cad = f"INSERT INTO productos VALUES ({self.get_id()}, '{self.nombreProducto}','{self.medida}','{self.fechaVencimiento}',{self.precioProduccion},{self.precioVenta})"
                # Ejecutamos la cadena con el metodo execute
                cursorObj.execute(cad)
                # Aseguramos la persistencia con el commit
                con.commit()
                messagebox.showinfo("Exito", "Producto agregado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
                return

        tk.Button(crearProductoFrame, text="Guardar Producto", font=("Arial", 12, "bold"),
                  command=guardar).pack(pady=10)
        tk.Button(crearProductoFrame, text="Volver al menu de productos", font=("Arial", 12, "bold"),
                  command= lambda: cambiarFrame(crearProductoFrame, frame)).pack(pady=10)

    # Metodo para actualizar el nombre del producto
    def actualizarProductos(self, con, ventana, frame):
            # Recorremos la BD con el objeto de Conexion
            cursorObj = con.cursor()

            # Establecer el frame para la interfaz de Actualizar producto
            frame.pack_forget()
            actualizarProductoFrame = tk.Frame(ventana)
            actualizarProductoFrame.pack()

            # Solicitud de entradas (ID del producto y su nuevo nombre)
            tk.Label(actualizarProductoFrame, text='Actualizar nombre del producto', font=('Arial', 18, 'bold')).pack(pady=10)
            tk.Label(actualizarProductoFrame, text='Rellene los siguientes campos:', font=('Arial', 12)).pack(pady=10)

            tk.Label(actualizarProductoFrame, text='Codigo del producto:', font=('Arial', 12)).pack(pady=10)
            entradaID = tk.Entry(actualizarProductoFrame)
            entradaID.pack()
            tk.Label(actualizarProductoFrame, text='Nombre del producto:', font=('Arial', 12)).pack(pady=10)
            entradaNombre = tk.Entry(actualizarProductoFrame)
            entradaNombre.pack()

            # Funcion a ejecutar una vez presionado el boton de "Actualizar producto" con manejo de posibles errores
            def guardar():
                try:
                    self.set_id(entradaID.get())
                    self.nombreProducto = entradaNombre.get().ljust(20)
                except:
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return

                try:
                    self.set_id(int(self.get_id()))
                except ValueError:
                    messagebox.showerror("Error", "El código del producto debe ser un número entero.")
                    return

                try:
                    cad = f"UPDATE productos SET Nombre_Producto='{self.nombreProducto}' WHERE Codigo={self.get_id()}"
                    cursorObj.execute(cad)
                    con.commit()
                    messagebox.showinfo("Éxito", "Nombre del producto actualizado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar la base de datos. \n{e}")
                    return

            tk.Button(actualizarProductoFrame, text="Actualizar Producto", font=("Arial", 12, "bold"),
                      command=guardar).pack(pady=10)
            tk.Button(actualizarProductoFrame, text="Volver al menú de productos", font=("Arial", 12, "bold"),
                      command=lambda: cambiarFrame(actualizarProductoFrame, frame)).pack(pady=10)
            
# Clase de Clientes que herede el atributo y metodo de la clase EntidadBase
class Clientes(EntidadBase):
    # Atributos de la clase clientes
    def __init__(self):
        super().__init__()
        self.nombreCliente=None
        self.apellidoCliente=None 
        self.direccion=None 
        self.telefono=None 
        self.correo=None

    # Metodo para crear la tabla de clientes en la base de datos
    def crearTablaClientes(self,con):
        cursorObj=con.cursor()
        #recorremos la BD con el objeto de Conexion
        cad='''CREATE TABLE IF NOT EXISTS clientes(Codigo integer,
                                                   Nombre_cliente text NOT NULL,
                                                   Apellido_cliente text NOT NULL,
                                                   Direccion text NOT NULL,
                                                   Telefono integer NOT NULL,
                                                   Correo text NOT NULL,
                                                   PRIMARY KEY(Codigo))'''
        #creamos la cadena con el sql a ejecutar
        cursorObj.execute(cad)
        #ejecutamos la cadena con el metodo execute
        con.commit()
        #aseguramos la persistencia con el commit

    # Metodo para crear un nuevo cliente en la base de datos
    def crearNuevoCliente(self,con, ventana, frame):
        # Recorremos la BD con el objeto de Conexion
        cursorObj = con.cursor()

        # Establecer el frame para la interfaze para crear un nuevo cliente
        frame.pack_forget()
        crearClienteFrame = tk.Frame(ventana)
        crearClienteFrame.pack()

        # Solicitud de entradas para el nuevo cliente
        tk.Label(crearClienteFrame, text='Crear nuevo cliente', font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(crearClienteFrame, text="Rellene los siguientes campos:", font=("Arial", 12)).pack(pady=10)

        tk.Label(crearClienteFrame, text="Número de identificación del Cliente:", font=("Arial", 12)).pack(pady=10)
        entradaID = tk.Entry(crearClienteFrame)
        entradaID.pack()
        tk.Label(crearClienteFrame, text="Nombre del Cliente:", font=("Arial", 12)).pack(pady=10)
        entradaNombre = tk.Entry(crearClienteFrame)
        entradaNombre.pack()
        tk.Label(crearClienteFrame, text="Apellido del Cliente:", font=("Arial", 12)).pack(pady=10)
        entradaApellido = tk.Entry(crearClienteFrame)
        entradaApellido.pack()
        tk.Label(crearClienteFrame, text="Dirección del Cliente:", font=("Arial", 12)).pack(pady=10)
        entradaDireccion = tk.Entry(crearClienteFrame)
        entradaDireccion.pack()
        tk.Label(crearClienteFrame, text="Teléfono del Cliente:", font=("Arial", 12)).pack(pady=10)
        entradaTelefono = tk.Entry(crearClienteFrame)
        entradaTelefono.pack()
        tk.Label(crearClienteFrame, text="Correo Electrónico del Cliente:", font=("Arial", 12)).pack(pady=10)
        entradaCorreo = tk.Entry(crearClienteFrame)
        entradaCorreo.pack()

        # Funcion a ejecutar una vez presionado el boton "Crear nuevo cliente" con manejo de posibles errores en los tipos de dato de entrada ingresados
        def guardar():
            try:
                self.set_id(entradaID.get())
                self.nombreCliente = entradaNombre.get().ljust(30)
                self.apellidoCliente = entradaApellido.get().ljust(30)
                self.direccion = entradaDireccion.get()
                self.telefono = entradaTelefono.get()
                self.correo = entradaCorreo.get()
            except:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                self.set_id(int(self.get_id()))
            except ValueError:
                messagebox.showerror("Error", "El numero de identificacion del cliente debe ser un numero entero.")
                return

            try:
                self.telefono = int(self.telefono)
            except ValueError:
                messagebox.showerror("Error", "El telefono del cliente debe ser un numero entero.")

            if validate_email(self.correo):
                pass
            else:
                messagebox.showerror("Error", "El correo es invalido.")
                return


            try:
                # Creamos la cadena con el sql a ejecutar
                cad = f"INSERT INTO clientes VALUES ({self.get_id()}, '{self.nombreCliente}', '{self.apellidoCliente}', '{self.direccion}', {self.telefono}, '{self.correo}')"
                # Ejecutamos la cadena con el metodo execute
                cursorObj.execute(cad)
                # Aseguramos la persistencia con el commit
                con.commit()
                messagebox.showinfo("Exito", "Cliente agregado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
                return

        tk.Button(crearClienteFrame, text="Guardar Cliente", font=("Arial", 12, "bold"),
                  command=guardar).pack(pady=10)
        tk.Button(crearClienteFrame, text="Volver al menu de clientes", font=("Arial", 12, "bold"),
                  command=lambda: cambiarFrame(crearClienteFrame, frame)).pack(pady=10)

    # Metodo para actualizar la direccion de un cliente dado su ID
    def actualizarCliente(self,con, ventana, frame):
        # Recorremos la BD con el objeto de Conexion
        cursorObj = con.cursor()

        # Establecer el frame para la interfaz de actualizar cliente
        frame.pack_forget()
        actualizarClienteFrame = tk.Frame(ventana)
        actualizarClienteFrame.pack()

        # Solicitud de campos de entrada
        tk.Label(actualizarClienteFrame, text='Actualizar direccion del cliente', font=('Arial', 18, 'bold')).pack(pady=10)
        tk.Label(actualizarClienteFrame, text='Rellene los siguientes campos:', font=('Arial', 12)).pack(pady=10)

        tk.Label(actualizarClienteFrame, text='Número de identificación del Cliente:', font=('Arial', 12)).pack(pady=10)
        entradaID = tk.Entry(actualizarClienteFrame)
        entradaID.pack()
        tk.Label(actualizarClienteFrame, text='Direccion del Cliente:', font=('Arial', 12)).pack(pady=10)
        entradaDireccion = tk.Entry(actualizarClienteFrame)
        entradaDireccion.pack()

        # Funcion a ejecutar una vez presionado el boton de "Actualizar cliente" con manejo de posibles errores en las entradas ingresadas
        def guardar():
            try:
                self.set_id(entradaID.get())
                self.direccion = entradaDireccion.get()
            except:
                messagebox.showerror("Error", "Todos los campos son obligatorios")

            try:
                self.set_id(int(self.get_id()))
            except ValueError:
                messagebox.showerror("Error", "El numero de identificacion del cliente debe ser un numero entero.")

            try:
                # Creamos la cadena con el sql a ejecutar
                cad = f"UPDATE clientes SET direccion='{self.direccion}' WHERE Codigo={self.get_id()}"
                # Ejecutamos la cadena con el metodo execute
                cursorObj.execute(cad)
                # Aseguramos la persistencia con el commit
                con.commit()
                messagebox.showinfo("Exito", "Direccion del cliente actualizada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
                return

        tk.Button(actualizarClienteFrame, text="Actualizar Cliente", font=("Arial", 12, "bold"),
                  command=guardar).pack(pady=10)
        tk.Button(actualizarClienteFrame, text="Volver al menu de clientes", font=("Arial", 12, "bold"),
                  command=lambda: cambiarFrame(actualizarClienteFrame, frame)).pack(pady=10)
    
# Funcion para cambiar de frames para la interfaz
def cambiarFrame(cerrarFrame, abrirFrame):
    cerrarFrame.pack_forget()
    abrirFrame.pack(fill="both", expand=True, padx=20, pady=20)

# Funcion para crear la tabla de facturas
def crearTablaFacturas(con):
    cursorObj=con.cursor()
    #recorremos la BD con el objeto de Conexion
    cad='''CREATE TABLE IF NOT EXISTS facturas(noFactura integer,
                                               noIdCliente integer NOT NULL,
                                               pago integer NOT NULL,
                                               fecha date NOT NULL,
                                               PRIMARY KEY(noFactura))'''
    #creamos la cadena con el sql a ejecutar
    cursorObj.execute(cad)
    #ejecutamos la cadena con el metodo execute
    con.commit()
    #aseguramos la persistencia con el commit

# Funcion para establecer el frame del menu principal
def menu(con,objProductos,objClientes):
    # Crear y abrir ventana de la interfaz de usuario, ajustando logo como icono e imagen
    ventana = tk.Tk()
    ventana.title('Cervezeria Artesanal')
    ventana.geometry('600x600')
    ventana.iconbitmap('Logo.ico')

    menuFrame = tk.Frame(ventana)
    menuFrame.pack(fill="both", expand=True, padx=20, pady=20)

    imagen = tk.PhotoImage(file="Logo.png")
    imagen = imagen.subsample(3, 3)
    label = tk.Label(menuFrame, image=imagen)
    label.pack()

    titulo = tk.Label(menuFrame, text='MENU PRINCIPAL', font=("Arial", 18, "bold"))
    titulo.pack(pady=10)

    def volverMenu(frame):
        frame.pack_forget()
        menuFrame.pack(fill="both", expand=True, padx=20, pady=20)

    # Funcion para establecer el frame de la interfaz del menu de productos
    def menuProductos():
        menuFrame.pack_forget()
        productosFrame = tk.Frame(ventana)

        titulo = tk.Label(productosFrame, text='MENU PRODUCTOS', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        boton1 = tk.Button(productosFrame, text="Crear un producto nuevo", font=("Arial", 12), width=30,
                           command= lambda: objProductos.crearNuevoProducto(con, ventana, productosFrame)).pack(pady=5)
        boton2 = tk.Button(productosFrame, text="Actualizar el nombre de un producto", font=("Arial", 12), width=30,
                           command= lambda: objProductos.actualizarProductos(con, ventana, productosFrame)).pack(pady=5)
        boton3 = tk.Button(productosFrame, text="Consultar un producto", font=("Arial", 12), width=30,
                           command= lambda: objProductos.consultarEntidad(con, ventana, productosFrame, "productos")).pack(pady=5)
        boton4 = tk.Button(productosFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                           command= lambda: volverMenu(productosFrame)).pack(pady=5)

        productosFrame.pack(fill="both", expand=True, padx=20, pady=20)

    # Funcion para establecer el frame de la interfaz del menu de clientes
    def menuClientes():
        menuFrame.pack_forget()
        clientesFrame = tk.Frame(ventana)

        titulo = tk.Label(clientesFrame, text='MENU CLIENTES', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        boton1 = tk.Button(clientesFrame, text="Crear un nuevo cliente", font=("Arial", 12), width=30,
                           command=lambda: objClientes.crearNuevoCliente(con, ventana, clientesFrame)).pack(pady=5)
        boton2 = tk.Button(clientesFrame, text="Actualizar la direccion de un cliente", font=("Arial", 12), width=30,
                           command=lambda: objClientes.actualizarCliente(con, ventana, clientesFrame)).pack(pady=5)
        boton3 = tk.Button(clientesFrame, text="Consultar un cliente", font=("Arial", 12), width=30,
                           command=lambda: objClientes.consultarEntidad(con, ventana, clientesFrame, "clientes")).pack(pady=5)
        boton4 = tk.Button(clientesFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                           command=lambda: volverMenu(clientesFrame)).pack(pady=5)

        clientesFrame.pack(fill="both", expand=True, padx=20, pady=20)

    # # Funcion para establecer el frame de la interfaz del menu de ventas
    def menuVentas():
        menuFrame.pack_forget()
        ventasFrame = tk.Frame(ventana)
        ventasFrame.pack()
        cursorObj = con.cursor()

        titulo = tk.Label(ventasFrame, text='MENU DE VENTAS', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        # Crear la lista de carrito cuyos elementos seran tuplas con el codigo del producto y su cantidad
        carrito = []
        ID = None

        # Crear un objeto de la clase Ventas
        misVentas = Ventas()

        # Funcion auxiliar para cambiar el valor no local de la variable ID
        def cambiar(entradaIDcliente,botonSolicitarID, cursorObj):
            nonlocal ID
            ID = misVentas.solicitarIDCliente(entradaIDcliente,botonSolicitarID, cursorObj)

        # Solicitud de entradas
        tk.Label(ventasFrame, text="Ingrese el ID del cliente:", font=("Arial", 12)).pack(pady=10)
        entradaIDcliente = tk.Entry(ventasFrame)
        entradaIDcliente.pack()
        botonSolicitarID = tk.Button(ventasFrame, text="Confirmar ID", font=("Arial", 12), command= lambda :cambiar(entradaIDcliente,botonSolicitarID, cursorObj))
        botonSolicitarID.pack(pady=10)
        
        tk.Label(ventasFrame, text="Ingrese el código del producto:", font=("Arial", 12)).pack(pady=10)
        entradaCodigoProducto = tk.Entry(ventasFrame)
        entradaCodigoProducto.pack()

        tk.Label(ventasFrame, text="Ingrese la cantidad:", font=("Arial", 12)).pack(pady=10)
        entradaCantidad = tk.Entry(ventasFrame)
        entradaCantidad.pack()
        
        botonAgregar = tk.Button(ventasFrame, text="Agregar producto", font=("Arial", 12), command= lambda : misVentas.agregarProducto(ID,entradaIDcliente,botonSolicitarID, entradaCodigoProducto, entradaCantidad, cursorObj, carrito, actualizarCarrito))
        botonAgregar.pack(pady=10)

        botonQuitar = tk.Button(ventasFrame, text="Quitar producto", font=("Arial", 12), command= lambda : misVentas.quitarProducto(ID, entradaCodigoProducto, entradaCantidad, carrito, actualizarCarrito))
        botonQuitar.pack(pady=10)

        carritoFrame = tk.Frame(ventasFrame)
        carritoFrame.pack(pady=20)

        botonFactura = tk.Button(ventasFrame, text="Finalizar compra", font=("Arial", 12), width=30,
                                command=lambda: factura()).pack(pady=5)

        botonVolver = tk.Button(ventasFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                                command=lambda: volverMenu(ventasFrame)).pack(pady=5)

        # Funcion para actualizar las cantidades mostradas del carrito
        def actualizarCarrito():
            for widget in carritoFrame.winfo_children():
                widget.destroy()

            tk.Label(carritoFrame, text="Carrito de Compras", font=("Arial", 14, "bold")).pack(pady=10)

            for producto, cantidad in carrito:
                tk.Label(carritoFrame, text=f"{producto[1]} - Cantidad: {cantidad} - Precio: {producto[5]}",
                         font=("Arial", 12)).pack()

        # Funcion para el frame de la interfaz de la factura, mostrarla en pantalla y enviarla al correo indicado (de ser posible)
        def factura():
            if carrito == []:
                messagebox.showerror("Error", "El carrito se encuentra vacío.")
                return

            ventasFrame.pack_forget()
            facturaFrame = tk.Frame(ventana)
            facturaFrame.pack()

            titulo = tk.Label(facturaFrame, text='FACTURA', font=("Arial", 18, "bold"))
            titulo.pack(pady=10)

            # Obtener los datos del cliente
            cursorObj.execute(f"SELECT * FROM clientes WHERE Codigo = {ID}")

            cliente = cursorObj.fetchone()

            # Desempaquetar los datos del cliente
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre = cliente[1].strip()
            apellido = cliente[2].strip()
            direccion = cliente[3].strip()
            telefono = cliente[4]
            correo = cliente[5].strip()
            cedula = ID

            # Separar los productos (sus datos) de sus cantidades
            productos = [compra[0] for compra in carrito]
            cantidad = [compra[1] for compra in carrito]

            # Hallar el total a pagar por el cliente dado los productos de su carrito y sus cantidades
            total =sum(producto[5] * n for producto, n  in zip(productos,cantidad))

            # Obtener toda la columna de numero de factura de la tabla de facturas
            cursorObj.execute(f"SELECT noFactura FROM facturas")
            numFacturas = cursorObj.fetchall()

            # En caso de no haber facturas registradas, tomar el numero como 1. En otro caso, tomar el siguiente numero al ultimo numero de factura
            if numFacturas == []:
                noFactura = 1
            else:
                noFactura = numFacturas[-1][0] + 1

            # Definir el texto a mostrar para la factura
            factura_texto = """
            ============================================
                             FACTURA
            ============================================
            No. de factura: {:<5}
            Fecha: {}
            Cliente: {} {}
            Dirección: {}
            Teléfono: {}
            Cédula/RUC: {}

            {:<4} {:<20} {:<8} {:<12} {:<12}
            ------------------------------------------------------------""".format(
                noFactura, fecha, nombre, apellido, direccion, telefono, cedula,
                "No.", "Producto", "Cant.", "P. Unitario", "Total"
            )

            for i, producto in enumerate(productos):
                nombre_producto = producto[1][:20]  # Asegurar máximo 20 caracteres
                factura_texto += "\n            {:<4} {:<20} {:<8.2f} ${:<11.2f} ${:<11.2f}".format(
                    i, nombre_producto.strip(), cantidad[i], producto[5], producto[5] * cantidad[i]
                )

            factura_texto += """\n            ------------------------------------------------------------
            TOTAL: ${:.2f}
            ============================================
                    ¡Gracias por su compra!
            """.format(total)


            # Ajustar tamaño del cuadro de texto
            lineas = factura_texto.count("\n") + 2
            ancho_max = max(len(linea) for linea in factura_texto.split("\n"))

            # Crear el widget de texto sin bordes y bien alineado
            text_widget = tk.Text(facturaFrame, font=("Courier", 12), wrap="none",
                                  height=lineas, width=ancho_max,
                                  bd=0, highlightthickness=0, relief="flat")
            text_widget.pack(pady=10, padx=10)

            # Insertar y centrar la factura
            text_widget.insert("1.0", factura_texto)
            text_widget.config(state="disabled")

            cursorObj.execute(f"INSERT INTO facturas VALUES ({noFactura}, {ID},{total},'{fecha}')")
            # Aseguramos la persistencia con el commit
            con.commit()
            
            botonVolver = tk.Button(facturaFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                                    command=lambda: volverMenu(facturaFrame)).pack(pady=5)

            # Enviar al correo del cliente (En caso de ser posible)
            try:
                remitente = "cerveceriaartesanalsa1@gmail.com"

                email = EmailMessage()
                email["From"] = remitente
                email["To"] = correo
                email["Subject"] = "Factura de compra Cerveceria Artesanal S.A"
                email.set_content(factura_texto)

                smtp = smtplib.SMTP_SSL("smtp.gmail.com")
                smtp.login(remitente,'qqej ojhk kfyg gzxm')
                smtp.sendmail(remitente, correo, email.as_string())
                messagebox.showinfo("Factura", "La factura ha sido enviada correctamente")
                smtp.quit()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al enviar el correo.\n{e}")

    boton1 = tk.Button(menuFrame, text="Menú de gestion de productos", font=("Arial", 12), width=30,
                       command= menuProductos).pack(pady=5)
    boton2 = tk.Button(menuFrame, text="Menú de gestion de clientes", font=("Arial", 12), width=30,
                       command= menuClientes).pack(pady=5)
    boton3 = tk.Button(menuFrame, text="Venta de Productos", font=("Arial", 12), width=30,
                       command= menuVentas).pack(pady=5)
    boton4 = tk.Button(menuFrame, text="Salir del Programa", font=("Arial", 12), width=30,
                       command= ventana.destroy).pack(pady=5)

    ventana.mainloop()

def main():
    miCon = conexionBD()
    misProductos = Productos()
    misClientes = Clientes()
    misProductos.crearTablaProductos(miCon)
    misClientes.crearTablaClientes(miCon)
    crearTablaFacturas(miCon)
    menu(miCon,misProductos,misClientes)
    cerrarBD(miCon)

main()
