from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import time


base_url = "https://looksrare.org/"


def scrape(all=False, save_html=False) -> BeautifulSoup:
    start_time = time.time()

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    driver = webdriver.Chrome(
        "drivers/chromedriver.exe",
        desired_capabilities=capabilities,
    )

    driver.get(base_url + "collections")
    if all:
        driver.find_element(By.CLASS_NAME, "css-xc335k").click()
        time.sleep(1)

    # clicking Load 'More button' 50 times
    for i in range(50):
        try:
            button = driver.find_elements(By.TAG_NAME, "button")[-2]
            button.click()
            print(f"{i+1} st click successful", end="\r")
            time.sleep(4)
        except:
            i -= 1

    elements = driver.find_element(By.CLASS_NAME, "css-1lkdgk4")
    html = elements.get_attribute("innerHTML")
    if save_html:
        with open("html/data.html", "w", encoding="utf-8") as f:
            f.write(html)

    soup = BeautifulSoup(html, "lxml")
    print(f"Data is scraped successful in {time.time() - start_time} seconds")
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
    data["total_vol"] = css_0[3].div.div.text.strip()
    data["owners"] = css_0[4].div.text.strip()
    data["items"] = css_0[5].div.text.strip()
    return data


def write_as_json(soup: BeautifulSoup):
    start_time = time.time()
    list_a = list(soup.find_all("a"))
    data = list(map(get_as_json, list_a))
    json.dump(data, open("data/data.json", "w"), indent=4)
    print(f"Data is written to data.json in {time.time()-start_time} seconds")


if __name__ == "__main__":
    # soup = BeautifulSoup(open("html\data.html", "r").read(), "html.parser")
    scrape(all=False)
