import csv
import requests
import uuid

def translate_text(subscription_key, endpoint, region, text, target_language):
    path = '/translate?api-version=3.0'
    params = f'&to={target_language}'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()

    translations = response.json()
    return translations[0]['translations'][0]['text']

def translate_csv(input_csv, output_csv, subscription_key, endpoint, region, target_language, start_line=0):
    with open(input_csv, 'r', encoding='latin1') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Traduccion']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Saltamos las líneas anteriores a 'start_line'
        for i, row in enumerate(reader):
            if i < start_line:
                continue  # Si la línea es antes de la línea de inicio, saltarla

            original_comment = row['Comentarios']
            translated_comment = translate_text(subscription_key, endpoint, region, original_comment, target_language)
            row['Traduccion'] = translated_comment
            writer.writerow(row)

if __name__ == "__main__":
    # Configuración de la API
    subscription_key = "my_key"  # Reemplaza con tu clave de suscripción
    endpoint = "https://api.cognitive.microsofttranslator.com/"  # Endpoint de Azure Translator
    region = "eastus"  # Reemplaza con tu región

    # Archivos de entrada y salida
    input_csv = r"PR4-Reforma_Judicial\Organismos_Comentarios.csv"  # Archivo de entrada con la columna 'Comentarios'
    output_csv = 'Organismos_traducidos2.csv'  # Archivo de salida

    # Idioma de destino para la traducción
    target_language = 'en'  # Cambia esto según el idioma deseado, por ejemplo, 'es', 'fr', etc.

    # Línea desde la que empezar la traducción (por ejemplo, empieza desde la línea 10)
    start_line = 2007

    translate_csv(input_csv, output_csv, subscription_key, endpoint, region, target_language, start_line)
    print(f"Archivo traducido guardado en: {output_csv}")
