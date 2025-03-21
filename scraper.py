from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


url = "https://www.ebay.com/globaldeals/tech#r0_i0"
def scrape(): 
    driver = setup_driver()
    driver.get(url)

    # scroll to bottom 
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")    
        if new_height == prev_height: 
            break      
        prev_height = new_height

    products = driver.find_elements(By.XPATH, '//*[@itemscope="itemscope"]')
    all_products=[]
    for product in products:
        try:
            title = product.find_element(By.XPATH, './/span[@itemprop="name"]').text
            price = product.find_element(By.XPATH, './/*[@itemprop="price"]').text
            try:
                original_price = product.find_element(By.XPATH, './/*[@class="dne-itemtile-original-price"]').text
            except:
                original_price = price
            product_url = product.find_element(By.XPATH, './/*[@itemprop="url"]').get_attribute("href")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_products.append({"title":title, "price":price, "original price":original_price, "url": product_url, "timestamp":timestamp})
        except:
            continue

    driver.quit()
    return all_products

def save_to_csv(data):
    file_name = "ebay_tech_deals.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["title", "price", "original price", "url", "timestamp"])
    df_new = pd.DataFrame(data)
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_csv(file_name, index=False)


if __name__ == '__main__':
    products = scrape()
    if products:
        save_to_csv(products)