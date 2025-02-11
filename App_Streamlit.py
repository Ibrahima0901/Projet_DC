import scrapy
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scrapy.crawler import CrawlerProcess

# URLs des catégories
URLS = {
    "Computers": "https://www.expat-dakar.com/ordinateurs?page=",
    "Telephones": "https://www.expat-dakar.com/telephones?page=",
    "Cinema": "https://www.expat-dakar.com/cinema?page="
}

# Classe Scrapy pour le scraping
class ExpatDakarSpider(scrapy.Spider):
    name = "expat_dakar"
    start_urls = []
    data = []

    def __init__(self, category, pages, *args, **kwargs):
        super(ExpatDakarSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.pages = pages
        self.start_urls = [f"{URLS[self.category]}{page}" for page in range(1, self.pages + 1)]

    def parse(self, response):
        containers = response.css('.listings-cards__list-item')
        for container in containers:
            try:
                details = container.css('.listing-card__header__title::text').get().strip()
                etat = container.css('.listing-card__header__tags__item--condition_new::text').get().strip()
                marque = container.css('.listing-card__header__tags::text').get().strip().replace(etat, '')
                adresse = ' '.join(container.css('.listing-card__header__location::text').get().split()).replace(',', '')
                prix = container.css('.listing-card__price::text').get().strip().replace('F Cfa','').replace(' ','')
                image_lien = container.css('.listing-card__image__resource.vh-img::attr(src)').get()

                dic = {
                    'details': details,
                    'etat': etat,
                    'marque': marque,
                    'prix': prix,
                    "adresse": adresse,
                    "lien image": image_lien
                }
                self.data.append(dic)
            except:
                pass

    def close(self, reason):
        # Enregistrer les données dans un fichier CSV une fois le scraping terminé
        df = pd.DataFrame(self.data)
        df.to_csv(f"data_{self.category}.csv", index=False)


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
