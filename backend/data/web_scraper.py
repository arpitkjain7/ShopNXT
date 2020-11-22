import os
import time
import difflib
import logging
import xlsxwriter
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

count = 0


def store_data(product_objects):
    path_to_save = os.path.join(
        os.getcwd(), "data", "collected_data", f"Data_{count}.json"
    )
    file = os.open(path_to_save, "w+")
    file.write(json.dumps(product_objects))
    file.close()


def Extract_Data(url: str, category: str, headless=False):

    if headless:
        options = Options()
        options.add_argument("--headless")
        print(os.path.join(os.getcwd(), "chromedriver"))
        driver = webdriver.Chrome(
            os.path.join(os.getcwd(), "utils", "chromedriver"), chrome_options=options,
        )
    else:
        print(os.path.join(os.getcwd(), "utils", "chromedriver"))
        driver = webdriver.Chrome(os.path.join(os.getcwd(), "utils", "chromedriver"))
    # driver.set_page_load_timeout(20)
    # driver.fullscreen_window()
    # driver.set_script_timeout(10)
    driver.get(url)
    logging.info("Logging into Target Environment")
    # accepting cookies
    shop_by_cat = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()=' Shop by Category ']"))
    )
    shop_by_cat.send_keys("\n")
    item1 = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//ul[@id='navBarMegaNav']//following::a[text()='{category}']",)
        )
    )
    item1.send_keys("\n")
    master_data = []
    item_present = True
    n = 1
    # driver.implicitly_wait(200)

    time.sleep(10)
    while item_present:
        prod_elem = driver.find_elements_by_xpath(
            f"//div[@class='items']//div[@qa='product'][{n}]"
        )
        if len(prod_elem) > 0:
            prod_brand_elem = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//div[@class='items']//div[@qa='product'][{n}]//div[@qa='product_name']//h6",
                    )
                )
            )
            prod_brand = prod_brand_elem.text
            prod_name_xpath = f"//div[@class='items']//div[@qa='product'][{n}]//div[@qa='product_name']//a"
            prod_name_elem = driver.find_element_by_xpath(prod_name_xpath)
            prod_name = prod_name_elem.text
            combo_list = driver.find_elements_by_xpath(
                f"//div[@class='items']//div[@qa='product'][{n}]//div[@class='col-sm-12 col-xs-7 qnty-selection']//div//span//ul"
            )
            print(f"combo_list: {combo_list}")
            combo = []
            if len(combo_list) > 0:
                m = 1
                combo_elem = driver.find_element_by_xpath(
                    f"//div[@class='items']//div[@qa='product'][{n}]//div[@class='col-sm-12 col-xs-7 qnty-selection']//div//span//ul"
                )
                num_of_combo = len(combo_elem.find_elements(By.TAG_NAME, "li"))
                print(f"num_of_combo: {num_of_combo}")
                while m <= num_of_combo:
                    quant_xpath = f"//div[@class='items']//div[@qa='product'][{n}]//div[@class='col-sm-12 col-xs-7 qnty-selection']//div//span//ul//li[{m}]//a//span[@ng-bind='allProducts.w']"
                    quant_elem = driver.find_element_by_xpath(quant_xpath)
                    quantity = quant_elem.get_attribute("innerHTML")
                    price_xpath = f"//div[@class='items']//div[@qa='product'][{n}]//div[@class='col-sm-12 col-xs-7 qnty-selection']//div//span//ul//li[{m}]//a//span[@ng-bind='allProducts.sp']"
                    price_elem = driver.find_element_by_xpath(price_xpath)
                    price = price_elem.get_attribute("innerHTML")
                    combo.append((quantity, price))
                    m += 1
            product_details = {
                "category": category,
                "product_name": prod_name,
                "product_brand": prod_brand,
                "combo": combo,
            }
            print(f"product_details: {product_details}")
            master_data.append(product_details)
            n += 1
            if n % 500 == 0:
                store_data(product_objects=master_data)
                master_data = []
            html = driver.find_element_by_tag_name("html")
            html.send_keys(Keys.PAGE_DOWN)
        else:
            show_more = driver.find_elements_by_xpath("//button[text()='Show More']")
            if len(show_more) > 0:
                show_more_button = driver.find_element_by_xpath(
                    "//button[text()='Show More']"
                )
                show_more_button.send_keys("\n")
            else:
                item_present = False
                print("No more items to extract")
    # except Exception as error:
    #     print("error")
    #     item_present = False
    # if n % 15 == 0:
    #     show_more = WebDriverWait(driver, 100).until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[text()='Show More']",))
    #     )
    #     show_more.send_keys("\n")
    # html = driver.find_element_by_tag_name("html")
    # html.send_keys(Keys.PAGE_DOWN)
    # except Exception as error:
    #     print(error)
    #     print("No more items to extract")
    #     item_present = False
    print(f"master_data: {master_data}")
    return master_data
    driver.close()


def scrape_wrapper(category: str):
    url = "https://www.bigbasket.com/"
    data = Extract_Data(url=url, category=category)
    return data
