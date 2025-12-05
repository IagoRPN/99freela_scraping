from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

debug = False


class Scrapper():

    def __init__(self):
        if not debug:
            self.options = Options()
            self.options.add_argument("--headless")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 5)
        
        self.page = 1

    def search_keyword(self, keyword: str):
        self.keyword = keyword
        self.keyword_encoded = keyword.replace(" ", "%20")
        self.base_url = f"https://www.99freelas.com.br/projects?q={self.keyword_encoded}"

    def scrape_projects(self):
        output_data = []
        while True:
            try:
                #second: selects the project type filter
                if self.page == 1:
                    url = f"{self.base_url}"
                else:
                    url = f"{self.base_url}&page={self.page}"
                self.driver.get(url)
                #print(f"APP_MSG: Navigated to URL with keyword filter: {driver.current_url}")


                projects_div = self.driver.find_element(By.CLASS_NAME, "projects-result")
                projects_list = projects_div.find_elements(By.TAG_NAME, "li")
                #print(f"APP_MSG: Found {len(projects_list)} projects on page {page}.")        

                if projects_list == []:
                    #print("APP_MSG: No more projects found. Exiting loop.")
                    break

                for project in projects_list:
                    project_title = project.find_element(By.CLASS_NAME, "title").text
                    project_link = project.find_element(By.TAG_NAME, "a").get_attribute("href")
                    self.driver.get(project_link)
                    project_description = self.driver.find_element(By.CSS_SELECTOR, ".item-text.project-description.formatted-text").text.replace("\n", " ").replace(",", " - ")
                    self.driver.back()
                    
                    if debug:
                        print(project_title, project_link, project_description)
                        
                    data = json.dumps({
                        "keyword": self.keyword,
                        "title": project_title,
                        "link": project_link,
                        "description": project_description
                    }, ensure_ascii=False)
                    output_data.append(data)
                
                self.page += 1
            except NoSuchWindowException:
                print("Browser window was closed. Exiting loop.")
            except Exception as e:
                print(f"An error occurred: {e}. Exiting loop.")
                break

        return output_data        
        self.driver.quit()