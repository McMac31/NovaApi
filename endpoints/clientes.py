from flask import Blueprint, jsonify,request
from OdooLogin import conexionOdoo


clientesPlano= Blueprint('clientes', __name__)
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

