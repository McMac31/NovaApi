from flask import Blueprint, jsonify,request
from OdooLogin import conexionOdoo

#Se divide cada uno en blueprints para mejor organizacion
clientesPlano= Blueprint('clientes', __name__)
ventasPlano=Blueprint('ventas',__name__)
contactosPlano=Blueprint('contactos',__name__)
odoo=conexionOdoo()

#Metodos HTTP
#Metodo GET para ver clientes 
#CLIENTES
@clientesPlano.route("/clientes",methods=["GET"]) #Establecemos metodo y ruta
def listadoCliente():
    try: #Control de excepciones
        Clientes=odoo.get_clientes()  #Llamada a metodo creado en OdooLogin
        return jsonify({"Clientes":Clientes, "Num clientes":len(Clientes)}) #Devuelvo los clientes con sus respectivos datos enseñando tambien cuantos hay
    except Exception as e:#Devolvemos la excepcion
        print("[ERROR] listadoCliente:", e) 
        return  jsonify({"Error listando clientes": str(e)}), 500 #Devolvemos el error y su respectivo codigo
    
#Metodo Post para añadir y subir un nuevo contacto a odoo
@clientesPlano.route("/clientes", methods=["POST"] ) #Establecemos metodo y ruta
def crear_cliente():
    data=request.get_json() #Metodo para buscar claves y valores
    nombre=data.get("name") #Especificamos que clave buscamos
    email=data.get("email")
    if not nombre or not email: #Condicion si no se cambia uno de los datos
       return jsonify({"error": "No se ha introducido ningun dato"}), 400
    try: #Control de excepciones
        nuevo_id=odoo.add_cliente(nombre,email) #Llamamos el metodo creado anteriormente
        return jsonify({"message":"Nuevo cliente creado con exito","id":nuevo_id}),201 #Devolvemos mensaje de exito con su respectivo codigo e ID del cliente nuevo
    except Exception as e: #Devolvemos la excepcion y codigo
        return jsonify({"error":str(e)}),500
    
#Metodo para borrar un cliente en base de su id el cual podemos ver en el get
@clientesPlano.route("/clientes/<int:id>", methods=["DELETE"]) #Establecemos el metodo delete y la variable id que sera la que se eliminara
def eliminarCliente(id):
    try: #Control de excepciones
        eliminado=odoo.eliminar_cliente(id) #Llamada a metodo creado en OdooLogin
        if eliminado: #Internamete el metodo de borrado devulve un booleano si se ha borrado un dato
            return jsonify({"message":f"Cliente con id : {id} Eliminado correctamente"}),200 #Devolvemos mensaje de borrado con exito y el id que fue borrado
        else:
            return jsonify({"error": "No eliminado"}),400 #Si no se puede eliminar devolvemos el mensaje
    except Exception as e: #Devolvemos la excepcion
        return jsonify({"error": str(e)}),500

#Metodo Put para cambiar un dato de un cliente ya creado en base de su id
@clientesPlano.route("/clientes/<int:id>", methods=["PUT"]) #Establecemos metodo put para editar y la variable id para el que sera editado
def editarCliente(id):
    try: #Controlamos excepciones
        data = request.get_json()  
        if not data: #Control de que se metan datos a actualizar en el json
            return jsonify({"error": "No se enviaron datos"}), 400
        actualizado = odoo.actualizar_cliente(id, data) #Llamada a metodo creado en OdooLogin
        if actualizado: #Si se cumple el cambio devovlvemos mensaje de exito
            return jsonify({"Mensaje": f"Cliente {id} actualizado correctamente"}), 200 #Mensaje de exito
        else:
            return jsonify({"error": "No se pudo actualizar el cliente"}), 400 #Mensaje de error si falla el metodo
    except Exception as e:
        return jsonify({"error": str(e)}), 500 #Mensaje de error de la excepcion capturada

#Ver clientes destacados
@clientesPlano.route("/clientes/destacados",methods=["GET"])
def Destacados():
    try: #Control de excepciones 
        Destacados=odoo.get_clientesDestacados()  #Llamada a metodo creado en OdooLogin
        return jsonify({"Clientes destacados":Destacados, "Numero de clientes destacados":len(Destacados)}) #Devuelvo los clientes con sus respectivos datos enseñando tambien cuantos hay
    except Exception as e: #Capturamos excepcion
        print("[ERROR] listadoCliente:", e)
        return  jsonify({"Error listando clientes": str(e)}), 500

#CONTACTOS
#Ver lista de contactos
@contactosPlano.route("/contactos", methods=["GET"]) #Metodo para ver los contactos
def listaContactos():
    try: #Control de excepciones
        Contactos=odoo.get_contactos()  #Llamada a metodo creado en OdooLogin
        return jsonify({"contactos":Contactos, "Num Contactos":len(Contactos)})#Devuelvo los contactos con sus respectivos datos enseñando tambien cuantos hay
    except Exception as e: #Capturamos Excepcion
        print("[ERROR] listadoContactos:", e)
        return  jsonify({"Error listando contactos": str(e)}), 500
    
#Añadir contacto nuevo
@contactosPlano.route("/contactos", methods=["POST"]) #Metodo para crear contacto nuevo
def crear_contacto():
    data=request.get_json()
    nombre=data.get("name")
    email=data.get("email")
    if not nombre or not email: #Si no se ingresa ningnun dato devolvemos error
        return jsonify({"error": "No se ha introducido ningun dato"}), 400
    try: #Control de excepciones
        nuevo_id=odoo.add_contacto(nombre,email) #Llamamos metodo creado y le pasamos los parametros capturados
        return jsonify({"Mensaje":"Nuevo contacto creado con exito","id":nuevo_id}),201 #Mensaje de extio
    except Exception as e: #Capturamos excepcion
        return jsonify({"error":str(e)}),500 #Devolvemos mensaje de error

#Eliminar contacto 
@contactosPlano.route("/contactos/<int:id>", methods=["DELETE"]) #Le pasamos el metodo a utilizar en este caso DELETE y la variable
def eliminarContacto(id):
    try: #Control de excepciones
        eliminado=odoo.eliminar_contacto(id) #Llamada a metodo creado en OdooLogin
        if eliminado: #Internamente el metodo de borrado devulve un booleano si se ha borrado un dato
            return jsonify({"Mensaje":f"Contacto con id : {id} Eliminado correctamente"}),200 #Mensaje de exito
        else:
            return jsonify({"error": "No eliminado"}),400 #Mensaje de error
    except Exception as e: #Capturamos excepcion
        return jsonify({"error": str(e)}),500

#Editar contacto
@contactosPlano.route("/contactos/<int:id>", methods=["PUT"])
def editarContacto(id):
    try: #Control de excepcion
        data = request.get_json()  
        if not data: #Control de que se metan datos a actualizar en el json
            return jsonify({"error": "No se enviaron datos"}), 400
        actualizado = odoo.actualizar_contacto(id, data) #Llamada a metodo creado en OdooLogin
        if actualizado: #Si el metodo se ejecuta correctamente devolvemos mensaje de exito
            return jsonify({"message": f"Cliente {id} actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el contacto"}), 400 #Si no delvovemos mensaje de error
    except Exception as e: #Devolvemos excepcion
        return jsonify({"error": str(e)}),500

 #VENTAS 
#Ver num ventas por mes
@ventasPlano.route("/ventas",methods=["GET"]) #Aqui cambia el .route ya que como estamos usando Blueprints, cambiamos la ruta para tener mejor organizado la seccion de contactos y ventas
def ventasMes():
    year=request.args.get("year")
    mes=request.args.get("month") #Buscamos con el request los datos solicitados
    num_ventas=odoo.get_NumventasMes(mes,year) #Le pasamos los parametros a los metodos
    return jsonify({"num_ventas": num_ventas}) #Devolvemos el resultado del metodo

#Ver total de ventas
@ventasPlano.route("/ventas/total",methods=["GET"]) #Le indicamos la ruta en la que mostraremos el todoal
def totalFacturado():
    facturado=odoo.get_totalFacturado() #Metemos dentro de la variable el resultado del metodo
    return jsonify({"Total Facturado": facturado}) #Devolvemos el resultado
    
#Ver pendientes de envio
@ventasPlano.route("/ventas/pendientes",methods=["GET"])
def ventasPndts():
    ventasPendientes=odoo.get_pedidosPendientes() #Metemos dentro de la variable el resultado del metodo
    return jsonify(ventasPendientes) #Devolvemos el resultado

#Ver productos con stock bajo
@ventasPlano.route("/ventas/stockbajo",methods=["GET"])
def bajoStock():
    return jsonify(odoo.get_prodStockBajo()) #Devolvemos el resultado del stock bajo

@ventasPlano.route("/ventas/detalles", methods=["GET"])
def detalleVenta():
	year = request.args.get("year")
	mes = request.args.get("month")
	ventaDetalle = odoo.get_detalleVenta(mes,year)
	return jsonify({"ventas":ventaDetalle})

    
