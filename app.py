from flask import Flask
from endpoints.clientes import clientesPlano

app=Flask(__name__)
app.register_blueprint(clientesPlano,url_prefix="/api")

@app.route("/")
def index():
    return{"message":"API CONECTADA CORRECTAMENTE"}, 200

if __name__=="__main__":
    app.run(debug=True,port=5000)