from tools.scraper import scrape, write_as_json, write_as_csv

print("Hi, this is Looksrare collections scraper!")
to_csv = input(
    "The scraped data will write to data/data.json.\n\n"
    "Do you want to write it to csv file? [y] or [n]\n"
)
soup = scrape()
if to_csv == "y":
    write_as_csv(soup)
else:
    write_as_json(soup)
print("THANK YOU!")