import os
import time
import difflib
import logging
import xlsxwriter
import pandas as pd
import json
import urllib
import uuid
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


def store_data(product_objects, category, sub_category):
    path_to_save = os.path.join(
        os.getcwd(),
        "data",
        "collected_data",
        "json",
        f"Data_{category}_{sub_category}.json",
    )
    file = open(path_to_save, "w")
    file.write(json.dumps(product_objects))
    file.close()


def save_product_images(image_obj, image_path):
    file = open(image_path, "wb")
    shutil.copyfileobj(image_obj.raw, file)
    file.close()


def generate_product_id():
    timestamp = str(int(datetime.now().timestamp()))
    unique_id = str(int(uuid.uuid1()) % 100000)
    return f"{timestamp}_{unique_id}"


def Extract_Data(url: str, category: [], headless=False):

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
    driver.get(url)
    logging.info("Logging into Target Environment")

    # shop_by_cat = WebDriverWait(driver, 100).until(
    #     EC.element_to_be_clickable((By.XPATH, "//a[text()=' Shop by Category ']"))
    # )
    # shop_by_cat.send_keys("\n")
    # item1 = WebDriverWait(driver, 100).until(
    #     EC.element_to_be_clickable(
    #         (By.XPATH, f"//ul[@id='navBarMegaNav']//following::a[text()='View All']",)
    #     )
    # )
    # item1.send_keys("\n")
    # category_element = WebDriverWait(driver, 100).until(
    #     EC.element_to_be_clickable((By.XPATH, f"//a[text()='{category}']",))
    # )
    sub_category_list = driver.find_elements_by_xpath(
        f"//a[text()='{category}']//following::ul[1]//li"
    )
    print(f"length of sub category : {len(sub_category_list)}")
    # base_url = driver.current_url
    print(f"base_url : {url}")
    sub_count = 0
    while sub_count < len(sub_category_list):
        if sub_count > 0:
            print("navigating back")
            driver.get(url)
            time.sleep(5)
        sub_count += 1
        sub_category = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//a[text()='{category}']//following::ul[1]//li[{sub_count}]//a",
                )
            )
        )
        sub_category_name = sub_category.text
        print(f"sub_category_name: {sub_category_name}")
        if sub_category_name not in ("Snacks, Dry Fruits, Nuts", "Oils & Vinegar"):
            sub_category.send_keys("\n")
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
                    product_id = generate_product_id()
                    prod_img_elem = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                f"//div[@class='items']//div[@qa='product'][{n}]//img",
                            )
                        )
                    )
                    img = prod_img_elem.get_attribute("src")
                    img_path = os.path.join(
                        os.getcwd(),
                        "data",
                        "collected_data",
                        "images",
                        f"{category}",
                        f"{sub_category_name}",
                    )
                    os.makedirs(img_path, exist_ok=True)
                    img_obj = requests.get(url=img, stream=True)
                    save_product_images(
                        image_obj=img_obj,
                        image_path=os.path.join(img_path, f"{product_id}.jpg",),
                    )
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
                    combo = []
                    if len(combo_list) > 0:
                        m = 1
                        combo_elem = driver.find_element_by_xpath(
                            f"//div[@class='items']//div[@qa='product'][{n}]//div[@class='col-sm-12 col-xs-7 qnty-selection']//div//span//ul"
                        )
                        num_of_combo = len(combo_elem.find_elements(By.TAG_NAME, "li"))
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
                        "product_id": product_id,
                        "category": category,
                        "sub_category_name": sub_category_name,
                        "product_name": prod_name,
                        "product_brand": prod_brand,
                        "img_src": img,
                        "combo": combo,
                    }
                    print(f"product_details: {product_details}")
                    master_data.append(product_details)
                    n += 1
                    print(n)
                    if n % 200 == 0:
                        print("file created")
                        store_data(
                            product_objects=master_data,
                            category=category,
                            sub_category=sub_category_name,
                        )
                        master_data = []
                        break
                    html = driver.find_element_by_tag_name("html")
                    html.send_keys(Keys.PAGE_DOWN)
                else:
                    try:
                        show_more_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[text()='Show More']",)
                            )
                        )
                        show_more_button.send_keys("\n")
                    except Exception as error:
                        store_data(
                            product_objects=master_data,
                            category=category,
                            sub_category=sub_category_name,
                        )
                        print(f"error: {error}")
                        master_data = []
                        break
    driver.close()
    return "category extraction complete"


def scrape_wrapper(category: str):
    url = "https://www.bigbasket.com/product/all-categories/"
    status = Extract_Data(url=url, category=category)
    return status
