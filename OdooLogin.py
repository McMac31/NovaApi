import xmlrpc.client #Uso de import para conectar a odoo
import ssl #Importacion para ignorar el ssl
from datetime import datetime

#Campos de enlace usuario, base de datos, contraseña
url = "https://odootechsolutions.duckdns.org"
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
    
    #Metodo para logearse en la base de datos
    def login(self):
        if not self.uid: #Controlamos que haya login
            self.uid=self.common.authenticate(self.db,self.username,self.password, {})
        return self.uid #Devolvemos el inicio de sesion
    
    #Metodo para obtener lista de clientes
    def get_clientes(self):
        uid= self.login()
        filtroCliente=[('customer_rank', '>', 0)] #Filtra para que busque solo clientes
        return self.models.execute_kw(self.db,self.uid,self.password, #Se le pasan las llaves de acceso para proceder a realizar los metodos
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
        [nuevo_cliente] #Le paso los datos del cliente a añadir
        )
    
    #Metodo para actualizar valor
    def actualizar_cliente(self,id, valores: dict):
        uid= self.login()
        filtroCliente=[('id', '=', id), ('customer_rank', '>', 0)] #Filtro para que solo modifique clientes y que coincida con el id pasado
        clientes = self.models.execute_kw(
        self.db, uid, self.password,
        'res.partner', 'search', #Buscamos primero si el cliente existe
        [filtroCliente] #Le pasamos el filtro 
        )
        if not clientes: #Control sobre si el cliente existe o no
            return False
        return self.models.execute_kw(self.db, self.uid,self.password, 
                 'res.partner', 'write', #Si el cliente existe 
                 [[id], valores]) #Re escribimos sus datos basado en el ID que se ha pasado
    
    #Metodo para eliminar clientes por id
    def eliminar_cliente(self,id):
        uid= self.login()
        filtroCliente=[('id', '=', id), ('customer_rank', '>', 0)] #Filtro para que solo acepte clientes
        clientes = self.models.execute_kw(
        self.db, uid, self.password,
        'res.partner', 'search',
        [filtroCliente] #Verifica que si sea un cliente
        )
        if not clientes:  #Control sobre si el cliente existe o no
            return False
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner', #Si el cliente existe 
        'unlink', #Elimina el cliente mediante el ID pasado anteriormente
        [[id]]                             
        )
    

#Ver contactos
    def get_contactos(self):
        uid= self.login()
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner', #Busca dentro de contactos
        'search_read', #Metodo para buscar y leer contactos
        [[]],
        {'fields':['name', 'email']}) #Campos a buscar
    
       #Metodo para añadir contacto
    def add_contacto(self,nombre,email): #Coge datos de entrada para añadir un nuevo contacto
        uid= self.login()
        nuevo_contacto={ #Metemos los datos a ingresar 
            'name':f'{nombre}',
            'email':f'{email}'
        }
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'create', #Metodo para crear contacto
        [nuevo_contacto] #Crea el contacto en base a los datos pasados
        )
    
        #Metodo para actualizar contacto
    def actualizar_contacto(self,id, valores: dict):
        uid= self.login()
        filtroContacto=[('id', '=', id)] #Establecemos un filtro para que busque por ID
        contacto= self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'search_read', #Metodo para buscar el contacto
         [filtroContacto], #Por el id que le pasamos anteriormente
        {'fields':['name', 'email']}
        )
        if not contacto: #Si el contacto no exite devolvemos false
            return False
        return self.models.execute_kw(self.db, self.uid,self.password, #Si existe 
                 'res.partner', 'write', #Ejecutamos la accion de escribir los datos nuevos al cliente
                 [[id], valores]) #Mediante id
    
    #Metodo para eliminar contacto por id
    def eliminar_contacto(self,id):
        uid= self.login()
        filtroContacto=[('id', '=', id)] #Establecemos un filtro para que busque por ID
        contacto= self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'search_read',#Metodo para buscar el contacto
         [filtroContacto], #Por el id que le pasamos anteriormente
        {'fields':['name', 'email']}
        )
        if not contacto: #Si el contacto no exite devolvemos false
            return False
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner',
        'unlink', #Ejecutamos el metodo de eliminar el contacto 
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
        fechaFin=f"{year}-{mes:02d}-31" #Le indico y formateo desde que fecha quiero finalizar
        filtroVentas=[('date_order', '>=', fechaInicio), ('date_order', '<=', fechaFin),('state','in',['sale','done'])] #Filtro las fechas de pedidos y ventra completada
        camposVenta=['id','name', 'partner_id', 'date_order', 'amount_total', 'state'] #Filtro para indicar que campos vamos a mostrar
        ventas=self.models.execute_kw(
            self.db,self.uid,self.password,
            'sale.order','search_read',
            [filtroVentas],
            {'fields': camposVenta}
        )
        return len(ventas) #Devolvemos el numero de ventas existentes

	
    #Metodo para ver las ventas del mes
    def get_detalleVenta(self,mes,year): #Filtro por fecha y año de ventas del mes
        uid=self.login()
        hoy=datetime.now()
        if not mes: #Controlo por si no se ingresa ninguna fecha ni año
            mes=hoy.month
        if not year:
            year=hoy.year
        fechaInicio=f"{year}-{mes:02d}-01"#Le indico y formateo desde que fecha quiero iniciar
        fechaFin=f"{year}-{mes:02d}-31" #Le indico y formateo desde que fecha quiero finalizar
        filtroVentas=[('date_order', '>=', fechaInicio), ('date_order', '<=', fechaFin),('state','in',['sale','done'])] #Filtro las fechas de pedidos y ven>
        camposVenta=['id','name', 'partner_id', 'date_order', 'amount_total', 'state'] #Filtro para indicar que campos vamos a mostrar
        ventas=self.models.execute_kw(
            self.db,self.uid,self.password,
            'sale.order','search_read',
            [filtroVentas],
            {'fields': camposVenta}
        )
        return ventas #Devolvemos las ventas existentes

    
    #Metodod para ver el total facutado 
    def get_totalFacturado(self):
        uid=self.login()
        campoVenta=['amount_total','state'] #Indicamos que campos estamos buscando
        filtroFacturado = [('invoice_status', '=', 'invoiced')] #Buscamos por el estado que este facturado
        facturado= self.models.execute_kw(
            self.db,self.uid,self.password,
            'sale.order','search_read',
            [filtroFacturado],
            {'fields': campoVenta}
        )
        total=sum(f['amount_total']for f in facturado) #Sumamos los datos de cada cliente que cumplan la condicion del filtro
        return total #Devolvemos la suma resultante

    #Metodo para ver pedidos en estado pendiente de envio
    def get_pedidosPendientes(self):
        uid = self.login()
        pedidos = self.models.execute_kw( 
            self.db, uid, self.password,
            'sale.order', 'search_read',
            [[('state', '=', 'sale')]], #Busco por estado los pedidos que estan en venta 
            {'fields': ['id', 'name', 'partner_id', 'date_order', 'amount_total', 'picking_ids']}) #Pongo los campos a mostrar
        pendientes = [] #Inicializo lista para guardar los envios pendientes de envios, ya que no se puede hacer filtrado directo
        for p in pedidos: #Voy pedido por pedido
            entregas = self.models.execute_kw(
                self.db, uid, self.password,
                'stock.picking', 'read',
                [p.get('picking_ids', [])], #Voy recogiendo id de recogida
                {'fields': ['state']})  #Busco por cada uno el estado
            if any(ent['state'] != 'done' for ent in entregas): #Selecciono las que sean diferentes a hecho
                pendientes.append(p)  # agregamos el pedido pendiente a la lista
        return {'Num pedidos': len(pendientes), 'Pedidos Pendientes': pendientes} #Enseñamos la informacion

    #Metoto para ver productos que tienen poco stock disponible
    def get_prodStockBajo(self):
        uid = self.login()
        campos = ['id','name','qty_available'] #Le indicamos que campos estamos buscando mostrar
        return self.models.execute_kw(
        self.db, uid, self.password,
        'product.product', 'search_read',
        [[('qty_available', '<=', 2)]], #Indicamos la condicion para considerar un producto con stock Bajo
        {'fields': campos}) #Devolvemos los valores y campos que cumplan la condicion
    
        #Metodo para obtener lista de clientes
    def get_clientesDestacados(self):
        uid= self.login()
        etiqueta="destacad" #Para que solo busque el patron destacad controlando si se añade destacados o similar
        filtroCliente=[('customer_rank', '>', 0),('category_id.name','ilike',etiqueta)] #Filtra para que busque solo clientes con la etiqueta destacado
        return self.models.execute_kw(self.db,self.uid,self.password,
        'res.partner', #Busca dentro de clientes
        'search_read', #Metodo para buscar y leer clientes
        [filtroCliente],
        {'fields':['name', 'email']}) #Campos a buscar
                
