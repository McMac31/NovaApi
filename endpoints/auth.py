from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta
from OdooLogin import conexionOdoo

authPlano = Blueprint("auth", __name__)
SECRET_KEY = "clave_de_prueba_para_token" 
odoo = conexionOdoo()

@authPlano.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Usuario o contraseña faltante"}), 400
    try:
        # Intentar logear en Odoo
        uid = odoo.common.authenticate(odoo.db, username, password, {})
        if not uid:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
        # Crear token JWT
        payload = {
            "uid": uid,
            "username": username,
            "exp": datetime.now() + timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
