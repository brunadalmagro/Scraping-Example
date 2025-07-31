from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import re 
import locale
import time

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Configurações do Firefox
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
service = Service(r'C:\geckodriver-v0.36.0-win32\geckodriver.exe')

# --- Scraping Mercado Livre PRIMEIRO ---
ml_link = "https://lista.mercadolivre.com.br/mesas"
driver = webdriver.Firefox(service=service, options=firefox_options)
driver.get(ml_link)

# Espera explícita para carregar os elementos
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-search-item__title")))
except:
    print("Elementos não carregaram a tempo")

# Rolagem para carregar mais itens (opcional)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

html_ml = driver.page_source
soup_ml = BeautifulSoup(html_ml, 'html.parser')

# Extração correta dos dados
produtos_ml = []
for item in soup_ml.find_all('li', class_='ui-search-layout__item'):
    # Nome do produto
    title = item.find('h2', class_='ui-search-item__title')
    nome = title.text.strip() if title else 'Sem título'
    
    # Preço
    price = item.find('span', class_='andes-money-amount__fraction')
    cents = item.find('span', class_='andes-money-amount__cents')
    
    preco = ''
    if price:
        preco = price.text.strip()
        if cents:
            preco += ',' + cents.text.strip()
    
    # Link
    link = item.find('a', class_='ui-search-link')
    link_url = link['href'] if link else ''
    
    produtos_ml.append({
        'nome_produto_ml': nome,
        'preco_formatado_ml': f"R$ {preco}" if preco else 'Preço não disponível',
        'link_ml': link_url
    })

driver.quit()

# --- Scraping OLX --- (mantive seu código original com pequenos ajustes)
driver = webdriver.Firefox(service=service, options=firefox_options)
driver.get("https://www.olx.com.br/brasil?q=mesas")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "olx-adcard__content")))
except:
    print("Elementos OLX não carregaram a tempo")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

produtos = []
for card in soup.find_all('div', class_='olx-adcard__content'):
    titulo = card.find('h2')
    titulo_text = titulo.get_text(strip=True) if titulo else ''
    
    preco = card.find('h3')
    preco_text = preco.get_text(strip=True) if preco else ''
    preco_num = re.sub(r'[^\d]', '', preco_text)
    preco_num = int(preco_num) if preco_num else 0
    preco_formatado = formatar_moeda(preco_num) if preco_num else 'R$ 0,00'
    
    link_tag = card.find('a')
    link_produto = link_tag['href'] if link_tag else ''
    
    produtos.append({
        'nome_produto': titulo_text,
        'preco_formatado': preco_formatado,
        'link_produto': link_produto
    })

driver.quit()

# Exibindo resultados
print("\n" + "-"*60)
print("RESULTADOS OLX")
print("-"*60)
print(pd.DataFrame(produtos).head())

print("\n" + "-"*60)
print("RESULTADOS MERCADO LIVRE")
print("-"*60)
print(pd.DataFrame(produtos_ml).head())

# Salvando em CSV
pd.DataFrame(produtos).to_csv('csv-files/olx_mesas.csv', index=False, encoding='utf-8-sig')
pd.DataFrame(produtos_ml).to_csv('csv-files/mercado_livre_mesas.csv', index=False, encoding='utf-8-sig')