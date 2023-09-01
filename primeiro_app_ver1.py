import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import openai

headers = {
	"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

opcoes = ['ninho forti+ zero lactose nestlé 380g', 'ninho forti+ zero lactose nestlé 700g', 'leite em pó ninho integral 380 gr', 'fralda huggies xxg tripla proteção', '200 toalhas umedecida fisher price', 'shampoo ducray anaphase 200ml', 'shampoo ducray anaphase 400ml']

st.title('Aplicativo Para Buscar Preço de Produtos')


pesquisa = st.selectbox('Selecione o produto a ser buscado',opcoes)


response = requests.get(
	"https://www.google.com.br/search",
	headers = headers,
	params = {
		"q" : pesquisa,
		"tbm" : "shop"
	}
)

soup = BeautifulSoup(response.text, "html5lib")

#quantidade de resultados
#soup_results = soup.find_all("div", {"class": "sh-dgr__gr-auto sh-dgr__grid-result"})

soup_ads = soup.find_all("a", {"class": "shntl sh-np__click-target"})
i = len(soup_ads)

titulo = []
loja = []
preco = []

# >>> codigo para anuncios sem serem patrocinados
#for i in range(0,10):
#	titulo.append(soup_results[i].find("h3").get_text())
#	loja.append(soup_results[i].find("div", {"class" : "aULzUe IuHnof"}).get_text().split('}')[-1:])
#	preco.append(soup_results[i].find("span", {"class" : "a8Pemb OFFNJ"}).get_text())

# anuncios patrocinados
for i in range(0,i):
	titulo.append(soup_ads[i].find("h3", {"class" : "sh-np__product-title translate-content"}).get_text())
	loja.append(soup_ads[i].find("span", {"class" : "E5ocAb"}).get_text().split('}')[-1:])
	preco.append(soup_ads[i].find("b", {"class" : "translate-content"}).get_text())

df = list(zip(titulo,loja, preco))
df = pd.DataFrame(df, columns = ['Produto', 'Loja', 'Preço'])


st.dataframe(df, width=700, height=300)

st.markdown('---')

st.header('Chat GPT recomenda para o melhor custo benefício:')


openai.api_key = st.secrets['minha_chave']

completion = openai.ChatCompletion.create (
	model = 'gpt-3.5-turbo',
	messages = [
		{'role':'user', 'content': f'O dataset a seguir indica o preço de um produto em várias lojas, sendo que as quantidades podem variar. Assim, calcule qual tem o menor valor unitário e indique para mim somente o item, preço e loja com melhor custo beneficio. Não precisa demonstrar o calculo {df}'}
	]
)

st.markdown(completion['choices'][0]['message']['content'])