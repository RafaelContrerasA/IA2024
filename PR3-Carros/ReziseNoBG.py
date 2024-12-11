import os
from PIL import Image
from rembg import remove

def process_images(input_folder, output_folder, target_size=(21, 28)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extensiones válidas para las imágenes
    valid_extensions = ('png', 'jpg', 'jpeg', 'bmp', 'webp')

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # Verifica si es un archivo válido de imagen
        if os.path.isfile(input_path) and filename.lower().endswith(valid_extensions):
            try:
                # Cargar la imagen
                with open(input_path, 'rb') as file:
                    input_image = file.read()
                
                # Eliminar el fondo
                output_image = remove(input_image)
                
                # Guardar temporalmente la imagen sin fondo
                temp_image_path = os.path.join(output_folder, f"temp_{filename}")
                with open(temp_image_path, 'wb') as temp_file:
                    temp_file.write(output_image)
                
                # Cargar la imagen sin fondo, redimensionarla y convertirla a RGB (3 canales)
                with Image.open(temp_image_path) as img:
                    
                    # Convertir a RGB si tiene canal alfa
                    img_rgb = img.convert('RGB')
                    resized_img = img_rgb.resize(target_size)
                    
                    final_path = os.path.join(output_folder, filename)
                    resized_img.save(final_path, format='JPEG')

                # Elimina la imagen temporal
                os.remove(temp_image_path)

                print(f"Procesada: {filename}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")



# Parámetros
input_folder = r'Hummer Dataser'  # Cambiar por la ruta de la carpeta de entrada
output_folder = r'Hummer_resized_noBG'  # Cambiar por la ruta de la carpeta de salida

# Procesar las imágenes
process_images(input_folder, output_folder)
