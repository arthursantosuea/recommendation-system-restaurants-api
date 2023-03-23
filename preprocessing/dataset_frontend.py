import pandas as pd
from ast import literal_eval
    

# Importando dataset
# Link: https://www.kaggle.com/datasets/damienbeneschi/krakow-ta-restaurans-data-raw
trip_advisor_df = pd.read_csv("../datasets/original_dataset.csv")

# Copiando dataset para tratamento
df_ta = trip_advisor_df.copy()

# Substituindo os reviews nulos por listas vazias e excluindo elementos nulos
df_ta["Reviews"].replace("[[], []]", pd.NA, inplace=True)
df_ta.dropna(subset=["Name", "City", "Cuisine Style", "Price Range", "Reviews"], inplace=True)

# Convertendo strings para itens de lista
df_ta["Cuisine Style"] = df_ta["Cuisine Style"].apply(lambda x: literal_eval(x))
df_ta["Cuisine Style"] = df_ta["Cuisine Style"].apply(lambda x: ', '.join(x))

# Excluindo elementos nulos
df_ta.dropna(subset=["Name", "City", "Cuisine Style", "Price Range", "Reviews"], inplace=True)

# Criando um dataframe com as cidades e seus respetivos países
cities_list = df_ta["City"].unique()
countries_list = ["Netherlands", "Greece", "Spain", "Germany", "Slovakia", 
             "Belgium", "Hungary", "Denmark", "Ireland", "Scotland", 
             "Switzerland", "Germany", "Finland", "Poland", "Portugal", 
             "Slovenia", "England", "Luxembourg", "France", "Spain", 
             "Italy", "Germany", "Portugal", "Norway", "France", 
             "Czech Republic", "Italy", "Sweden", "Austria", "Poland", "Switzerland"]

countries_and_cities = {"City": cities_list, "Country": countries_list}

df_cities_countries = pd.DataFrame(data=countries_and_cities)

# Excluindo colunas não utilizadas
df_ta.drop(columns=["Unnamed: 0", "Ranking", "Reviews", "ID_TA"], inplace=True)

# Inserindo os países associados às cidades
df_ta = pd.merge(df_ta, df_cities_countries, on="City", how="inner")
df_ta = df_ta.reindex(columns=['Name', 'City', 'Country', 'Cuisine Style', 
                               'Rating', 'Price Range', 'Number of Reviews', 'URL_TA'])

# Renomeando as colunas
df_ta.rename(columns={"Cuisine Style": "CuisineStyle", 
                      "Price Range": "PriceRange",
                      "Number of Reviews": "NumberOfReviews"}, inplace=True)

# Salvando dataset para vizualização no front-end
df_ta.to_csv("../datasets/restaurants_TripAdvisor.csv", header=True, index=False)
