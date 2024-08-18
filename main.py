#you tube comments on  you tube orignal Ai series.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import pandas as pd
from datetime import datetime


driver=webdriver.Chrome()
driver.set_page_load_timeout(60)
driver.get('https://www.tokopedia.com/')
driver.maximize_window()
sleep(5)
search=driver.find_element(By.XPATH,"""//*[@id="header-main-wrapper"]/div[2]/div[2]/div/div/div/div/input""")
search.clear()
search.send_keys('laptop lenovo')

search.send_keys(Keys.ENTER)
sleep(5)
for i in range(8):
    driver.execute_script("window.scrollBy(0,700)","")
    sleep(2)
sleep(5)
container_element = driver.find_element(By.CLASS_NAME,'css\\-rjanld')
driver.execute_script("arguments[0].scrollIntoView();", container_element)


pagination = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, './/*[@id="zeus-root"]/div/div[2]/div/div[2]/div[5]/nav'))
)
pages = pagination.find_element(By.XPATH, './/ul[contains(@class, "css-1ni9y5x-unf-pagination-items")]')
page_items = pages.find_elements(By.TAG_NAME, 'li')
last_page = int(page_items[-2].text.replace('.', ''))
if last_page >= 10 : 
    last_page = 10

# sleep(10)
title_product = []
product_price = []
seller_product = []
product_sell = []
product_image = []
current_page = 1


while current_page <= last_page:
    sleep(5)
    products = driver.find_elements(By.CLASS_NAME, "css-5wh65g")

    for product in products:
        try : 
            title = product.find_element(By.CLASS_NAME, 'OWkG6oHwAppMn1hIBsC3pQ\\=\\=').text
        except NoSuchElementException:
            title = None

        try : 
            title = title.replace(",", " ")
        except NoSuchElementException:
            title = title
        title_product.append(title)

        try:
            price = product.find_element(By.CLASS_NAME, '_8cR53N0JqdRc\\+mQCckhS0g\\=\\=').text
        except NoSuchElementException:
            try:
                price = product.find_element(By.CLASS_NAME, 'gJHohDcsji\\+TjH4Kkc9LEw\\=\\=').text
            except NoSuchElementException:
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

        
        print(f"{title}\n{price}\n{sell}\n{image}\n--------------------")

        try : 
            escaped_title = title.replace("'", "\\'").replace('"', '\\"')
        except NoSuchElementException:
            escaped_title = title

        # if "'" in title or '"' in title:
        #     escaped_title = title.replace("'", "\\'").replace('"', '\\"')
        
        driver.execute_script(f'console.log(`{escaped_title}`);')

    driver.execute_script(f'console.log(">>>>> Data Terambil :  {len(title_product)} <<<<<");')
    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, './/button[contains(@class, "css-16uzo3v-unf-pagination-item")][@aria-label="Laman berikutnya"]')
        if next_page.is_enabled():
            next_page.click()
            driver.execute_script(f'console.log(">>>>> HALAMAN {current_page} <<<<<");')
        else:
            break
    except NoSuchElementException:
        break


time = datetime.now().strftime("%y%m%d%H%M%S")

df=pd.DataFrame({"title":title_product, 'harga' : product_price, 'terjual' : product_sell, 'seller' : seller_product})
df.to_csv(f"product_{time}.csv",index=False)
assert "No results found." not in driver.page_source
driver.close()