# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: [nombre]
import math
import sys
import os
import util as util


def tarea2_deteccion(archivo_ventanas_similares, archivo_detecciones):
    if not os.path.isfile(archivo_ventanas_similares):
        print("ERROR: no existe archivo {}".format(archivo_ventanas_similares))
        sys.exit(1)
    elif os.path.exists(archivo_detecciones):
        print("ERROR: ya existe archivo {}".format(archivo_detecciones))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer el archivo archivo_ventanas_similares (fue creado por tarea2_busqueda)
    #    puede servir la funcion util.leer_objeto() que está definida en util.py
    #
    #  2-crear un algoritmo para buscar secuencias similares entre audios
    #    ver slides de la semana 5 y 7
    #    identificar grupos de ventanas de Q y R que son similares y pertenecen a las mismas canciones con el mismo desfase
    

    
    #En este diccionario estará como llave el nombre de la radio y la cancion y como valor un par [desfase, contador]
    repeticiones_canciones = {}
    with open(archivo_ventanas_similares, 'r') as similares:
        for linea in similares:
            #Esta varible contiene ['nombre_radio', 'inicio_ventana_radio', 'nombre_cancion', 'inicio_ventana_cancion']
            division = linea.split(' ')
            
            # Se convierten a float los inicios de ventanas
            inicio_cancion = float(division[len(division) - 2])
            inicio_radio = float(division[1])

            # Obtener desfases:
            # Se redondea al medio segundo
            desfase_real = abs(round(2*(inicio_radio - inicio_cancion), 0)/2)

            # Se crea otro desfase mas 'grueso' en su aproximacion, para que tenga se tenga un margen para meter ventanas
            desfase_dicc = math.trunc(desfase_real)

            # Formateo de el nombre de la llave        
            nombre_radio = division[0]
            nombre_cancion = ' '.join(division[2:len(division)-2])

            llave = nombre_radio + '#' + nombre_cancion + '#' + str(desfase_dicc)


            
            if llave in repeticiones_canciones:
                arreglo = repeticiones_canciones[llave]
                arreglo[0] += 1
                if inicio_cancion > arreglo[2]:
                    arreglo[2] = round(inicio_cancion, 1)
                repeticiones_canciones[llave] = arreglo
            else:
                # Cada llave tiene como valor ['votaciones', 'desfase del diccionario', 'maximo registrado de tiempo de la cancion', 'desfase real']
                repeticiones_canciones[llave] = [1, desfase_dicc ,round(inicio_cancion, 1), desfase_real]


    #Primer filtro, unir canciones que tengan desfases parecidos y que tengan hartos votos
    nombres_seleccionados = {}
    for llave in repeticiones_canciones:
        arreglo = repeticiones_canciones[llave]
        if arreglo[0] > 20:
            nombres = llave.split('#')

            nueva_llave = nombres[0] + '#' + nombres[1]
            if nueva_llave in nombres_seleccionados:
                posibles_fusiones = nombres_seleccionados[nueva_llave]
                #Si es 0 despues del for, es porque ninguna de las repeticiones de esa cancion existentes es parecido a este caso
                indentificado = 0
                for i in range(len(posibles_fusiones)):
                    if abs(posibles_fusiones[i][1]-arreglo[3]) < 2.0:
                        #Se suman los votos
                        posibles_fusiones[i][1] += arreglo[0]
                        if arreglo[2] > posibles_fusiones[i][2]:
                            posibles_fusiones[i][2] = arreglo[2]

                        indentificado = 1
                        break
                if indentificado == 0:
                    #Se agrega al vector de repeticiones de la cancion una nueva repeticion
                    posibles_fusiones.append([arreglo[0], arreglo[3], arreglo[2]])
                    nombres_seleccionados[nueva_llave] = posibles_fusiones

            else:
                #El arreglo contiene = [Ventanas, desfase, inicio cancion], 
                nombres_seleccionados[nueva_llave] = [[arreglo[0], arreglo[3], arreglo[2]]]


    #Ultimo filtro, eliminar las que tengan menos de 15 votos
    canciones_finales = []
    for llave in nombres_seleccionados:
        arreglos = nombres_seleccionados[llave]
        for subarreglo in arreglos:
            if subarreglo[0] > 10:
                nombres = llave.split('#')

                nombres.extend(subarreglo)
                canciones_finales.append(nombres)

    
    canciones_finales.sort(key=lambda x: (x[0], x[3]))


    #  3-escribir las detecciones encontradas en archivo_detecciones, en un archivo con 5 columnas:
    #    columna 1: nombre de archivo Q (nombre de archivo en carpeta radio)
    #    columna 2: tiempo de inicio (número, tiempo medido en segundos de inicio de la emisión)
    #    columna 3: largo de la detección (número, tiempo medido en segundos con el largo de la emisión)
    #    columna 4: nombre de archivo R (nombre de archivo en carpeta canciones)
    #    columna 5: confianza (número, mientras más alto mayor confianza de la respuesta)
    with open(archivo_detecciones, 'a') as detecciones_finales:
        for cancion in canciones_finales:
            detecciones_finales.write("{}\t {}\t {}\t {}\t {}\n".format(cancion[0], cancion[3], cancion[4], cancion[1], cancion[2]))

        


    return
       


# inicio de la tarea
if len(sys.argv) != 3:
    print("Uso: {} [archivo_ventanas_similares] [archivo_detecciones]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
archivo_ventanas_similares = sys.argv[1]
archivo_detecciones = sys.argv[2]

# llamar a la tarea
tarea2_deteccion(archivo_ventanas_similares, archivo_detecciones)
