import pandas as pd
import nltk
from ast import literal_eval
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


# Função para converter os reviews em listas
def convert_to_list(x):
    try:
        return literal_eval(x)
    except ValueError:
        return pd.NA


# Função para processar as sentenças
def process_sentences(text):
    # Normalização
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


# Importando dataset
# Link: https://www.kaggle.com/datasets/damienbeneschi/krakow-ta-restaurans-data-raw
trip_advisor_df = pd.read_csv("../datasets/original_dataset.csv")

# Copiando dataset para tratamento
final_ta_df = trip_advisor_df.copy()

# Removendo atributos não relevantes
final_ta_df.drop(columns=["Unnamed: 0", 
                          "Ranking", 
                          "Rating", 
                          "Number of Reviews", 
                          "URL_TA", 
                          "ID_TA"], inplace=True)

# Renomeando as colunas
final_ta_df.rename(columns={"Name": "name", 
                            "City": "city", 
                            "Cuisine Style": "style", 
                            "Price Range": "price", 
                            "Reviews": "reviews"}, inplace=True)

# Substituindo os reviews nulos por listas vazias e excluindo elementos nulos
final_ta_df["reviews"].replace("[[], []]", pd.NA, inplace=True)
final_ta_df.dropna(inplace=True)

# Ajustando formatações
# Padronizando todas as letras para minúsculas
final_ta_df["reviews"] = final_ta_df["reviews"].str.lower()
final_ta_df["style"] = final_ta_df["style"].str.lower()
final_ta_df["city"] = final_ta_df["city"].str.lower()

# Convertendo strings para itens de lista e juntando-os
final_ta_df["style"] = final_ta_df["style"].apply(lambda x: literal_eval(x))
final_ta_df["style"] = final_ta_df["style"].apply(lambda x: ', '.join(x))

# Convertendo strings para itens de lista e lixo para elementos nulos
final_ta_df["reviews"] = final_ta_df["reviews"].apply(convert_to_list)

# Excluindo elementos nulos
final_ta_df.dropna(inplace=True)

# Juntando os itens da lista
# x[0] -> review
# x[1] -> data e hora da publicação de cada review
final_ta_df["reviews"] = final_ta_df["reviews"].apply(lambda x: '; '.join(x[0]))

# Substituindo as faixas de preço
final_ta_df["price"].replace(['$', "$$ - $$$", "$$$$"], 
                             ["cheap-eats", "mid-range", "fine-dining"], 
                             inplace=True)

# Criando um dataframe com as cidades e seus respetivos países
cities_list = final_ta_df["city"].unique()
countries_list = ["netherlands", "greece", "spain", "germany", "slovakia", 
             "belgium", "hungary", "denmark", "ireland", "scotland", 
             "switzerland", "germany", "finland", "poland", "portugal", 
             "slovenia", "england", "luxembourg", "france", "spain", 
             "italy", "germany", "portugal", "norway", "france", 
             "czech republic", "italy", "sweden", "austria", "poland", "switzerland"]

countries_and_cities = {"city": cities_list, "country": countries_list}

df_cities_countries = pd.DataFrame(data=countries_and_cities)

# Inserindo os países associados às cidades
final_ta_df = pd.merge(final_ta_df, df_cities_countries, on="city", how="inner")
final_ta_df = final_ta_df.reindex(columns=["name", "city", "country", "price", "style", "reviews"])

# Processando "reviews" e "cuisine style"
final_ta_df["reviews_processed"] = final_ta_df["reviews"].apply(process_sentences)
final_ta_df["style_processed"] = final_ta_df["style"].apply(process_sentences)

# Unindo os dados processados em uma única coluna
final_ta_df["bag_of_words"] = final_ta_df["style_processed"] + ' ' + final_ta_df["reviews_processed"]

# Excluindo atributos não utilizados
final_ta_df.drop(columns=["style", "reviews", "style_processed", "reviews_processed"], inplace=True)

# Salvando dataset para uso nas recomendações
final_ta_df.to_csv("../datasets/recommendation_dataset.csv", header=True, index=True)
