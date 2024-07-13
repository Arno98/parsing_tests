import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        # Налаштування параметрів для браузера Chrome
        options = Options()
        options.add_argument("--headless")  # Запуск в headless режимі (без графічного інтерфейсу)
        options.add_argument("--disable-gpu")  # Вимкнення GPU для сумісності
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')  # Встановлення user-agent
        options.add_argument("--window-size=1920x1200")  # Встановлення розміру вікна
        options.add_argument("--log-level=3")  # Встановлення рівня логування
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Вимкнення деяких логів
        return webdriver.Chrome(options=options)

    def fetch_data(self):
        # Відкриття сторінки та очікування її завантаження
        self.driver.get(self.url)
        WebDriverWait(self.driver, 5).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    def parse_data(self, soup):
        data = {}

        # Назва товару
        title_element = soup.find('h1', {'class': 'x-item-title__mainTitle'})
        data['title'] = title_element.get_text(strip=True) if title_element else 'N/A'

        # Посилання на фото
        image_elements = soup.find_all('div', {'class': 'ux-image-carousel-item'})
        data['image_urls'] = [img['src'] for img in [el.find('img') for el in image_elements] if img and 'src' in img.attrs]

        # Посилання на товар
        data['product_url'] = self.url

        # Ціна
        price_element = soup.find('div', {'class': 'x-price-primary'})
        data['price'] = price_element.get_text(strip=True) if price_element else 'N/A'

        # Продавець
        seller_element = soup.find('div', {'class': 'x-sellercard-atf__info__about-seller'})
        data['seller'] = seller_element.get('title', 'N/A') if seller_element else 'N/A'

        # Ціна доставки
        shipping_table = soup.find('table', {'class': 'ux-table-section ux-table-section--html-table ux-table-section-with-hints--shippingTable'})
        if shipping_table:
            first_td = shipping_table.find('td', {'data-testid': 'ux-table-section-body-cell'})
            if first_td:
                first_span = first_td.find('span', {'class': 'ux-textspans'})
                if first_span:
                    shipping_cost = first_span.get_text(strip=True)
        data['shipping_cost'] = shipping_cost

        return data

    def save_data(self, data, filename='ebay_product.json'):
        # Збереження даних у файл у форматі JSON
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def run(self):
        # Основний метод для запуску всіх процесів
        soup = self.fetch_data()
        data = self.parse_data(soup)
        self.save_data(data)
        print(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # URL товару на eBay
    url = "https://www.ebay.com/itm/175287415197?itmmeta=01J2PBNHXTQN3QY43M9PMG0V0Z&hash=item28cff1b19d:g:4MYAAOSweC1h3Dyg"
    scraper = EbayScraper(url)
    scraper.run()
