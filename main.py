import json
import copy
from time import time
from functools import reduce

restaurantes={7:{'estadia':1.5,'apertura1':11,'apertura2':25,'cierre1':19,'cierre2':24},
            8:{'estadia':1.5,'apertura1':11,'apertura2':25,'cierre1':23,'cierre2':24},
}

distancias=[
    
    [0.000000,0.678333,0.360278,1.000556,0.603611,0.568167,0.459722,0.093889,0.158056],
    [0.694167,0.000000,1.022222,1.535000,0.074444,0.876833,0.312500,0.651111,0.795833],
    [0.396111,1.015000,0.000000,1.331111,0.940556,0.857500,0.796389,0.430278,0.484167],
    [1.907500,2.127222,2.251111,0.000000,2.052778,0.328333,1.908611,1.886389,2.009167],
    [0.619722,0.074444,0.947500,1.460556,0.000000,0.858000,0.238056,0.576389,0.721389],
    [0.568167,0.876833,0.857500,0.328333,0.858000,0.000000,0.732333,0.566667,0.549833],
    [0.474444,0.305833,0.802222,1.315278,0.231389,0.732333,0.000000,0.431111,0.575833],
    [0.067778,0.626667,0.411389,0.962500,0.551944,0.566667,0.408056,0.000000,0.170000],
    [0.131111,0.763333,0.465278,1.060556,0.688611,0.549833,0.544722,0.158889,0.000000]
]

atracciones={1:{'nombre':'POI1','beneficio':1,'costo':21000,'estadia':5,'apertura1':16,'apertura2':25,'cierre1':21,'cierre2':24,'obligatoria':0    ,'restaurant':0},
             2:{'nombre':'Poi2','beneficio':2,'costo':48000,'estadia':4,'apertura1':16.5,'apertura2':25,'cierre1':20.5,'cierre2':24,'obligatoria':1,'restaurant':0},
             3:{'nombre':'Poi3','beneficio':3,'costo':65000,'estadia':3,'apertura1':8,'apertura2':25,'cierre1':14,'cierre2':24,'obligatoria':1     ,'restaurant':0},
             4:{'nombre':'Poi4','beneficio':4,'costo':19000,'estadia':2,'apertura1':16,'apertura2':25,'cierre1':21,'cierre2':24,'obligatoria':1    ,'restaurant':0},
             5:{'nombre':'Poi5','beneficio':5,'costo':250000,'estadia':48,'apertura1':8,'apertura2':25,'cierre1':18,'cierre2':24,'obligatoria':0   ,'restaurant':0},
             6:{'nombre':'Poi6','beneficio':6,'costo':19000,'estadia':5,'apertura1':16,'apertura2':25,'cierre1':21,'cierre2':24,'obligatoria':0    ,'restaurant':0},
             7:{'nombre':'restaurant1','beneficio':0,'costo':0, 'estadia':1.5,'apertura1':13,'apertura2':0,'cierre1':15,'cierre2':0,'obligatoria':1,'restaurant':1},
             8:{'nombre':'restaurant2','beneficio':0,'costo':0, 'estadia':1.5,'apertura1':13,'apertura2':0,'cierre1':15,'cierre2':0,'obligatoria':1,'restaurant':1}
             

}
atracciones_total=copy.copy(atracciones)
def beneficio_final(ruta):
    beneficio=0
    for i in ruta[1:]:
        beneficio+=atracciones_total[i]['beneficio']
    return beneficio
def remover_restaurant(atracciones):
    atraccion2=copy.copy(atracciones)
    if(isinstance(atracciones,dict)):
        for i in atraccion2:
            if(atracciones_total[i]['restaurant']==1):           
                del atracciones[i]
    else:
        for i in atraccion2:
            if(atracciones_total[i]['restaurant']==1):
                atracciones.remove(i)


def beneficio_total(atracciones):
    total=0
    for i in atracciones:
        total+=atracciones[i]['beneficio']
    return total

def calcular_tiempo_necesario(atraccion1,atraccion2,tiempo_actual):

    tiempo_viaje=distancias[atraccion1][atraccion2]
    tiempo_espera=0
    apertura1=atracciones[atraccion2]['apertura1']
    cierre1=atracciones[atraccion2]['cierre1']
    cierre2=atracciones[atraccion2]['cierre2']
    apertura2=atracciones[atraccion2]['apertura2']
    if(atraccion1>0):
        estadia1=atracciones_total[atraccion1]['estadia']
    else:
        estadia1=0
    estadia2=atracciones[atraccion2]['estadia']
    tiempo_total=0   
    hora_llegada=tiempo_actual+tiempo_viaje+estadia1

    if(hora_llegada>cierre1):
        if(hora_llegada<apertura2):
            tiempo_espera=apertura2-hora_llegada
        elif(hora_llegada>cierre2):
            tiempo_total=9999999

    if(hora_llegada < apertura1):
        tiempo_espera=apertura1-hora_llegada
    
    # tiempo_total=tiempo_viaje+tiempo_espera	+estadia2+estadia1

    hora_final=hora_llegada+tiempo_espera
    

    return hora_final

def factible(atraccion):
    actual=atraccion
    presupuesto_disponible=presupuesto-atracciones[actual]['costo']
    obligatorias=copy.copy(atracciones)
    obligatorias=list(filter(lambda x: atracciones[x]['obligatoria'] == 1, obligatorias))
    # tiempo=tiempo_actual+distancias[ruta[-1]][actual]
    tiempo=calcular_tiempo_necesario(ruta[-1],actual,tiempo_actual)
    if(atraccion in obligatorias):
        obligatorias.remove(atraccion)

    for i in obligatorias:
        presupuesto_disponible-=atracciones[i]['costo']

    while(len(obligatorias)>0):
        
        mas_cercano=min(obligatorias,key=lambda x:calcular_tiempo_necesario(actual,x,tiempo))
        # tiempo+=distancias[actual][mas_cercano]
        tiempo= calcular_tiempo_necesario(actual,mas_cercano,tiempo)
        actual=mas_cercano
        obligatorias.remove(mas_cercano)
        if(atracciones_total[mas_cercano]['restaurant']==1):
            remover_restaurant(obligatorias)
    if(presupuesto_disponible < 0 or tiempo > tiempo_maximo):
        return -1
    else:
         return 1

def evaluar_atraccion(atraccion):
    beneficio=atracciones[atraccion]['beneficio']
    estadia=int(atracciones[atraccion]['estadia'])
    costo=int(atracciones[atraccion]['costo'])
    tiempo_viaje=distancias[ruta[-1]][atraccion]
    tiempo_espera=0
    apertura1=atracciones[atraccion]['apertura1']
    cierre1=atracciones[atraccion]['cierre1']
    cierre2=atracciones[atraccion]['cierre2']
    apertura2=atracciones[atraccion]['apertura2']
    tiempo_total=0
    puntaje=0
    if(tiempo_actual+tiempo_viaje>cierre1):
        if(tiempo_actual+tiempo_viaje<apertura2):
            tiempo_espera=apertura2-tiempo_actual-tiempo_viaje
        elif(tiempo_actual+tiempo_viaje>cierre2):
            puntaje=-9999
        
    if(tiempo_actual+tiempo_viaje < apertura1):
        tiempo_espera=apertura1-tiempo_actual-tiempo_viaje


    
    tiempo_total=tiempo_viaje+tiempo_espera+estadia
     

    if(tiempo_actual+tiempo_viaje>tiempo_maximo):
        puntaje=-9999

    if(costo>presupuesto):
        puntaje= -9999
    if(factible(atraccion)== -1):
        puntaje = -99999
    else:
        if(atracciones[atraccion]['obligatoria']==1):
            puntaje=(1/tiempo_total)
        else:
            puntaje=beneficio*(tiempo_maximo/tiempo_total)+beneficio*(presupuesto/costo)
            puntaje=(beneficio/beneficio_total)+(1-(tiempo_total/tiempo_maximo))+(1-(costo/presupuesto))


    return puntaje,tiempo_total


def escoger_atraccion(atracciones):
    eleccion=0
    maximo=-999999
    for atraccion in atracciones:
        fitness=evaluar_atraccion(atraccion)[0]
        if(fitness>maximo):
            eleccion=atraccion
            maximo=fitness
    if(atracciones[eleccion]['obligatoria']==0):
        obligatorias=copy.copy(atracciones)
        obligatorias=list(filter(lambda x: atracciones[x]['obligatoria'] == 1, obligatorias))
        obligatorias.append(eleccion)        
        nueva_eleccion=min(obligatorias,key=lambda x:calcular_tiempo_necesario(ruta[-1],x,tiempo_actual))
        if(factible(nueva_eleccion)):
            eleccion=nueva_eleccion
        
    return eleccion


        

if __name__ == "__main__":

    ruta=[0]
    tiempo_disponible=0
    presupuesto=0
    tiempo_actual=0
    tiempo_inicio=0
    tiempo_maximo=30
    presupuesto=232000
    beneficio_total=beneficio_total(atracciones_total)
    

    while(tiempo_disponible>0 or len(atracciones)>=0):
        if(len(atracciones)==0):
            print("no quedan atracciones por visitar")
            break
        if(presupuesto<0):
            print("Ninguna atracción es posible de visitar con el tiempo o presupuesto disponible")
            break
        mejor_atraccion=escoger_atraccion(atracciones)
        puntaje_atraccion,tiempo_atraccion=evaluar_atraccion(mejor_atraccion)
    
        if(puntaje_atraccion<0 ):
            print("se supero el tiempo máximo de viaje")
            break
        else:
            tiempo_actual+=tiempo_atraccion
            # tiempo_disponible-=tiempo_atraccion #La comenté para no restarle a la busqueda de la mejor atracción
            presupuesto-=atracciones[mejor_atraccion]['costo']
            del atracciones[mejor_atraccion]
            if(atracciones_total[mejor_atraccion]['restaurant']==1):
                remover_restaurant(atracciones)            
            ruta.append(mejor_atraccion)
    
    
    if(ruta==[0]):
        print("No hay una ruta que permita visitar a todas las atracciones obligatorias en el tiempo máximo indicado")
    else:
        print("La ruta final es:",ruta)
        print("Su beneficio total es:",beneficio_final(ruta))
        print("hora inicio de la ruta:",tiempo_inicio)
        print("hora final de la ruta:",tiempo_actual)


