import pandas as pd
import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from webdriver_manager.firefox import GeckoDriverManager
import matplotlib.pyplot as plt
import plotly.express as px

# Initialisation des options du navigateur Selenium pour Firefox
options = Options()
options.add_argument("--headless")  # Mode sans interface graphique
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-gpu")  # Evite certains bugs d'affichage
options.add_argument("--no-sandbox")  # Nécessaire pour exécuter en mode root

# URLs des catégories
URLS = {
    "Computers": "https://www.expat-dakar.com/ordinateurs?page=",
    "Telephones": "https://www.expat-dakar.com/telephones?page=",
    "Cinema": "https://www.expat-dakar.com/cinema?page="
}

# Fonction de scraping
def scrape_expats_dakar(category, pages):
    """Scrape les annonces de la catégorie choisie sur expat-dakar.com"""
    url_base = URLS[category]
    data = []
    
    # Initialisation de Selenium avec Firefox
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    
    try:
        for p in range(1, pages + 1):
            url = f"{url_base}{p}"
            driver.get(url)
            time.sleep(5)  # Pause pour permettre le chargement complet de la page
            
            # Attendre que les annonces soient visibles
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listings-cards__list-item"))
            )
            
            soup = bs(driver.page_source, 'html.parser')
            infos = soup.find_all('div', class_='listings-cards__list-item')

            for info in infos:
                try:
                    details = info.find('div', class_='listing-card__header__title').text.strip()
                    # État de l'annonce
                    etat = info.find('span', class_='listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_new').text.strip()
                    # Marque de l'annonce
                    marque =info.find('div', class_='listing-card__header__tags').text.strip().replace(etat,'')
                    # Prix
                    prix = info.find('span', class_='listing-card__price').text.strip().replace('F Cfa','').replace(' ','')
                    # Adresse
                    adresse = ' '.join(info.find('div', class_="listing-card__header__location").text.strip().split()).replace(',', '')
                    # Lien de l'image
                    image_lien = info.find('img', class_='listing-card__image__resource vh-img')['src']

                    data.append({
                        'details': details,
                        'etat': etat,
                        'marque': marque,
                        'prix': prix,
                        'adresse': adresse,
                        'image_lien': image_lien
                    })

                except Exception as e:
                    print(f"Erreur lors du scraping : {e}")
                    pass
    finally:
        driver.quit()  # Fermer Selenium après exécution

    return pd.DataFrame(data)

# Interface Streamlit
st.markdown("<h1 style='text-align: center; color: black;'>MY DATA SCRAPER APP</h1>", unsafe_allow_html=True) 
st.markdown("This app scrapes and downloads data from Expat-Dakar.")

st.sidebar.markdown("**User Input Features**")
pages = st.sidebar.number_input("Number of pages to scrape", min_value=1, value=2)
category = st.sidebar.selectbox(
    "How would you like to scrape",
    ("Selenium & beautifulSoup","Webscrapper","Dashboard of the data","Fill the form"))

# Ajout des boutons pour chaque catégorie
col1, col2, col3 = st.columns(3)

# Variables pour stocker les données
df_computers = pd.DataFrame()
df_phones = pd.DataFrame()
df_cinema = pd.DataFrame()
if category == "Selenium & beautifulSoup":
    with col1:
        if st.button("Scrape Computers"):
            st.write("Scraping **Computers** data... This may take a few minutes.")
            df_computers = scrape_expats_dakar("Computers", pages)
            if not df_computers.empty:
                st.success(f"Scraped {len(df_computers)} items!")
                st.dataframe(df_computers)
                csv_computers = df_computers.to_csv(index=False).encode("utf-8")
                st.download_button("Download Computers Data", csv_computers, "Computers_data.csv", "text/csv")
            else:
                st.warning("No data found for Computers.")

    with col2:
        if st.button("Scrape Telephones"):
            st.write("Scraping **Telephones** data... This may take a few minutes.")
            df_phones = scrape_expats_dakar("Telephones", pages)
            if not df_phones.empty:
                st.success(f"Scraped {len(df_phones)} items!")
                st.dataframe(df_phones)
                csv_phones = df_phones.to_csv(index=False).encode("utf-8")
                st.download_button("Download Telephones Data", csv_phones, "Telephones_data.csv", "text/csv")
            else:
                st.warning("No data found for Telephones.")

    with col3:
        if st.button("Scrape Cinema"):
            st.write("Scraping **Cinema** data... This may take a few minutes.")
            df_cinema = scrape_expats_dakar("Cinema", pages)
            if not df_cinema.empty:
                st.success(f"Scraped {len(df_cinema)} items!")
                st.dataframe(df_cinema)
                csv_cinema = df_cinema.to_csv(index=False).encode("utf-8")
                st.download_button("Download Cinema Data", csv_cinema, "Cinema_data.csv", "text/csv")
            else:
                st.warning("No data found for Cinema.")
