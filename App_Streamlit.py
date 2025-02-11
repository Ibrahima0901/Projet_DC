import pandas as pd
import streamlit as st
import requests
from requests import get
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt

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
    for p in range(1, pages + 1):
        url = f"{url_base}{p}"
        time.sleep(5)
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        infos = soup.find_all('div', class_='listings-cards__list-item')
    
        for info in infos:
            try:
                details = info.find('div', class_='listing-card__header__title').text.strip()
                # État de l'annonce
                etat = info.find('span', class_='listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_new').text.strip()
                # Marque de l'annonce
                marque = info.find('div', class_='listing-card__header__tags').text.strip().replace(etat,'')
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

elif category == "Webscrapper":
    def load_(dataframe, title, key):
        if st.button(title, key=key):
            st.subheader('Web scraping data')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            
            # Ajouter une option pour choisir le nombre de lignes à afficher
            rows_per_page = st.selectbox('Nombre de lignes par page', options=[10, 20, 50, 100], key=f'rows_per_page_{key}')
            
            # Calculer le nombre total de pages
            total_pages = (len(dataframe) // rows_per_page) + (1 if len(dataframe) % rows_per_page else 0)
            
            # Ajouter une option pour choisir la page à afficher
            page_number = st.number_input('Numéro de page', min_value=1, max_value=total_pages, value=1, key=f'page_number_{key}')
            
            # Calculer les indices de début et de fin pour la pagination
            start_idx = (page_number - 1) * rows_per_page
            end_idx = start_idx + rows_per_page
            
            # Afficher le dataframe paginé
            st.dataframe(dataframe.iloc[start_idx:end_idx])

    # Charger les données
    load_(pd.read_csv('Data/Scrape_Ordinateur_Expat_dakar.csv'), 'Computers data', '1')
    load_(pd.read_csv('Data/Scrape_Telephone_Expat_Dakar.csv'), 'Telephones data', '2')
    load_(pd.read_csv('Data/Scrape_Cinema_Expat_Dakar.csv'), 'Cinema data', '3')

elif category == "Dashboard of the data":
    computer_data = pd.read_csv('Data/Scrape_Ordinateur_Expat_dakar.csv')
    phone_data = pd.read_csv('Data/Scrape_Telephone_Expat_Dakar.csv')
    cinema_data = pd.read_csv('Data/Scrape_Cinema_Expat_Dakar.csv')

    if 'Prix' in computer_data.columns:
        fig, ax = plt.subplots()
        computer_data['Prix'].hist(bins=20, ax=ax)
        ax.set_xlabel("Prix")
        ax.set_ylabel("Nombre")
        ax.set_title("Répartition des prix des ordinateurs")
        st.pyplot(fig)

    if 'Prix' in phone_data.columns:
        st.subheader("📱 Répartition des prix des téléphones")
        fig, ax = plt.subplots()
        phone_data['Prix'].hist(bins=20, ax=ax, color='green', alpha=0.7)
        ax.set_xlabel("Prix (en FCFA)")
        ax.set_ylabel("Nombre d'annonces")
        ax.set_title("Distribution des prix des téléphones")
        st.pyplot(fig)

    if 'Marque' in phone_data.columns:
        st.subheader("🏆 Marques de téléphones les plus vendues")
        top_brands = phone_data['Marque'].value_counts().head(5)
        st.bar_chart(top_brands)

elif category == "Fill the form":
    st.page_link("https://ee.kobotoolbox.org/x/OHZQDGcE", label="Google", icon="🌎")
