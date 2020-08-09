from collections import defaultdict
from pysnmp.hlapi import *
from pysnmp import debug
lista=[] 
listaFinal=[]
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
ListaInThroughput=[]
ListaInThrou2=[]
ListaMacAddress=[]
def listADD(lista,listado):
    for x in lista:  # guardar listado temporal en lista correspondiente
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
# ip interface OSPF
get_item(IPOrigen,lista,'1.3.6.1.2.1.14.7.1.1',comunidad) 
listADD(lista,ListaVisitado)
lista=[]

# ip interfaces y gateway
get_item(IPOrigen,lista,'1.3.6.1.2.1.4.22.1.3',comunidad)  
for x in lista:   # guardar las ip que faltan por visitar para explorar 
    temp=x.split(" ")
    temp=temp[1]
    if not temp in ListaVisitado:
       ListaExplorar.append(temp)
       #print(temp)
lista=[]

# ip tabla enrutamiento 
get_item(IPOrigen,lista,'1.3.6.1.2.1.4.24.4.1.1',comunidad) 
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

#1.3.6.1.2.1.2.2.1.10 inifoctect
lista=[]
get_item(IPOrigen,lista,'1.3.6.1.2.1.2.2.1.10',comunidad)
listADD(lista,ListaInThrou)
lista=[]

get_item(IPOrigen,lista,'1.3.6.1.2.1.2.2.1.10',comunidad)
listADD(lista,ListaInThrou2)
for x in range(len(ListaInThrou2)):
      ListaInThroughput.append(str((int(ListaInThrou2[x])-int(ListaInThrou[x]))))   
#      print(ListaInThrou2[x]+" "+ListaInThrou[x]+" sum:"+str((int(ListaInThrou2[x])-int(ListaInThrou[x]))))
#1.3.6.1.2.1.2.2.1.6  mac addres 
lista=[]
get_item(IPOrigen,lista,'1.3.6.1.2.1.2.2.1.6',comunidad)
listADD(lista,ListaMacAddress)


for x in ListaVisitado: #recorer todas las ip que estan ospf en ese router
    if x in ListaIPRouter: # recorer todas las ip tabla enrutamiento
       index=(int(ListaIndexInterface[ListaIPRouter.index(x)])-1)
       listaFinal.append(ListadoRouteName[0][22:]+" "+ListaInterfaName[index]+" "+x+" bw:"+ListaBandWith[index]+" MTU:"+ListaMTU[index]+" ram:"+str(ram)+" throu:"+ListaInThroughput[index]+" MacAdd:"+ListaMacAddress[index])
       #print(ListadoRouteName[0][22:]+" "+ListaInterfaName[index]+" "+x+" bw:"+ListaBandWith[index]+" MTU:"+ListaMTU[index]+" ram:"+str(ram)+" throu:"+ListaInThroughput[index]+" MacAdd:"+ListaMacAddress[index])

#Lista ip repetida(balanceo de carga) 
aux = defaultdict(list)
for index, item in enumerate(ListaIPRouter):
    aux[item].append(index)
banl = {item: indexs for item, indexs in aux.items() if len(indexs) > 1}

print(banl)
for x in listaFinal:
      print(x)
