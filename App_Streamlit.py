import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer
from twisted.internet import reactor

class ExpatsDakarSpider(scrapy.Spider):
    name = 'expats_dakar'

    def start_requests(self):
        categories = {
            "Computers": "https://www.expat-dakar.com/ordinateurs?page=",
            "Telephones": "https://www.expat-dakar.com/telephones?page=",
            "Cinema": "https://www.expat-dakar.com/cinema?page="
        }

        for category, url in categories.items():
            for page in range(1, 6):  # Suppose we want to scrape the first 5 pages of each category
                yield scrapy.Request(url=f"{url}{page}", callback=self.parse, meta={'category': category})

    def parse(self, response):
        data = []
        category = response.meta['category']

        containers = response.css(".listings-cards__list-item")
        for container in containers:
            try:
                details = container.css('.listing-card__header__title::text').get().strip()
                etat = container.css(".listing-card__header__tags__item--condition_new::text").get().strip()
                marque = container.css(".listing-card__header__tags::text").get().strip().replace(etat, '')
                adresse = ' '.join(container.css('.listing-card__header__location::text').get().split())
                prix = container.css(".listing-card__price::text").get().strip().replace('F Cfa', '').replace(' ', '')
                image_lien = container.css(".listing-card__image__resource.vh-img::attr(src)").get()

                dic = {
                    'category': category,
                    'details': details,
                    'etat': etat,
                    'marque': marque,
                    'prix': prix,
                    "adresse": adresse,
                    "lien image": image_lien
                }
                
                data.append(dic)
            except Exception as e:
                self.logger.error(f"Error parsing container: {e}")

        yield from data

        # Suivi des pages suivantes (pagination)
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={'category': category})

# Initialisation du CrawlerRunner
runner = CrawlerRunner(get_project_settings())

# Démarrer le crawling
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ExpatsDakarSpider)

# Exécution du crawler sans interférer avec Streamlit
crawl().addCallback(lambda _: reactor.stop())
reactor.run()




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
