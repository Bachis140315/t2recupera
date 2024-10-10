# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: [nombre]

import sys
import os
import util as util
import scipy
import numpy


def tarea2_busqueda(carpeta_descriptores_radio_Q, carpeta_descritores_canciones_R, archivo_ventanas_similares):
    if not os.path.isdir(carpeta_descriptores_radio_Q):
        print("ERROR: no existe {}".format(carpeta_descriptores_radio_Q))
        sys.exit(1)
    elif not os.path.isdir(carpeta_descritores_canciones_R):
        print("ERROR: no existe {}".format(carpeta_descritores_canciones_R))
        sys.exit(1)
    elif os.path.exists(archivo_ventanas_similares):
        print("ERROR: ya existe {}".format(archivo_ventanas_similares))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer Q y R: datos en carpeta_descriptores_radio_Q y carpeta_descritores_canciones_R
    #     esas carpetas fueron creadas por tarea2_extractor con los audios de radio y canciones
    #     puede servir la funcion util.leer_objeto() que está definida en util.py
    #     LISTO!!
    #
    #  2-para cada descriptor de Q localizar el más cercano en R
    #     podría usar cdist (ver semana 02) o algún índice de busqueda eficiente (Semanas 03-04)
    #
    #  3-escribir en el archivo archivo_ventanas_similares una estructura que asocie
    #     cada ventana de Q con su ventana más parecida en R
    #     recuerde guardar el nombre del archivo y los tiempos de inicio y fin que representa cada ventana de Q y R
    #     puede servir la funcion util.guardar_objeto() que está definida en util.py
    #
    

    # Se obtienen nombres de los archivos binarios con el descriptor MFCC para las canciones y para los audios de radio
    nombres_descriptores_canciones = util.listar_archivos_con_extension(carpeta_descritores_canciones_R, '.wavcancionbin')
    nombres_descriptores_radio = util.listar_archivos_con_extension(carpeta_descriptores_radio_Q, '.wavradiobin')


    #Se leer archivo binario con MFCC de la cancion y se guarda en un arreglo, ademas de obtener las ventanas desde el segundo
    #que comienzan hasta que terminan
    mfccs_canciones = []
    ventanas_canciones = []
    for binario_cancion in nombres_descriptores_canciones:
        cancion = util.leer_objeto(carpeta_descritores_canciones_R, binario_cancion)
        mejor_cancion = cancion[:, 2:]

        cancion_ventanas = util.lista_ventanas(binario_cancion, cancion.shape[0], 44100, util.samples_ventana)

        if len(mfccs_canciones) == 0:
            mfccs_canciones = mejor_cancion
        else:
            # agregar como filas
            mfccs_canciones = numpy.vstack([mfccs_canciones, mejor_cancion])

        ventanas_canciones.extend(cancion_ventanas)

    
    #util.imprimir_ventanas(ventanas_canciones, mfccs_canciones, 50)

    #Se realiza lo mismo que anteriormente pero para las radios
    
    for descriptor_radio in nombres_descriptores_radio:

        ventanas_radio = []
        mfccs_radios = util.leer_objeto(carpeta_descriptores_radio_Q , descriptor_radio)
        mejor_mfccs_radio = mfccs_radios[:, 2:]
        #print(mejor_mfccs_radio)
        #print('\n')
        radio_ventanas = util.lista_ventanas(descriptor_radio, mejor_mfccs_radio.shape[0], 44100, util.samples_ventana)


        ventanas_radio.extend(radio_ventanas)

        #Se calcula para cada radio la distancia euclideana entres los descriptores de cada 
        distancias = scipy.spatial.distance.cdist(mejor_mfccs_radio, mfccs_canciones, metric='euclidean')

        #Devuelve las posiciones de los que tienen distancia minima dentro de 'mfccs_canciones' por cada arreglo en 'mfccs_radios'
        index_min = numpy.argmin(distancias, axis=1)


        dist_min = numpy.amin(distancias, axis=1)

        with open(archivo_ventanas_similares, 'a') as archivo_output:
            for i in range(len(mejor_mfccs_radio)):
                query = ventanas_radio[i]
                conocido = ventanas_canciones[index_min[i]]
                diferencia = (conocido[1] - query[1])

                nombre_radio_separado = query[0].split('.')
                nombre_radio_original = nombre_radio_separado[0] + '.' + nombre_radio_separado[1]

                nombre_cancion_separado = conocido[0].split('.')
                nombre_cancion_original = nombre_cancion_separado[0] + '.' + nombre_cancion_separado[1]

                #print(" {:4d}) {}  se parece a  {} [{}-{}]  (diferencia de tiempos={:4.1f} seg.)".format(i, query, conocido[0], conocido[1], conocido[2],  diferencia))
                archivo_output.write("{} {} {} {} \n".format(nombre_radio_original, query[1], nombre_cancion_original, conocido[1]))
            

        
    return



# inicio de la tarea
if len(sys.argv) != 4:
    print(
        "Uso: {} [carpeta_descriptores_radio_Q] [carpeta_descritores_canciones_R] [archivo_ventanas_similares]".format(
            sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_descriptores_radio_Q = sys.argv[1]
carpeta_descritores_canciones_R = sys.argv[2]
archivo_ventanas_similares = sys.argv[3]

# llamar a la tarea
tarea2_busqueda(carpeta_descriptores_radio_Q, carpeta_descritores_canciones_R, archivo_ventanas_similares)
