from tools.scraper import scrape, write_as_json, write_as_csv

print("Hi, this is Looksrare collections scraper!")
to_csv = (
    input(
        "The scraped data will write to data/data.json.\n\nDo you want to write it to csv file? [y] or [n]\n"
    )
    == "y"
)

save_html = input("Do you want to save html file also? [y] or [n]\n") == "y"
soup = scrape(save_html)

if to_csv:
    write_as_csv(soup)
else:
    write_as_json(soup)

print("THANK YOU!")
