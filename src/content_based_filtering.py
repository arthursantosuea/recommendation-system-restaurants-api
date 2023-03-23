import pandas as pd

import nltk

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import json

# Função para extrair dados (cidades ou países) do input
def extracting_data(description, data, dataset, recommendations):
    data_list = dataset[data].unique()
    data_input = []

    for i in data_list:
        if i in description:
            data_input.append(i)
            description = description.replace(i, '')
    
    if data_input:
        recommendation = recommendations[recommendations[data].isin(data_input)]
        if recommendation.empty:
            for i in data_input:
                recommendations = recommendations.append(dataset.loc[dataset[data] == i])
        else:
            recommendations = recommendation

    return recommendations, description


# Função para extrair preços do input
def extracting_price(description, recommendations):
    # Definindo sinônimos das faixas de preço dos restaurantes
    price_map = {
        "cheap-eats": ("cheap", "inexpensive", "low-price", "low-cost", "economical", "economic", "affordable"),
        "mid-range": ("moderate", "fair", "mid-price", "reasonable", "average"),
        "fine-dining": ("expensive", "fancy", "lavish")
    }

    for key, value in price_map.items():
        if any(v in description for v in value):
            recommendations = recommendations[recommendations["price"] == key]
            break
    
    return recommendations


# Função para processar as sentenças
def process_sentences(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    temp_sentence = []

    # Palavras tokenizadas
    words = nltk.word_tokenize(text)

    # Lematizar cada palavra baseado na posição das mesmas na frase
    tags = nltk.pos_tag(words)

    for i, word in enumerate(words):
        if tags[i][1] in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
            lemmatized = lemmatizer.lemmatize(word, 'v')
        else:
            lemmatized = lemmatizer.lemmatize(word)
        
        # Removendo stop words e tokens não alfabéticos
        if lemmatized not in stop_words and lemmatized.isalpha(): 
            temp_sentence.append(lemmatized)

    # Ajustando formatação
    full_sentence = ' '.join(temp_sentence)
    full_sentence = full_sentence.replace("n't", " not")
    full_sentence = full_sentence.replace("'m", " am")
    full_sentence = full_sentence.replace("'s", " is")
    full_sentence = full_sentence.replace("'re", " are")
    full_sentence = full_sentence.replace("'ll", " will")
    full_sentence = full_sentence.replace("'ve", " have")
    full_sentence = full_sentence.replace("'d", " would")

    return full_sentence


# Função para recomendar restaurantes baseado no input do usuário
def recommendation(user_input, dataset):
    # Criando dataset para armazenar dados compatíveis
    recommendations = dataset.copy()

    # Convertendo input para letras minúsculas
    description = str(user_input).lower()

    # Extraindo cidades, países e preços do input
    recommendations, description = extracting_data(description, "city", dataset, recommendations)
    recommendations, description = extracting_data(description, "country", dataset, recommendations)
    recommendations = extracting_price(description, recommendations)

    # Processando o input do usuário 
    description = process_sentences(description)
    description = description.strip()
    print("Processed user feedback:", description)

    # Iniciando um vetorizador TD-IDF
    tf_idf_vec = TfidfVectorizer()

    # Ajustando dados para os reviews já processados
    vec = tf_idf_vec.fit(recommendations["bag_of_words"])
    features = vec.transform(recommendations["bag_of_words"])

    # Transformando o input do usuário no modelo processado
    description_vector =  vec.transform([description])

    # Calculando a similaridade cosseno entre o input do usuário e os reviews
    cos_sim = linear_kernel(description_vector, features)

    # Adicionando a similaridade ao dataset
    recommendations["similarity"] = cos_sim[0]

    # Ordenando o dataset pela similaridade
    recommendations.sort_values(by="similarity", ascending=False, inplace=True)

    # return dataset[["name", "city", "country", "price", "style", "reviews", "similarity"]]

    return recommendations.index.values


# Função para retornar os dados a serem mostrados no front-end
def restaurants_data(recommended_restaurants, dataset):
    restaurants = pd.DataFrame()
    count = 0

    for restaurant in recommended_restaurants:
        if count < 100:
            restaurants = restaurants.append(dataset.iloc[[restaurant]], ignore_index=True)
            count += 1
        else:
            break

    response = json.loads(restaurants.to_json(orient="records"))
    # response_json = json.loads(response)

    return response

# Lendo o dataset para recomendação
data_restaurants = pd.read_csv("../datasets/recommendation_dataset.csv")

# Lendo o dataset para exposição dos dados
data_frontend = pd.read_csv("../datasets/restaurants_TripAdvisor.csv")

# user_input = input("Input: ")
# rec = recommendation(user_input, data_restaurants)
# x = restaurants_data(rec, data_frontend)
# x.to_csv("rec.csv", index=True, header=True)
