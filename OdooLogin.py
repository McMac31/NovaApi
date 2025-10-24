import xmlrpc.client #Uso de import para conectar a odoo
import ssl #Importacion para ignorar el ssl

#Campos de enlace usuario, base de datos, contraseña
url = "https://odootechsolutions.duckdns.org/"
db = "techsolutions_db"
username = "ikyemendez24@lhusurbil.eus" 
password = "password"

context = ssl._create_unverified_context() #Ignora el ssl

class conexionOdoo: #Clase de conexion
    def __init__(self):
        self.db=db
        self.username=username
        self.password=password
        self.uid=None
        self.common= xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", context=context, allow_none=True) #Estableciendo conexion
        self.models=xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", context=context,allow_none=True) #Verifican conexion con clientes y objetos 

    def login(self):
        if not self.uid: #Controlamos que haya login
            self.uid=self.common.authenticate(self.db,self.username,self.password, {})
        return self.uid #Devolvemos el inicio de sesion
    
    #Metodo para obtener lista de clientes
    def get_clientes(self):
        uid= self.login()
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner', #Busca dentro de clientes
        'search_read', #Metodo para buscar y leer clientes
        [[]],
        {'fields':['name', 'email']}) #Campos a buscar
    
    #Metodo para añadir cliente
    def add_cliente(self,nombre,email): #Coge datos de entrada para añadir un nuevo cliente
        uid= self.login()
        nuevo_cliente={ #Metemos los datos a ingresar 
            'name':f'{nombre}',
            'email':f'{email}'
        }
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'create', #Metodo para crear cliente
        [nuevo_cliente]
        )
    
    #Metodo para actualizar valor
    def actualizar_cliente(self,id, valores: dict):
        uid= self.login()
        return self.models.execute_kw(self.db, self.uid,self.password,
                 'res.partner', 'write',
                 [[id], valores])
    
    #Metodo para eliminar clientes por id
    def eliminar_cliente(self,id):
        uid= self.login()
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'unlink',
        [[id]]                             
        )
        

        
    

    