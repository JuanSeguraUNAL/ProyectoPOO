import sqlite3
from sqlite3 import Error
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def conexionBD():
    try:
        con=sqlite3.connect('BaseDatosCerveceria.db')
        #establezco el objeto de conexion y creo la BD fisica
        return con
    except Error:
        print(Error)

def cerrarBD(con):
    con.close()

def crearTablaProductos(con):
    cursorObj=con.cursor()
    #recorremos la BD con el objeto de Conexion
    cad='''CREATE TABLE IF NOT EXISTS productos(noIdProducto integer,
                                  nombreProducto text NOT NULL,
                                  medida text NOT NULL,
                                  fechaVencimiento date NOT NULL,
                                  precioProduccion integer NOT NULL,
                                  precioVenta integer NOT NULL,
                                  PRIMARY KEY(noIdProducto))'''
    #creamos la cadena con el sql a ejecutar
    cursorObj.execute(cad)
    #ejecutamos la cadena con el metodo execute
    con.commit()
    #aseguramos la persistencia con el commit

def crearTablaClientes(con):
    cursorObj=con.cursor()
    #recorremos la BD con el objeto de Conexion
    cad='''CREATE TABLE IF NOT EXISTS clientes(noIdCliente integer,
                                               nombreCliente text NOT NULL,
                                               apellidoCliente text NOT NULL,
                                               direccion text NOT NULL,
                                               telefono integer NOT NULL,
                                               correo text NOT NULL,
                                               PRIMARY KEY(noIdCliente))'''
    #creamos la cadena con el sql a ejecutar
    cursorObj.execute(cad)
    #ejecutamos la cadena con el metodo execute
    con.commit()
    #aseguramos la persistencia con el commit

def cambiarFrame(cerrarFrame, abrirFrame):
    cerrarFrame.pack_forget()
    abrirFrame.pack(fill="both", expand=True, padx=20, pady=20)

def crearNuevoProducto(con, ventana, frame):
    # Recorremos la BD con el objeto de Conexion
    cursorObj = con.cursor()

    frame.pack_forget()
    crearProductoFrame = tk.Frame(ventana)
    crearProductoFrame.pack()

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

    def guardar():
        try:
            noIdProducto = entradaID.get()
            nombreProducto = entradaNombre.get().ljust(20)
            medida = entradaMedida.get()
            fV = entradaFV.get()
            precioProduccion = entradaPP.get()
            precioVenta = entradaPV.get()
        except:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

        try:
            noIdProducto = int(noIdProducto)
        except ValueError:
            messagebox.showerror("Error", "El codigo del producto debe ser un numero entero.")
            return

        try:
            fechaVencimiento = datetime.strptime(fV, '%d/%m/%Y').date().strftime('%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use dd/mm/yyyy")
            return

        try:
            precioProduccion = float(precioProduccion)
            precioVenta = float(precioVenta)
        except ValueError:
            messagebox.showerror("Error", "Los precios deben ser numeros")
            return

        try:
            # Creamos la cadena con el sql a ejecutar
            cad = f"INSERT INTO productos VALUES ({noIdProducto}, '{nombreProducto}','{medida}','{fechaVencimiento}',{precioProduccion},{precioVenta})"
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

def crearNuevoCliente(con, ventana, frame):
    # Recorremos la BD con el objeto de Conexion
    cursorObj = con.cursor()

    frame.pack_forget()
    crearClienteFrame = tk.Frame(ventana)
    crearClienteFrame.pack()

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

    def guardar():
        try:
            noIdCliente = entradaID.get()
            nombreCliente = entradaNombre.get().ljust(30)
            apellidoCliente = entradaApellido.get().ljust(30)
            direccion = entradaDireccion.get()
            telefono = entradaTelefono.get()
            correo = entradaCorreo.get()
        except:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

        try:
            noIdCliente = int(noIdCliente)
        except ValueError:
            messagebox.showerror("Error", "El numero de identificacion del cliente debe ser un numero entero.")

        try:
            telefono = int(telefono)
        except ValueError:
            messagebox.showerror("Error", "El telefono del cliente debe ser un numero entero.")

        try:
            # Creamos la cadena con el sql a ejecutar
            cad = f"INSERT INTO clientes VALUES ({noIdCliente}, '{nombreCliente}', '{apellidoCliente}', '{direccion}', {telefono}, '{correo}')"
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

def actualizarProducto(con, ventana, frame):
    # Recorremos la BD con el objeto de Conexion
    cursorObj = con.cursor()

    frame.pack_forget()
    actualizarProductoFrame = tk.Frame(ventana)
    actualizarProductoFrame.pack()

    tk.Label(actualizarProductoFrame, text='Actualizar nombre del producto', font=('Arial', 18, 'bold')).pack(pady=10)
    tk.Label(actualizarProductoFrame, text='Rellene los siguientes campos:', font=('Arial', 12)).pack(pady=10)

    tk.Label(actualizarProductoFrame, text='Codigo del producto:', font=('Arial', 12)).pack(pady=10)
    entradaID = tk.Entry(actualizarProductoFrame)
    entradaID.pack()
    tk.Label(actualizarProductoFrame, text='Nombre del producto:', font=('Arial', 12)).pack(pady=10)
    entradaNombre = tk.Entry(actualizarProductoFrame)
    entradaNombre.pack()

    def guardar():
        try:
            noIdProducto = entradaID.get()
            nombreProducto = entradaNombre.get().ljust(20)
        except:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

        try:
            noIdProducto = int(noIdProducto)
        except ValueError:
            messagebox.showerror("Error", "El codigo del producto debe ser un numero entero.")

        try:
            # Creamos la cadena con el sql a ejecutar
            cad = f"UPDATE productos SET nombreProducto='{nombreProducto}' WHERE noIdProducto={noIdProducto}"
            # Ejecutamos la cadena con el metodo execute
            cursorObj.execute(cad)
            # Aseguramos la persistencia con el commit
            con.commit()
            messagebox.showinfo("Exito", "Nombre del producto actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
            return

    tk.Button(actualizarProductoFrame, text="Actualizar Producto", font=("Arial", 12, "bold"),
              command=guardar).pack(pady=10)
    tk.Button(actualizarProductoFrame, text="Volver al menu de productos", font=("Arial", 12, "bold"),
              command=lambda: cambiarFrame(actualizarProductoFrame, frame)).pack(pady=10)
def actualizarCliente(con, ventana, frame):
    # Recorremos la BD con el objeto de Conexion
    cursorObj = con.cursor()

    frame.pack_forget()
    actualizarClienteFrame = tk.Frame(ventana)
    actualizarClienteFrame.pack()

    tk.Label(actualizarClienteFrame, text='Actualizar direccion del cliente', font=('Arial', 18, 'bold')).pack(pady=10)
    tk.Label(actualizarClienteFrame, text='Rellene los siguientes campos:', font=('Arial', 12)).pack(pady=10)

    tk.Label(actualizarClienteFrame, text='Número de identificación del Cliente:', font=('Arial', 12)).pack(pady=10)
    entradaID = tk.Entry(actualizarClienteFrame)
    entradaID.pack()
    tk.Label(actualizarClienteFrame, text='Direccion del Cliente:', font=('Arial', 12)).pack(pady=10)
    entradaDireccion = tk.Entry(actualizarClienteFrame)
    entradaDireccion.pack()

    def guardar():
        try:
            noIdCliente = entradaID.get()
            direccion = entradaDireccion.get()
        except:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

        try:
            noIdCliente = int(noIdCliente)
        except ValueError:
            messagebox.showerror("Error", "El numero de identificacion del cliente debe ser un numero entero.")

        try:
            # Creamos la cadena con el sql a ejecutar
            cad = f"UPDATE clientes SET direccion='{direccion}' WHERE noIdCliente={noIdCliente}"
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

def consultarProducto(con, ventana, frame):
    # Recorremos la BD con el objeto de Conexion
    cursorObj = con.cursor()

    frame.pack_forget()
    consultarProductoFrame = tk.Frame(ventana)
    consultarProductoFrame.pack()

    tk.Label(consultarProductoFrame, text='Codigo del producto:', font=('Arial', 12)).pack(pady=10)
    entradaID = tk.Entry(consultarProductoFrame)
    entradaID.pack()

    def consultar():
        try:
            noIdProducto = entradaID.get()
        except:
            messagebox.showerror("Error", "Ingrese el codigo del producto.")
            return

        try:
            noIdProducto = int(noIdProducto)
        except ValueError:
            messagebox.showerror("Error", "El codigo del producto debe ser un numero entero.")

        try:
            cursorObj = con.cursor()
            # recorremos la BD con el objeto de Conexion
            cad = f'SELECT * FROM productos WHERE noIdProducto= {noIdProducto}'
            # creamos la cadena con el sql a ejecutar
            cursorObj.execute(cad)
            # ejecutamos la cadena con el metodo execute
            filas = cursorObj.fetchall()
            for row in filas:
                codigo = row[0]
                nombre = row[1]
                medida = row[2]
                fechaVn = row[3]
                precioP = row[4]
                precioV = row[5]
                tk.Label(consultarProductoFrame, text=f'El nombre del producto es: {nombre} que corresponde al codigo: {codigo}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarProductoFrame, text=f'La medida del producto es: {medida}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarProductoFrame, text=f'La fecha de vencimiento del producto es: {fechaVn}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarProductoFrame, text=f'El precio de Producción es: {precioP}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarProductoFrame, text=f'El precio de Venta es: {precioV}', font=('Arial', 12)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
            return

    tk.Button(consultarProductoFrame, text="Consultar producto", font=("Arial", 12, "bold"),
              command=consultar).pack(pady=10)
    tk.Button(consultarProductoFrame, text="Volver al menu de productos", font=("Arial", 12, "bold"),
              command=lambda: cambiarFrame(consultarProductoFrame, frame)).pack(pady=10)

def consultarCliente(con, ventana, frame):
    # Recorremos la BD con el objeto de Conexion
    cursorObj = con.cursor()

    frame.pack_forget()
    consultarClienteFrame = tk.Frame(ventana)
    consultarClienteFrame.pack()

    tk.Label(consultarClienteFrame, text='Número de identificación del Cliente:', font=('Arial', 12)).pack(pady=10)
    entradaID = tk.Entry(consultarClienteFrame)
    entradaID.pack()

    def consultar():
        try:
            noIdCliente = entradaID.get()
        except:
            messagebox.showerror("Error", "Ingrese el numero de identificacion del cliente.")
            return

        try:
            noIdCliente = int(noIdCliente)
        except ValueError:
            messagebox.showerror("Error", "El numero de identificacion del cliente debe ser un numero entero.")

        try:
            cursorObj = con.cursor()
            # recorremos la BD con el objeto de Conexion
            cad = f'SELECT * FROM clientes WHERE noIdCliente= {noIdCliente}'
            # creamos la cadena con el sql a ejecutar
            cursorObj.execute(cad)
            # ejecutamos la cadena con el metodo execute
            filas = cursorObj.fetchall()
            for row in filas:
                codigo = row[0]
                nombre = row[1]
                apellido = row[2]
                direccion = row[3]
                telefono = row[4]
                correo = row[5]
                tk.Label(consultarClienteFrame, text=f'El nombre completo del cliente es: {nombre} {apellido} que corresponde al numero de identificacion: {codigo}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarClienteFrame, text=f'La dirección del cliente es: {direccion}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarClienteFrame, text=f'El teléfono del cliente es: {telefono}', font=('Arial', 12)).pack(pady=10)
                tk.Label(consultarClienteFrame, text=f'El correo del cliente es: {correo}', font=('Arial', 12)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar en la base de datos. \n{e}")
            return

    tk.Button(consultarClienteFrame, text="Consultar cliente", font=("Arial", 12, "bold"),
              command=consultar).pack(pady=10)
    tk.Button(consultarClienteFrame, text="Volver al menu de clientes", font=("Arial", 12, "bold"),
              command=lambda: cambiarFrame(consultarClienteFrame, frame)).pack(pady=10)
def menu(con):
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

    def menuProductos():
        menuFrame.pack_forget()
        productosFrame = tk.Frame(ventana)

        titulo = tk.Label(productosFrame, text='MENU PRODUCTOS', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        boton1 = tk.Button(productosFrame, text="Crear un producto nuevo", font=("Arial", 12), width=30,
                           command= lambda: crearNuevoProducto(con, ventana, productosFrame)).pack(pady=5)
        boton2 = tk.Button(productosFrame, text="Actualizar el nombre de un producto", font=("Arial", 12), width=30,
                           command= lambda: actualizarProducto(con, ventana, productosFrame)).pack(pady=5)
        boton3 = tk.Button(productosFrame, text="Consultar un producto", font=("Arial", 12), width=30,
                           command= lambda: consultarProducto(con, ventana, productosFrame)).pack(pady=5)
        boton4 = tk.Button(productosFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                           command= lambda: volverMenu(productosFrame)).pack(pady=5)

        productosFrame.pack(fill="both", expand=True, padx=20, pady=20)

    def menuClientes():
        menuFrame.pack_forget()
        clientesFrame = tk.Frame(ventana)

        titulo = tk.Label(clientesFrame, text='MENU CLIENTES', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        boton1 = tk.Button(clientesFrame, text="Crear un nuevo cliente", font=("Arial", 12), width=30,
                           command=lambda: crearNuevoCliente(con, ventana, clientesFrame)).pack(pady=5)
        boton2 = tk.Button(clientesFrame, text="Actualizar la direccion de un cliente", font=("Arial", 12), width=30,
                           command=lambda: actualizarCliente(con, ventana, clientesFrame)).pack(pady=5)
        boton3 = tk.Button(clientesFrame, text="Consultar un cliente", font=("Arial", 12), width=30,
                           command=lambda: consultarCliente(con, ventana, clientesFrame)).pack(pady=5)
        boton4 = tk.Button(clientesFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                           command=lambda: volverMenu(clientesFrame)).pack(pady=5)

        clientesFrame.pack(fill="both", expand=True, padx=20, pady=20)

    def menuVentas():
        menuFrame.pack_forget()
        ventasFrame = tk.Frame(ventana)
        ventasFrame.pack()

        titulo = tk.Label(ventasFrame, text='MENU DE VENTAS', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        boton = tk.Button(ventasFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                           command=lambda: volverMenu(ventasFrame)).pack(pady=5)

    def menuFactura():
        menuFrame.pack_forget()
        facturaFrame = tk.Frame(ventana)
        facturaFrame.pack()

        titulo = tk.Label(facturaFrame, text='IMPRESION DE FACTURA', font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        boton = tk.Button(facturaFrame, text="Retornar al menu principal", font=("Arial", 12), width=30,
                          command=lambda: volverMenu(facturaFrame)).pack(pady=5)


    boton1 = tk.Button(menuFrame, text="Menú de gestion de productos", font=("Arial", 12), width=30,
                       command= menuProductos).pack(pady=5)
    boton2 = tk.Button(menuFrame, text="Menú de gestion de clientes", font=("Arial", 12), width=30,
                       command= menuClientes).pack(pady=5)
    boton3 = tk.Button(menuFrame, text="Venta de Productos", font=("Arial", 12), width=30,
                       command= menuVentas).pack(pady=5)
    boton4 = tk.Button(menuFrame, text="Impresion de Facturas", font=("Arial", 12), width=30,
                       command= menuFactura).pack(pady=5)
    boton5 = tk.Button(menuFrame, text="Salir del Programa", font=("Arial", 12), width=30,
                       command= ventana.quit).pack(pady=5)

    ventana.mainloop()

def main():
    miCon = conexionBD()
    crearTablaProductos(miCon)
    crearTablaClientes(miCon)
    menu(miCon)
    cerrarBD(miCon)

main()