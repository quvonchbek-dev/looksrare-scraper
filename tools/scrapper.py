from selenium import webdriver

driver = webdriver.Chrome("F:\TeleBOT\looksrare_api\drivers\chromedriver.exe")
url = "https://looksrare.org/collections"
driver.get(url)
print(driver.get_network_conditions())
for i in range(50):
    pass