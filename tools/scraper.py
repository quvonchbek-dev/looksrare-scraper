from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time
import pandas as pd
from datetime import datetime
from tqdm import tqdm

base_url = "https://looksrare.org/"


def scrape(all=False, save_html=False) -> BeautifulSoup:
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path="drivers/")
    print("[+] Browser is started.")
    driver.get(base_url + "collections")
    if all:
        driver.find_element(By.CLASS_NAME, "css-xc335k").click()
        time.sleep(1)

    print("[+] Starting click 'Load More' button,  50 times")

    for i in tqdm(list(range(50)), "Processing...", colour="#01ffbf"):
        try:
            button = driver.find_elements(By.TAG_NAME, "button")[-2]
            button.click()
            time.sleep(4)
        except:
            i -= 1

    elements = driver.find_element(By.CLASS_NAME, "css-1lkdgk4")
    html = elements.get_attribute("innerHTML")
    if save_html:
        with open("html/data.html", "w", encoding="utf-8") as f:
            f.write(html)

    soup = BeautifulSoup(html, "lxml")
    print(f"[+] Data is scraped successfully.")
    return soup


# rank, name, href, floor, 24h_vol, total_vol, owners, items, offers, image_url
def get_as_json(a: BeautifulSoup):
    css_0 = a.find_all("div", class_="css-0")
    data = {}
    data["rank"] = a.div.div.div.text.strip()
    try:
        name = a.div.div.find_all("span")[2].text.strip()
    except:
        name = a.div.div.find_all("span")[-1].text.strip()
    data["name"] = name
    data["href"] = a["href"]
    try:
        floor = css_0[1].div.div.div.text.strip()
    except:
        floor = "-"
    data["floor"] = floor
    data["_24h_vol"] = css_0[2].div.div.div.text.strip()
    data["total_vol"] = css_0[3].div.div.text.strip().replace(",", ".")
    data["owners"] = css_0[4].div.text.strip()
    data["items"] = css_0[5].div.text.strip().replace(",", ".")
    return data


def write_as_json(soup: BeautifulSoup) -> tuple:
    list_a = list(soup.find_all("a"))
    data = []
    for a in tqdm(list_a, "Processing...", colour="#01ffbf"):
        data.append(get_as_json(a))
    json.dump(data, open("data/data.json", "w"), indent=4)
    print(f"[+] Data is written to data.json")
    return data


def write_as_csv(soup: BeautifulSoup = None):
    if soup:
        write_as_json(soup)
    df = pd.read_json("data/data.json").drop(columns=["href"])
    filename = f"data/{datetime.now().strftime('%Y-%m-%d-%H%M')}.csv"
    df.to_csv(filename, index=False)
    print(f"[+] Data is written to {filename}")
    return True


def write_as_excel(soup: BeautifulSoup = None):
    if soup:
        write_as_json(soup)
    df = pd.read_json("data/data.json").drop(columns=["rank"])
    filename = f"data/{datetime.now().strftime('%Y-%m-%d-%H%M')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"[+] Data is written to {filename}")
    return True


if __name__ == "__main__":
    # soup = BeautifulSoup(open("html\data.html", "r").read(), "html.parser")
    write_as_csv()
    # write_as_excel()
