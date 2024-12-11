import os
import requests
import json
import uuid  

# Configuración de la API
SUBSCRIPTION_KEY = "azure_key"
ENDPOINT = "https://api.bing.microsoft.com/v7.0/images/search"

def buscar_imagenes(query, excluded_terms, count=2000):
    headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
    resultados = []
    params = {
        "q": query + " -" + " -".join(excluded_terms)
        ,
        "count": 50,  #La api no deja mas de 50 por solicitud
        "offset": 0,
        "imageType": "Photo",
        "safeSearch": "Off",
    }
    
    while len(resultados) < count:
        response = requests.get(ENDPOINT, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error en la solicitud: {response.status_code}")
            break
        
        data = response.json()
        images = data.get("value", [])
        
        for image in images:
            resultados.append(image["contentUrl"])
        
        print(f"Resultados obtenidos: {len(resultados)}")
        
        # Avanzar en los resultados
        params["offset"] += 50
        
        if len(images) < 50:  # No hay más resultados
            break
    
    return resultados[:count]

def descargar_imagenes(query, urls):
    carpeta = query
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Encabezados simulando un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Referer": "https://www.bing.com/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    for i, url in enumerate(urls):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=5)
            if response.status_code == 200:
                extension = url.split(".")[-1].split("?")[0]
                unique_id = str(uuid.uuid4())  # Generar un ID único
                archivo = os.path.join(carpeta, f"image_{unique_id}.{extension}")
                
                with open(archivo, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Imagen descargada: {archivo}")
            else:
                print(f"Error al descargar la imagen {i}: {response.status_code}")
        except Exception as e:
            print(f"Error al descargar la imagen {i}: {e}")

# Búsqueda y descarga
if __name__ == "__main__":
    query = "rolls-royce"
    excluded_terms = ["cullinan"]
    
    # Realizar búsqueda
    print("Buscando imágenes...")
    resultados = buscar_imagenes(query, excluded_terms)
    
    # Guardar resultados en un archivo JSON
    with open(f"{query}_resultados.json", "w") as f:
        json.dump(resultados, f, indent=4)
    
    print(f"Total de imágenes obtenidas: {len(resultados)}")
    
    # Descargar imágenes
    print("Descargando imágenes...")
    descargar_imagenes(query, resultados)
