from scrapper_handler import Scrapper
from file_output_handler import FileHandler


scrapper = Scrapper()
file  = FileHandler("projects.csv")
keyword_list = ["web scraping", "python", "automação"]

for keyword in keyword_list:
    print(f"APP_MSG: Starting scraping for keyword: {keyword}")
    scrapper.search_keyword(keyword)
    result = scrapper.scrape_projects()
    print(f"APP_MSG: Scraping completed. Total projects found: {len(result)}")
    file.save_to_file(result)