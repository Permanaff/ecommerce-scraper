#you tube comments on  you tube orignal Ai series.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import pandas as pd

driver=webdriver.Chrome()
driver.set_page_load_timeout(60)
driver.get('https://www.tokopedia.com/')
driver.maximize_window()
sleep(5)
search=driver.find_element(By.XPATH,"""//*[@id="header-main-wrapper"]/div[2]/div[2]/div/div/div/div/input""")
search.clear()
search.send_keys('sandisk')

search.send_keys(Keys.ENTER)
sleep(5)
for i in range(8):
    driver.execute_script("window.scrollBy(0,700)","")
    sleep(2)
sleep(10)
container_element = driver.find_element(By.CLASS_NAME,'css\\-rjanld')
driver.execute_script("arguments[0].scrollIntoView();", container_element)


pagination = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, './/*[@id="zeus-root"]/div/div[2]/div/div[2]/div[5]/nav'))
)
pages = pagination.find_element(By.XPATH, './/ul[contains(@class, "css-1ni9y5x-unf-pagination-items")]')
page_items = pages.find_elements(By.TAG_NAME, 'li')
last_page = int(page_items[-2].text.replace('.', ''))
# if last_page >= 20 : 
#     last_page = 20

last_page = 5

print(last_page)


# sleep(10)
title_product = []
product_price = []
seller_product = []
product_sell = []
product_image = []
print('a')
current_page = 1


while current_page <= last_page:
    sleep(5)
    products = driver.find_elements(By.CLASS_NAME, "css-5wh65g")

    for product in products:
        try : 
            title = product.find_element(By.CLASS_NAME, 'OWkG6oHwAppMn1hIBsC3pQ\\=\\=').text
        except NoSuchElementException:
            title = None
        title_product.append(title)

        # price_elemen = product.find_element(By.CLASS_NAME, 'ELhJqP-Bfiud3i5eBR8NWg==')

        try:
            # Mencoba menemukan elemen pertama
            price = product.find_element(By.CLASS_NAME, '_8cR53N0JqdRc\\+mQCckhS0g\\=\\=').text
        except NoSuchElementException:
            try:
                # Jika elemen pertama tidak ditemukan, coba elemen alternatif
                price = product.find_element(By.CLASS_NAME, 'gJHohDcsji\\+TjH4Kkc9LEw\\=\\=').text
            except NoSuchElementException:
                # Tangani kasus jika elemen juga tidak ditemukan
                price = None
        product_price.append(price)

        
        try:
            # Mencoba menemukan elemen pertama
            sell = product.find_element(By.CLASS_NAME, 'eLOomHl6J3IWAcdRU8M08A\\=\\=').text
        except NoSuchElementException:
            sell = None
        product_sell.append(sell)

        try:
            image = product.find_element(By.CLASS_NAME, 'css\\-1c345mg').get_attribute('src')
        except NoSuchElementException:
            image = None
        product_image.append(image)

        try:
            seller = product.find_element(By.CLASS_NAME, 'X6c\\-fdwuofj6zGvLKVUaNQ\\=\\=').text

            if seller == 'Dilayani Tokopedia' : 
                try:
                    seller = product.find_element(By.XPATH, '//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[4]/div[1]/div[8]/a/div[1]/div[2]/div[4]/div[2]/span[2]').get_attribute('src')
                except NoSuchElementException:
                    seller = None

        except NoSuchElementException:
            seller = None

        seller_product.append(seller)
        

        driver.execute_script(f"console.log('{title}');")
        print(f"{title}\n{price}\n{sell}\n{image}\n--------------------")

    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, './/button[contains(@class, "css-16uzo3v-unf-pagination-item")][@aria-label="Laman berikutnya"]')
        if next_page.is_enabled():
            next_page.click()
        else:
            break
    except NoSuchElementException:
        break


df=pd.DataFrame({"title":title_product, 'harga' : product_price, 'terjual' : product_sell, 'seller' : seller_product})
df.to_csv("sandisk_product_tokopedia.csv",index=False)
assert "No results found." not in driver.page_source
driver.close()