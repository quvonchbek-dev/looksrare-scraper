from bs4 import BeautifulSoup
import json
import time

base_url = "https://looksrare.org/"

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
    json.dump(data, open("data.json", "w"), indent=4)
    print(f"Data is written to data.json in {time.time()-start_time}")


if __name__ == "__main__":
    soup = BeautifulSoup(open("html\data.html", "r").read(), "html.parser")
