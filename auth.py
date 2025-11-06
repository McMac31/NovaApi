# auth.py
import os
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError,DecodeError
from datetime import datetime, timedelta, timezone
from OdooLogin import conexionOdoo

authPlano = Blueprint("auth", __name__)
odoo = conexionOdoo()

SECRET_KEY = os.environ.get("JWT_SECRET")
JWT_ALGO = "HS256"

@authPlano.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=False, silent=True)
        if not data:
            return jsonify({"error": "Body JSON inválido "}), 400
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"error": "Usuario o contraseña faltante"}), 400

        # debug temporal: tipos
        current_app.logger.debug(f"login request types: username={type(username)}, password={type(password)}")
        current_app.logger.debug(f"SECRET type: {type(SECRET_KEY)}")

        # validar tipos
        if not isinstance(username, str) or not isinstance(password, str):
            return jsonify({"error": "username y password deben ser strings"}), 400

        # Intentar login en Odoo
        uid = odoo.common.authenticate(odoo.db, username, password, {})
        if not uid:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        # payload con UTC y exp correcto
        now = datetime.now(timezone.utc)
        payload = {
            "uid": int(uid),
            "username": username,
            "iat": int(now.timestamp()),                             # iat como entero UTC
            "exp": int((now + timedelta(hours=72)).timestamp())     # exp como entero UTC
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
            return jsonify({"token": token}), 200

        # Asegurar secret key válida
        if not SECRET_KEY or not isinstance(SECRET_KEY, str):
            current_app.logger.error("SECRET_KEY no configurada o no es string")
            return jsonify({"error": "Servidor: SECRET_KEY no configurada"}), 500

        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGO)
        # pyjwt a veces devuelve bytes
        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return jsonify({"token": token}), 200

    except Exception as e:
        current_app.logger.exception("Error en login")
        # devolver mensaje simple para cliente y log completo en servidor
        return jsonify({"error": "Error interno en login", "detail": str(e)}), 500


#Validar JWT
def _obtener_token_de_request():
    # Mira Authorization: Bearer <token>
    auth = request.headers.get("Authorization", "")
    if auth and auth.startswith("Bearer "):
        return auth.split(" ", 1)[1].strip()
    # control 
    return request.headers.get("X-API-Token") or request.args.get("token")


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGO])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "token_expired"}
    except jwt.InvalidTokenError:
        return {"error": "token_invalid"}


def require_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        current_app.logger.debug(f"Authorization header: {auth!r}")
        if not auth:
            return jsonify({"error":"Token no proporcionado"}), 401
        parts = auth.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"error":"Authorization header mal formado. Debe ser: Bearer <token>"}), 401
        token = parts[1].strip()
        current_app.logger.debug(f"Token recibido (len={len(token)}): {token[:50]}...")

        # Verificar token y manejar errores específicos
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_app.logger.debug(f"Payload decodificado: {payload}")
        except ExpiredSignatureError:
            return jsonify({"error":"Token expirado"}), 401
        except InvalidSignatureError:
            return jsonify({"error":"Firma inválida (SECRET_KEY no coincide)"}), 401
        except DecodeError as e:
            current_app.logger.exception("DecodeError")
            return jsonify({"error":"Token inválido (no se pudo decodificar)", "detail": str(e)}), 401
        except Exception as e:
            current_app.logger.exception("Error verificando token")
            return jsonify({"error":"Error verificando token", "detail": str(e)}), 500
        return f(*args, **kwargs)
    return wrapper
