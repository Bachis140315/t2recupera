# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: [nombre]

import sys
import os
import util as util


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
    #
    #  2-para cada descriptor de Q localizar el más cercano en R
    #     podría usar cdist (ver semana 02) o algún índice de busqueda eficiente (Semanas 03-04)
    #
    #  3-escribir en el archivo archivo_ventanas_similares una estructura que asocie
    #     cada ventana de Q con su ventana más parecida en R
    #     recuerde guardar el nombre del archivo y los tiempos de inicio y fin que representa cada ventana de Q y R
    #     puede servir la funcion util.guardar_objeto() que está definida en util.py
    #
    # borrar las siguientes lineas
    print("ERROR: tarea2_busqueda no implementado!")
    sys.exit(1)


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
