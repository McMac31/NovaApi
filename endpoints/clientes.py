from flask import Blueprint, jsonify,request
from OdooLogin import conexionOdoo


clientesPlano= Blueprint('clientes', __name__)
odoo=conexionOdoo()

#Metodos HTTP

#Metodo GET para ver clientes 
@clientesPlano.route("/clientes",methods=["GET"])
def listadoCliente():
    try:

        Clientes=odoo.get_clientes()
        return jsonify({"data":Clientes, "count":len(Clientes)})
    except Exception as e:
        print("[ERROR] listadoCliente:", e)
        return  jsonify({"Error listando clientes": str(e)}), 500
    
#
@clientesPlano.route("/clientes", methods=["POST"] )
def crear_cliente():
    data=request.get_json()
    nombre=data.get("name")
    email=data.get("email")
    if not nombre or not email: 
       return jsonify({"error": "Falta name o email"}), 400
    try:
        nuevo_id=odoo.add_cliente(nombre,email)
        return jsonify({"message":"Nuevo cliente creado con exito","id":nuevo_id}),201
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@clientesPlano.route("/clientes/<int:id>", methods=["DELETE"])
def eliminarCliente(id):
    try:
        eliminado=odoo.eliminar_cliente(id)
        if eliminado:
            return jsonify({"message":f"Cliente con id : {id} Eliminado correctamente"}),200
        else:
            return jsonify({"error": "No eliminado"}),400
    except Exception as e:
        return jsonify({"error": str(e)}),500


@clientesPlano.route("/clientes/<int:id>", methods=["PUT"])
def editarCliente(id):
    data=request.get_json
    valores={}
    if "name" in data:
        valores["name"]=data["name"]
    if "email" in data:
        valores["email"]=data["email"]
    if not valores:
        return jsonify({"error": "Nada que actualizar"}), 400
    try:
        editado=odoo.actualizar_cliente(id,valores)
        if editado:
            return jsonify({"message":f"Cliente {id} actualizado"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}),500


