from pysnmp.hlapi import *
from pysnmp import debug
lista=[] 
comunidad='public'
IPOrigen='192.168.7.1'
ListaVisitado=[]
ListaExplorar=[]
ListaIPRouter=[]
ListaIndexInterface=[]
ListaInterfaName=[]
ListadoRouteName=[]
ListaBandWith=[]
ListaMTU=[]
ListaInThrou=[]
def listADD(lista,listado):
    for x in lista:  # guardar las ip vistidas en el router 
        temp=x.split(" ")
        temp=temp[1]
        listado.append(temp)
    
def get_item(ip,lista,oid,comunidad): # Funcion para obtener nombre Router
         g = nextCmd(
            SnmpEngine(),
            CommunityData(comunidad, mpModel=1),
            UdpTransportTarget((ip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False
         )
         while True:
               try:
                  errorIndication, errorStatus, errorIndex, varBinds = next(g);
                  if errorIndication:
                    print(errorIndication)
                  elif errorStatus:
                     print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and     varBinds[int(errorIndex) - 1][0] or '?'))
                  else:
                    for name, val in varBinds:
                      lista.append(str(name.prettyPrint())+" "+str(val.prettyPrint()))		
               except StopIteration:
                  break	
get_item(IPOrigen,lista,'1.3.6.1.2.1.14.7.1.1',comunidad) # ip interface OSPF
listADD(lista,ListaVisitado)
lista=[]
get_item(IPOrigen,lista,'1.3.6.1.2.1.4.22.1.3',comunidad) # ip interfaces y gateway 
for x in lista:   # guardar las ip que faltan por visitar para explorar 
    temp=x.split(" ")
    temp=temp[1]
    if not temp in ListaVisitado:
       ListaExplorar.append(temp)
       #print(temp)
lista=[]
get_item(IPOrigen,lista,'1.3.6.1.2.1.4.24.4.1.1',comunidad) # ip tabla enrutamiento 
listADD(lista,ListaIPRouter) # guardar las ip de la tabla de enrutamiento del router 
lista=[]
# obtener listado de las ip tabla entruamietno index de la interface
get_item(IPOrigen,lista,'1.3.6.1.2.1.4.24.4.1.5',comunidad) 
listADD(lista,ListaIndexInterface)
lista=[]
# obtener los nombre de las interfaces 
get_item(IPOrigen,lista,'1.3.6.1.2.1.31.1.1.1.1',comunidad) 
listADD(lista,ListaInterfaName)
lista=[]
# obtener nombre del router 
#1.3.6.1.2.1.1.5  nombre del router
get_item(IPOrigen,lista,'1.3.6.1.2.1.1.5',comunidad)
ListadoRouteName=lista
lista=[]
# obtener bandwith
#1.3.6.1.2.1.2.2.1.5
get_item(IPOrigen,lista,'1.3.6.1.2.1.2.2.1.5',comunidad)
listADD(lista,ListaBandWith)
lista=[]
# obtener MTU
# 1.3.6.1.2.1.2.2.1.4
get_item(IPOrigen,lista,'1.3.6.1.2.1.2.2.1.4',comunidad)
listADD(lista,ListaMTU)
lista=[]
# obtener memoria ram
get_item(IPOrigen,lista,'1.3.6.1.4.1.9.9.48.1.1.1.6',comunidad)
ma=lista[0].split(" ")
ma=ma[1]
ma2=lista[1].split(" ")
ma2=ma2[1]
ram=int(ma)+int(ma2)
print(ram)
#1.3.6.1.2.1.2.2.1.10
lista=[]
get_item(IPOrigen,lista,'1.3.6.1.2.1.2.2.1.10',comunidad)
listADD(lista,ListaInThrou)
print(ListaVisitado)

for x in ListaVisitado: #recorer todas las ip que estan ospf en ese router
    if x in ListaIPRouter: # recorer todas las ip tabla enrutamiento
       index=(int(ListaIndexInterface[ListaIPRouter.index(x)])-1)
       print(ListadoRouteName[0][22:]+" "+ListaInterfaName[index]+" "+x+" bw:"+ListaBandWith[index]+" MTU:"+ListaMTU[index]+" ram:"+str(ram)+" throu:"+ListaInThrou[index])

