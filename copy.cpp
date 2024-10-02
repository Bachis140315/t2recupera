#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

#include "utils.cpp"
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

//Lee los bytes dentro de un archivo y retorna un vector con lo que representa cada byte
std::vector<char> leer_bytes_en_archivo(const std::string &filename) {
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
	if ((numBytes % sizeof(char)) != 0)
		throw std::runtime_error("raro, no cuadran los bytes");
	std::vector<char> vector;
	vector.resize(numBytes / sizeof(char));
	infile.read(reinterpret_cast<char*>(vector.data()), numBytes);
	if (infile.bad())
		throw std::runtime_error("error leyendo " + filename);
	return vector;
}

//Crea y escribe en un archivo con el vector de Mats, dentro de una carpeta especificada por los variables entrantes,
void escribir_bytes_en_archivo(const std::string& carpeta, const std::string& filename, const std::vector<double>& file_bytes) {
	crearVerificarCarpeta(carpeta);
	std::cout << filename << std::endl;
    std::ofstream outfile;
    outfile.open(filename, std::ios::app | std::ios::binary);
    
    if (!outfile.is_open()) {
        throw std::runtime_error("Error abriendo en " + filename);
    }
    
    // Corregimos el reinterpret_cast a const char*
    outfile.write(reinterpret_cast<const char*>(file_bytes.data()), file_bytes.size() * sizeof(double));
    outfile.close();

    if (outfile.bad()) {
        throw std::runtime_error("Error escribiendo en " + filename);
    }
}


