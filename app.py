from flask import Flask
from endpoints.clientes import clientesPlano

app=Flask(__name__)
app.register_blueprint(clientesPlano,url_prefix="/api") #Con ek porefix le defino que para acceder a los planos se debe poner primero /api y luego su respectiva ruta
                                                        #en este casp seria /clientes

@app.route("/") #Verifico que la primera conexion este hecha correctamente
def index():
    return{"message":"API CONECTADA CORRECTAMENTE"}, 200

if __name__=="__main__":
    app.run(debug=True,port=5000)