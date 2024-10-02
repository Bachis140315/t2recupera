#include <iostream>
#include <filesystem>
#include <vector>
#include <cmath>


#include "copy.cpp"
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>


int main(int argc, char** argv){

    if (argc < 3) {
        std::cout << "uso: " << argv[0] << " [carpeta_audios_entrada] " <<" [carpeta_descriptores_salida] " << std::endl; 
		return 1;
	}


    std::string carpetaAudios = argv[1];

    //Buscar nombres de los archivos en la carpeta "dir_imagenes_Q"
    std::vector<std::string> nombresAudiosR = listarArchivosEnCarpeta(carpetaAudios + "/canciones/", ".m4a");

    //Buscar nombres de los archivos en la carpeta "dir_imagenes_R"
    std::vector<std::string> nombresAudiosQ = listarArchivosEnCarpeta(carpetaAudios + "/radio/", ".m4a");

    //Obtener nombre del txt donde se guardaran los resultados
    std::string carpetaArchivoSalida = argv[2];

    /*Computar los descriptores de los audios R
    1. Convertir audio a wav
    2. Obtener descriptor
    3. Escribir descriptor en archivos en la carpeta correspondiente
    */
    for (std::string audio : nombresAudiosR){
        //Obtener descriptor por cada ventana de audio y escribirlo todo en un solo archivo
        std::pair<std::string, std::vector<double>> descriptor = crearRetornarMFCCDescriptor(carpetaAudios + "/canciones/", audio, 44100);
        std::vector<double> realdescriptor = descriptor.second;
        std::cout << "llegamos aqui " << std::endl;
        escribir_bytes_en_archivo(carpetaArchivoSalida, descriptor.first, realdescriptor);
    }

    for (std::string audio : nombresAudiosQ){
        std::pair<std::string, std::vector<double>> descriptor = crearRetornarMFCCDescriptor(carpetaAudios + "/radio/", audio, 44100);
        std::vector<double> realdescriptor = descriptor.second;
        std::cout << "llegamos aqui 2" << std::endl;
        escribir_bytes_en_archivo(carpetaArchivoSalida, descriptor.first, realdescriptor);
    }

    return 0;
}