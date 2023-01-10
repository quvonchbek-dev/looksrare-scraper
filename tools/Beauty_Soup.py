from bs4 import BeautifulSoup

soup = BeautifulSoup(open("data.html", "r").read(), "html.parser")
k = 10
# titles = soup.find_all("span", class_="chakra-text css-n17w0h")
# print(len(titles))
# floors = soup.find_all("div", class_="css-1jahz1o")
# print(len(floors))
a = list(soup.find_all("a"))
row = a[0]
name = row.find_all("span")[-1].text.strip()
css_0 = row.find_all("div", class_="css-0")
floor = css_0[1].div.div.div.text
total_vol = css_0[2].div.div.div.text
print(total_vol)
for i, div in enumerate(a):
    # print(div)
    pass
    # print(i+1, div.text.strip())