# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: [nombre]

import sys
import os
import util as util
import librosa


def tarea2_extractor(carpeta_audios_entrada, carpeta_descriptores_salida):
    if not os.path.isdir(carpeta_audios_entrada):
        print("ERROR: no existe {}".format(carpeta_audios_entrada))
        sys.exit(1)
    elif os.path.exists(carpeta_descriptores_salida):
        print("ERROR: ya existe {}".format(carpeta_descriptores_salida))
        sys.exit(1)


    #  1-leer los archivos con extension .m4a que están carpeta_audios_entrada
    #    puede servir la funcion util.listar_archivos_con_extension() que está definida en util.py
    nombres_audios = util.listar_archivos_con_extension(carpeta_audios_entrada , '.m4a')

    for audio in nombres_audios:
        # 2-convertir a wav
        audio_wav = util.convertir_a_wav(carpeta_audios_entrada + audio, 44100, carpeta_descriptores_salida)

        # 3-descriptor mfcc para cada wav
        samples, sr = librosa.load(audio_wav, sr=None)
        print("audio samples={} samplerate={} segundos={:.1f}".format(len(samples), sr, len(samples) / sr))
        cancion_mfcc = librosa.feature.mfcc(y=samples, sr=sr, n_mfcc=42, n_fft=util.samples_ventana, hop_length=util.samples_ventana)
        descriptor = cancion_mfcc.transpose()

        # 3-guardar descriptor en un archivo
        util.guardar_objeto(descriptor, None, audio_wav + 'bin' )




    


# inicio de la tarea
if len(sys.argv) != 3:
    print("Uso: {} [carpeta_audios_entrada] [carpeta_descriptores_salida]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_audios_entrada = sys.argv[1]
carpeta_descriptores_salida = sys.argv[2]

# llamar a la tarea
tarea2_extractor(carpeta_audios_entrada, carpeta_descriptores_salida)
