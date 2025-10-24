from flask import Blueprint, jsonify,request
from OdooLogin import conexionOdoo


clientesPlano= Blueprint('clientes', __name__)
ventasPlano=Blueprint('ventas',__name__)
contactosPlano=Blueprint('contactos',__name__)
odoo=conexionOdoo()

#Metodos HTTP
#Metodo GET para ver clientes 
@clientesPlano.route("/clientes",methods=["GET"])
def listadoCliente():
    try:
        Clientes=odoo.get_clientes()  #Llamada a metodo creado en OdooLogin
        return jsonify({"data":Clientes, "count":len(Clientes)}) #Devuelvo los clientes con sus respectivos datos enseñando tambien cuantos hay
    except Exception as e:
        print("[ERROR] listadoCliente:", e)
        return  jsonify({"Error listando clientes": str(e)}), 500
    
#Metodo Post para añadir y subir un nuevo contacto a odoo
@clientesPlano.route("/clientes", methods=["POST"] )
def crear_cliente():
    data=request.get_json()
    nombre=data.get("name")
    email=data.get("email")
    if not nombre or not email: #Condicion si no se cambia uno de los datos
       return jsonify({"error": "No se ha introducido ningun dato"}), 400
    try:
        nuevo_id=odoo.add_cliente(nombre,email)
        return jsonify({"message":"Nuevo cliente creado con exito","id":nuevo_id}),201
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
#Metodo para borrar un cliente en base de su id el cual podemos ver en el get
@clientesPlano.route("/clientes/<int:id>", methods=["DELETE"])
def eliminarCliente(id):
    try:
        eliminado=odoo.eliminar_cliente(id) #Llamada a metodo creado en OdooLogin
        if eliminado: #Internamete el metodo de borrado devulve un booleano si se ha borrado un dato
            return jsonify({"message":f"Cliente con id : {id} Eliminado correctamente"}),200
        else:
            return jsonify({"error": "No eliminado"}),400
    except Exception as e:
        return jsonify({"error": str(e)}),500

#Metodo Put para cambiar un dato de un cliente ya creado en base de su id
@clientesPlano.route("/clientes/<int:id>", methods=["PUT"])
def editarCliente(id):
    try:
        data = request.get_json()  
        if not data: #Control de que se metan datos a actualizar en el json
            return jsonify({"error": "No se enviaron datos"}), 400

        actualizado = odoo.actualizar_cliente(id, data) #Llamada a metodo creado en OdooLogin
        if actualizado:
            return jsonify({"message": f"Cliente {id} actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el cliente"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@contactosPlano.route("/contactos", methods=["GET"])
def listaContactos():
    try:
        Contactos=odoo.get_contactos()  #Llamada a metodo creado en OdooLogin
        return jsonify({"contactos":Contactos, "Num Contactos":len(Contactos)})#Devuelvo los contactos con sus respectivos datos enseñando tambien cuantos hay
    except Exception as e:
        print("[ERROR] listadoContactos:", e)
        return  jsonify({"Error listando contactos": str(e)}), 500
    

@contactosPlano.route("/contactos", methods=["POST"])
def crear_contacto():
    data=request.get_json()
    nombre=data.get("name")
    email=data.get("email")
    if not nombre or not email:
        return jsonify({"error": "No se ha introducido ningun dato"}), 400
    try:
        nuevo_id=odoo.add_contacto(nombre,email)
        return jsonify({"message":"Nuevo contacto creado con exito","id":nuevo_id}),201
    except Exception as e:
        return jsonify({"error":str(e)}),500

@contactosPlano.route("/contactos/<int:id>", methods=["DELETE"])
def eliminarContacto(id):
    try:
        eliminado=odoo.eliminar_contacto(id) #Llamada a metodo creado en OdooLogin
        if eliminado: #Internamente el metodo de borrado devulve un booleano si se ha borrado un dato
            return jsonify({"message":f"Contacto con id : {id} Eliminado correctamente"}),200
        else:
            return jsonify({"error": "No eliminado"}),400
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@contactosPlano.route("/contactos/<int:id>", methods=["PUT"])
def editarContacto(id):
    try:
        data = request.get_json()  
        if not data: #Control de que se metan datos a actualizar en el json
            return jsonify({"error": "No se enviaron datos"}), 400
        actualizado = odoo.actualizar_contacto(id, data) #Llamada a metodo creado en OdooLogin
        if actualizado:
            return jsonify({"message": f"Cliente {id} actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el contacto"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@ventasPlano.route("/ventas",methods=["GET"])
def ventasMes():
    year=request.args.get("year")
    mes=request.args.get("month") #Busco y transformo a entero
    num_ventas=odoo.get_NumventasMes(mes,year)
    return jsonify({"num_ventas": num_ventas})

@ventasPlano.route("/ventas/total",methods=["GET"])
def totalFacturado():
    facturado=odoo.get_totalFacturado()
    return jsonify({"Total Facturado": facturado})
    

@ventasPlano.route("/ventas/pendientes",methods=["GET"])
def ventasPndts():
    ventasPendientes=odoo.get_pedidosPendientes()
    return jsonify({'Pedidos Pendientes':ventasPendientes})


@ventasPlano.route("/ventas/stockbajo",methods=["GET"])
def bajoStock():
    return jsonify(odoo.get_prodStockBajo())


