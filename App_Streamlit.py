import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

URLS = {
    "Computers": "https://www.expat-dakar.com/ordinateurs?page=",
    "Telephones": "https://www.expat-dakar.com/telephones?page=",
    "Cinema": "https://www.expat-dakar.com/cinema?page="
}

data = []
def scrape_expats_dakar(category, pages)
    for category, base_url in URLS.items():
        try:
            for p in range(1, pages+1):
                url = f"{base_url}{p}"
                time.sleep(5)
                response = requests.get(url)
                Page_source = response.content
                soup = bs(Page_source, 'html.parser')
                infos = soup.find_all('div', class_='listings-cards__list-item')
                for info in infos:
                    try:
                        # Détails de l'annonce
                        details = info.find('div', class_='listing-card__header__title').text.strip()
                        # État de l'annonce
                        etat = info.find('span', class_='listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_new').text.strip()
                        # Marque de l'annonce
                        marque = info.find('div', class_='listing-card__header__tags').text.strip().replace(etat,'')
                        # Prix
                        prix = info.find('span', class_='listing-card__price__deal').text.strip().replace('F Cfa','').replace(' ','')
                        # Adresse
                        adresse = ' '.join(info.find('div', class_="listing-card__header__location").text.strip().split()).replace(',', '')
                        # Lien de l'image
                        image_lien = info.find('img', class_='listing-card__image__resource vh-img')['src']
                        dic = {'category': category, 'details': details, 'etat': etat, 'marque': marque, 'prix': prix, 'adresse': adresse, 'image_lien': image_lien}
                        data.append(dic)
                    except Exception as e:
                        print(f"Erreur lors du scraping : {e}")
                        pass
        finally:
              response.quit()
        return pd.DataFrame(data)
        
# Interface Streamlit
st.markdown("<h1 style='text-align: center; color: black;'>MY DATA SCRAPER APP</h1>", unsafe_allow_html=True)
st.markdown("This app scrapes and downloads data from Expat-Dakar.")

st.sidebar.markdown("**User Input Features**")
pages = st.sidebar.number_input("Number of pages to scrape", min_value=1, value=2)
category = st.sidebar.selectbox(
    "How would you like to scrape",
    ("Scrapy","Dashboard of the data","Fill the form"))

# Ajout des boutons pour chaque catégorie
col1, col2, col3 = st.columns(3)

# Variables pour stocker les données
df_computers = pd.DataFrame()
df_phones = pd.DataFrame()
df_cinema = pd.DataFrame()

if category == "Scrapy":
    with col1:
        if st.button("Scrape Computers"):
            st.write("Scraping **Computers** data... This may take a few minutes.")
            spider = ExpatDakarSpider(category="Computers", pages=pages)
            process = CrawlerProcess()
            process.crawl(spider)
            process.start()
            df_computers = pd.DataFrame(spider.data)
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
            spider = ExpatDakarSpider(category="Telephones", pages=pages)
            process = CrawlerProcess()
            process.crawl(spider)
            process.start()
            df_phones = pd.DataFrame(spider.data)
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
            spider = ExpatDakarSpider(category="Cinema", pages=pages)
            process = CrawlerProcess()
            process.crawl(spider)
            process.start()
            df_cinema = pd.DataFrame(spider.data)
            if not df_cinema.empty:
                st.success(f"Scraped {len(df_cinema)} items!")
                st.dataframe(df_cinema)
                csv_cinema = df_cinema.to_csv(index=False).encode("utf-8")
                st.download_button("Download Cinema Data", csv_cinema, "Cinema_data.csv", "text/csv")
            else:
                st.warning("No data found for Cinema.")

elif category == "Dashboard of the data":
    # Ajouter le code pour afficher les graphiques de données
    pass

elif category == "Fill the form":
    st.page_link("https://ee.kobotoolbox.org/x/OHZQDGcE", label="Google", icon="🌎")
