# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: [nombre]

# este archivo se puede importar en los .py 
# para tener funciones compartidas entre todos los  programas
import os
import pickle
import subprocess


samples_ventana = 4096
# funcion que recibe un nombre de archivo y llama a FFmpeg para crear un archivo wav
# requiere que el comando ffmpeg esté disponible
def convertir_a_wav(archivo_audio, sample_rate, dir_temporal):
    archivo_wav = "{}/{}.{}.wav".format(dir_temporal, os.path.basename(archivo_audio), sample_rate)
    if os.path.isfile(archivo_wav):
        return archivo_wav
    os.makedirs(dir_temporal, exist_ok=True)
    comando = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", archivo_audio, "-ac", "1", "-ar", str(sample_rate),
               archivo_wav]
    print("  {}".format(" ".join(comando)))
    code = subprocess.call(comando)
    if code != 0:
        raise Exception("ERROR en comando: " + " ".join(comando))
    return archivo_wav


# Retorna todos los archivos que terminan con el parametro extension
# ejemplo: listar_archivos_con_extension(dir, ".m4a") retorna los nombres de archivos .m4a en dir
def listar_archivos_con_extension(carpeta, extension):
    lista = []
    for archivo in os.listdir(carpeta):
        # los que terminan con la extension se agregan a la lista de nombres
        if archivo.endswith(extension):
            lista.append(archivo)
    lista.sort()
    return lista


# escribe el objeto de python en un archivo binario
def guardar_objeto(objeto, carpeta, nombre_archivo):
    if carpeta == "" or carpeta == "." or carpeta is None:
        archivo = nombre_archivo
    else:
        archivo = "{}/{}".format(carpeta, nombre_archivo)
        # asegura que la carpeta exista
        os.makedirs(carpeta, exist_ok=True)
    # usa la librería pickle para escribir el objeto en un archivo binario
    # ver https://docs.python.org/3/library/pickle.html
    with open(archivo, 'wb') as handle:
        pickle.dump(objeto, handle, protocol=pickle.HIGHEST_PROTOCOL)


# reconstruye el objeto de python que está guardado en un archivo
def leer_objeto(carpeta, nombre_archivo):
    if carpeta == "" or carpeta == "." or carpeta is None:
        archivo = nombre_archivo
    else:
        archivo = "{}/{}".format(carpeta, nombre_archivo)
    with open(archivo, 'rb') as handle:
        objeto = pickle.load(handle)
    return objeto


# Recibe una lista de listas y lo escribe en un archivo separado por \t
# Por ejemplo:
# listas = [
#           ["dato1a", "dato1b", "dato1c"],
#           ["dato2a", "dato2b", "dato2c"],
#           ["dato3a", "dato3b", "dato3c"] ]
# al llamar:
#   escribir_lista_de_columnas_en_archivo(listas, "archivo.txt")
# escribe un archivo de texto con:
# dato1a  dato1b   dato1c
# dato2a  dato2b   dato3c
# dato2a  dato2b   dato3c
def escribir_lista_de_columnas_en_archivo(lista_con_columnas, archivo_texto_salida):
    with open(archivo_texto_salida, 'w') as handle:
        for columnas in lista_con_columnas:
            textos = []
            for col in columnas:
                textos.append(str(col))
            texto = "\t".join(textos)
            print(texto, file=handle)


def lista_ventanas(nombre_archivo, numero_descriptores, sample_rate, samples_por_ventana):
    # tantas ventanas como numero de descriptores
    tiempos = []
    for i in range(0, samples_por_ventana * numero_descriptores, samples_por_ventana):
        # tiempo de inicio de la ventana
        segundos_desde = i / sample_rate
        # tiempo de fin de la ventana
        segundos_hasta = (i + samples_por_ventana - 1) / sample_rate
        # crear objeto
        v = (nombre_archivo, segundos_desde, segundos_hasta)
        # agregar a la lista
        tiempos.append(v)
    return tiempos


def imprimir_ventanas(ventanas, mfcc, muestreo_ventanas=1):
    print("ventanas={} descriptores={}".format(len(ventanas), mfcc.shape))
    print("mostrando algunas ventanas:")
    for i in range(0, len(ventanas), muestreo_ventanas):
        print(" {:4d}) {} descriptor={}".format(i, ventanas[i], mfcc[i].shape))
