from tools.scraper import scrape, write_as_json

soup = scrape()
write_as_json(soup)
