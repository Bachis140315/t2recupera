#include <cstdlib>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <sstream>
#include <stdexcept>
#include <utility>

#include "Mfcc.cpp"
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>


namespace fs = std::filesystem;

template<typename T>
std::vector<T> leer_bytes_archivo(const std::string &filename) {
	//abrir el archivo
	std::ifstream infile;
	infile.open(filename);
	if (!infile.is_open())
		throw std::runtime_error("no puedo abrir " + filename);
	//ir al final
	infile.seekg(0, std::ios::end);
	//obtener la posicion en bytes
	int numBytes = infile.tellg();
	//volver al inicio
	infile.seekg(0, std::ios::beg);
	//leer todos los bytes del archivo
	if ((numBytes % sizeof(T)) != 0)
		throw std::runtime_error("no cuadran los bytes");
	std::vector<T> vector;
	vector.resize(numBytes / sizeof(T));
	infile.read(reinterpret_cast<char*>(vector.data()), numBytes);
	if (infile.bad())
		throw std::runtime_error("error leyendo " + filename);
	return vector;
}

void crearVerificarCarpeta(std::string rutaCarpeta){
    if (!fs::exists(rutaCarpeta)){
        if (fs::create_directory(rutaCarpeta)) {
            std::cout << "Carpeta creada exitosamente: " << rutaCarpeta << std::endl;
        } else {
            std::cerr << "Error al crear la carpeta: " << rutaCarpeta << std::endl;
        }
    } else {
        std::cout << "La carpeta ya existe: " << rutaCarpeta << std::endl;
    }
}

//Convierte un audio en formato .wav
std::string convertirAudioWav(std::string dataset, std::string nombreAudio, int sampleRate){
    
    std::string carpeta = "./wavs" ;  // Carpeta que queremos crear
    crearVerificarCarpeta(carpeta);

    std::stringstream oss;
    std::size_t soloNombre = nombreAudio.find_last_of('.');
    oss << carpeta << "/" << nombreAudio.substr(0, soloNombre) << "." << std::to_string(sampleRate) << ".wav";
    std::cout << oss.str() << std::endl;
    std::cout << !fs::exists(oss.str()) << std::endl;
    if(fs::exists(oss.str())){
        return "nothing";
    }

    std::string rutaArchivo = dataset + nombreAudio;
    //Crear archivo
    std::stringstream createRaw;
    createRaw << "ffmpeg " << "-hide_banner -loglevel error -i " << '"' + rutaArchivo + '"' << " -ac 1 -ar " << std::to_string(sampleRate) << " " << "-acodec pcm_s16le -f s16le " << '"' + oss.str() + '"';
    std::string createRawCommand = createRaw.str();
    
    int ret = std::system(createRawCommand.c_str());
	if (ret != 0)
		throw std::runtime_error("error al ejecutar: " + createRawCommand);

    return oss.str();
}

std::vector<double> crearDescriptorMfcc(std::string ruta, int sampleRate){
    std::vector<double> samples = leer_bytes_archivo<double>(ruta);
    std::vector<double> mfcc_descriptor;
    Mfcc mfcc; 
    mfcc.init(sampleRate, 48, (sampleRate/2)+1, 48);
    mfcc.getCoefficients(samples, mfcc_descriptor);
    return mfcc_descriptor;
}


std::pair<std::string, std::vector<double>> crearRetornarMFCCDescriptor(std::string dataset, std::string rutaArchivo, int sampleRate){
    std::string rutaWav = convertirAudioWav(dataset, rutaArchivo, sampleRate);
    return std::pair<std::string, std::vector<double>>(rutaWav,crearDescriptorMfcc(rutaWav, sampleRate));
}



//Se retorna un vector con los nombres de los archivos .jpg que estan en 'nombreCarpeta'
std::vector<std::string> listarArchivosEnCarpeta(std::string nombreCarpeta, std::string extension){

    std::string pathCarpeta = fs::current_path().string() + "/" + nombreCarpeta;
    std::vector<std::string> nombresArchivos;

    try {
        for (const auto& entry : fs::directory_iterator(pathCarpeta)) {

            if (entry.path().extension() == extension) {
                std::string fileName = entry.path().filename().string();  
                nombresArchivos.push_back(fileName);
            }   
        }
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    
    return nombresArchivos;
}

void escribirListaDeColumnasEnArchivo(std::vector<std::string> listaImagenesOriginales, const std::vector<std::pair<double, std::string>>& listaConColumnas, const std::string& archivoTextoSalida) {
    std::ofstream handle(archivoTextoSalida, std::ios::out | std::ios::trunc);

    if (!handle.is_open()) {
        throw std::ios_base::failure("Error al abrir el archivo.");
    }

    if (listaImagenesOriginales.size() != listaConColumnas.size()) {
        throw std::invalid_argument("El tamaño de listaImagenesOriginales debe coincidir con el tamaño de listaConColumnas.");
    }
    
    for (size_t i = 0; i < listaImagenesOriginales.size(); i++){
        std::pair<double, std::string> parR = listaConColumnas[i];
        std::string original = listaImagenesOriginales[i];

        std::stringstream textoStream;
        handle << original << "\t" << parR.second<< "\t" << parR.first << "\n" ;
    }
    

    handle.close();
}
