import xmlrpc.client #Uso de import para conectar a odoo
import ssl #Importacion para ignorar el ssl
from datetime import datetime

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
        filtroCliente=[('customer_rank', '>', 0)] #Filtra para que busque solo clientes
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner', #Busca dentro de clientes
        'search_read', #Metodo para buscar y leer clientes
        [filtroCliente],
        {'fields':['name', 'email']}) #Campos a buscar
    
    #Metodo para añadir cliente
    def add_cliente(self,nombre,email): #Coge datos de entrada para añadir un nuevo cliente
        uid= self.login()
        nuevo_cliente={ #Metemos los datos a ingresar 
            'name':f'{nombre}',
            'email':f'{email}',
            'customer_rank': 1 #Defino que es un cliente
        }
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'create', #Metodo para crear cliente
        [nuevo_cliente]
        )
    
    #Metodo para actualizar valor
    def actualizar_cliente(self,id, valores: dict):
        uid= self.login()
        filtroCliente=[('id', '=', id), ('customer_rank', '>', 0)] #Filtro para que solo modifique clientes
        clientes = self.models.execute_kw(
        self.db, uid, self.password,
        'res.partner', 'search',
        [filtroCliente]
        )
        if not clientes:
            return False
        return self.models.execute_kw(self.db, self.uid,self.password,
                 'res.partner', 'write',
                 [[id], valores])
    
    #Metodo para eliminar clientes por id
    def eliminar_cliente(self,id):
        uid= self.login()
        filtroCliente=[('id', '=', id), ('customer_rank', '>', 0)] #Filtro para que solo acepte clientes
        clientes = self.models.execute_kw(
        self.db, uid, self.password,
        'res.partner', 'search',
        [filtroCliente] #Verifica que si sea un cliente
        )
        if not clientes:
            return False
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'unlink',
        [[id]]                             
        )
    
#CONTACTOS
#Ver contactos
    def get_contactos(self):
        uid= self.login()
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner', #Busca dentro de contactos
        'search_read', #Metodo para buscar y leer contactos
        [[]],
        {'fields':['name', 'email']}) #Campos a buscar
    
       #Metodo para añadir cliente
    def add_contacto(self,nombre,email): #Coge datos de entrada para añadir un nuevo contacto
        uid= self.login()
        nuevo_contacto={ #Metemos los datos a ingresar 
            'name':f'{nombre}',
            'email':f'{email}'
        }
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'create', #Metodo para crear cliente
        [nuevo_contacto]
        )
    
        #Metodo para actualizar contacto
    def actualizar_contacto(self,id, valores: dict):
        uid= self.login()
        return self.models.execute_kw(self.db, self.uid,self.password,
                 'res.partner', 'write',
                 [[id], valores])
    
    #Metodo para eliminar contacto por id
    def eliminar_contacto(self,id):
        uid= self.login()
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'unlink',
        [[id]]                             
        )
    
    #Metodo para ver las ventas del mes
    def get_NumventasMes(self,mes,year): #Filtro por fecha y año de ventas del mes
        uid=self.login()
        hoy=datetime.now() 
        if not mes: #Controlo por si no se ingresa ninguna fecha ni año 
            mes=hoy.month
        if not year:
            year=hoy.year
        fechaInicio=f"{year}-{mes:02d}-01"#Le indico y formateo desde que fecha quiero iniciar
        fechaFin=f"{year}-{mes:02d}-31"
        filtroVentas=[('date_order', '>=', fechaInicio), ('date_order', '<=', fechaFin)] #Filtro las fechas de pedidos
        camposVenta=['id','name', 'partner_id', 'date_order', 'amount_total', 'state']
        
        ventas=self.models.execute_kw(
            self.db,self.uid,self.password,
            'sale.order','search_read',
            [filtroVentas],
            {'fields': camposVenta}
        )
        return len(ventas)
    
    def get_totalFacturado(self):
        uid=self.login()
        campoVenta=['amount_total','state']
        filtroFacturado = [('invoice_status', '=', 'invoiced')]
        facturado= self.models.execute_kw(
            self.db,self.uid,self.password,
            'sale.order','search_read',
            [filtroFacturado],
            {'fields': campoVenta}
        )
        total=sum(f['amount_total']for f in facturado)
        return total

    
    def get_pedidosPendientes(self):
        uid=self.login()
        camposVenta=['id','name', 'partner_id', 'date_order', 'amount_total', 'state']
        filtroEstado=[('state','in',['sale','sale'])]
        pedidosPdnts= self.models.execute_kw(
            self.db, self.uid, self.password,
            'sale.order','search_read',
            [filtroEstado],
            {'fields': camposVenta}
        )
        return pedidosPdnts

    def get_prodStockBajo(self):
        uid = self.login()
        campos = ['id','name','qty_available']
        return self.models.execute_kw(
        self.db, uid, self.password,
        'product.product', 'search_read',
        [[('qty_available', '<=', 2)]],
        {'fields': campos})
                

    