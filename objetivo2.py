lista = ['192.2 1','192.2 40','192.2 8','193.2 70','193.2 11','193.2 5','10.2 8','10.2 5']
IndexMayor=0
cont=0
ma=0
for i in range(len(lista)):
    if i !=len(lista)-1:
      MacActual=lista[i].split(" ")
      MacAct=int(MacActual[1])
      MacSiguiente=lista[i+1].split(" ")
      MacSig=int(MacSiguiente[1])
      if MacActual[0]==MacSiguiente[0]:
        if cont==0:
          IndexMayor=i
        m=lista[IndexMayor].split()
        ma=int(m[1])
        if ma<MacSig:
          IndexMayor=i+1
        cont=1+cont
      if MacActual[0]!=MacSiguiente[0]:
        cont=0
        lista[IndexMayor]=lista[IndexMayor]+" *"
    if i ==  len(lista)-1:
      lista[IndexMayor]=lista[IndexMayor]+" *"
for x in lista:
  print(x)

