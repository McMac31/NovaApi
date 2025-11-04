from flask import Flask
from endpoints.clientes import clientesPlano, ventasPlano, contactosPlano
from auth import authPlano
from flask_cors import CORS

app=Flask(__name__)
CORS(app, resources={r"/api/*":{"origins": "*"}})
app.register_blueprint(clientesPlano,url_prefix="/api") #Con ek porefix le defino que para acceder a los planos se debe poner primero /api y luego su respectiva ruta
app.register_blueprint(ventasPlano,url_prefix="/api")   
app.register_blueprint(contactosPlano,url_prefix="/api") #en este casp seria /clientes
app.register_blueprint(authPlano, url_prefix="/api") #Blueprint para el token

@app.route("/") #Verifico que la primera conexion este hecha correctamente
def index():
    return{"message":"API CONECTADA CORRECTAMENTE"}, 200

if __name__=="__main__":
    app.run(debug=True,port=5000)
