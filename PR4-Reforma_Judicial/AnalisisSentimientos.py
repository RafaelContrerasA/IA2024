import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt

# Descargar lexicón de VADER 
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

# Leer archivo CSV
def load_comments(csv_file):
    df = pd.read_csv(csv_file, encoding='latin1')
    if "Traduccion" not in df.columns:
        raise ValueError("El archivo CSV no tiene una columna llamada 'Traduccion'")
    return df["Traduccion"].dropna().tolist()

# Analizar sentimientos y contar comentarios positivos, neutrales y negativos
def analyze_sentiments(comments):
    sentiment_counts = {'pos': 0, 'neu': 0, 'neg': 0}
    
    print("Puntuaciones por comentario:")
    for idx, comment in enumerate(comments, start=1):
        scores = sia.polarity_scores(comment)
        print(f"Comentario {idx}: {scores}")  # Imprime las puntuaciones del comentario
        
        compound_score = scores['compound']
        if compound_score >= 0.05:
            sentiment_counts['pos'] += 1
        elif compound_score <= -0.05:
            sentiment_counts['neg'] += 1
        else:
            sentiment_counts['neu'] += 1
    
    total_comments = len(comments)
    
    # Calcular porcentajes
    sentiment_percentages = {key: (count / total_comments) * 100 for key, count in sentiment_counts.items()}
    return sentiment_percentages

# Graficar los resultados
def plot_sentiment_analysis(sentiment_percentages):
    labels = ['Positivo', 'Neutral', 'Negativo']
    values = [sentiment_percentages['pos'], sentiment_percentages['neu'], sentiment_percentages['neg']]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, values, color=['green', 'blue', 'red'], alpha=0.7)
    plt.title('Distribución de Sentimientos')
    plt.xlabel('Sentimiento')
    plt.ylabel('Porcentaje de comentarios')

    # Añadir los valores de porcentaje sobre las barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, f'{yval:.1f}%', ha='center', va='bottom')

    plt.ylim(0, 100)  # Los porcentajes van de 0 a 100
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Main
if __name__ == "__main__":
    csv_file = r"PR4-Reforma_Judicial\Judicial_English.csv"  # CSV comentarios y tweets
    try:
        comments = load_comments(csv_file)
        sentiment_percentages = analyze_sentiments(comments)

        print("\nAnálisis de sentimientos completado:")
        print(f"Porcentaje de comentarios positivos: {sentiment_percentages['pos']:.1f}%")
        print(f"Porcentaje de comentarios neutrales: {sentiment_percentages['neu']:.1f}%")
        print(f"Porcentaje de comentarios negativos: {sentiment_percentages['neg']:.1f}%")

        # Graficar los resultados
        plot_sentiment_analysis(sentiment_percentages)
    except Exception as e:
        print(f"Error: {e}")
