from datetime import datetime, timedelta
import threading
import time
import random

contenedor = ['vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 
'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio', 'vacio']
permiso = threading.Semaphore(1)
posicion_productor = 0
posicion_consumidor = 0

def producir():
    i = 1
    limite = random.randint(1, 4)
    global posicion_productor
    if(posicion_productor == 20):
        posicion_productor = 0
    a = 0
    for elemento in contenedor:
        if(elemento == "vacio")and(a == posicion_productor):
            contenedor[posicion_productor] = "producto"
            print("El productor inserta el producto en el espacio: ", posicion_productor)
            time.sleep(2)
            posicion_productor = posicion_productor + 1 
            if(i == limite):
                print("Alcancé el límite de inserciones")
                time.sleep(2)
                break
            i = i+1
        a = a+1
    print("Salgo de la fase de producción")
    time.sleep(2)
    permiso.release()

def consumir():
    i = 1
    limite = random.randint(1, 4)
    global posicion_consumidor
    if(posicion_consumidor == 20):
        posicion_consumidor = 0
    a = 0
    for elemento in contenedor:
        if(elemento == "producto")and(a == posicion_consumidor):
            contenedor[posicion_consumidor] = "vacio"
            print("El consumidor adquiere el producto del espacio: ", posicion_consumidor)
            time.sleep(2)
            posicion_consumidor = posicion_consumidor + 1 
            if(i == limite):
                print("Alcancé el límite de veces en las que puedo consumir")
                time.sleep(2)
                break
            i = i+1
        a = a+1
    print("Salgo de la fase de consumo")
    time.sleep(2)
    permiso.release()

def funcionProductor():
    start = datetime.now()
    while datetime.now() - start < timedelta(seconds=random.randint(2, 5)):
        print("El productor intenta ingresar al contenedor...")
        time.sleep(2)
        if("vacio" in contenedor):
            permiso.acquire()
            producir()
        else:
            print("El productor no pudo acceder debido a que no hay espacio en el contenedor.")
            time.sleep(2)

    tiempo_descanso = random.randint(2, 5) 
    start_descanso = datetime.now()
    while datetime.now() - start_descanso < timedelta(seconds = tiempo_descanso):
        print("El productor está durmiendo...")
        time.sleep(2)

def funcionConsumidor():
    start = datetime.now()
    while datetime.now() - start < timedelta(seconds=random.randint(2, 5)):
        print("El consumidor intenta ingresar al contenedor...")
        time.sleep(2)
        if("producto" in contenedor):
            permiso.acquire()
            consumir()
        else:
            print("El consumidor no pudo acceder debido a que no hay productos disponibles.")
            time.sleep(2)
            
    tiempo_descanso = random.randint(2, 5) 
    start_descanso = datetime.now()
    while datetime.now() - start_descanso < timedelta(seconds = tiempo_descanso):
        print("El consumidor está durmiendo...")
        time.sleep(2)

def main():
    i = 0
    while i < 4:
        productor = threading.Thread(target=funcionProductor)
        productor.start()
        consumidor = threading.Thread(target=funcionConsumidor)
        consumidor.start()
        i = i+1

if __name__ == '__main__':
    main()