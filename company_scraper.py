import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import string
import re
import pandas as pd
from tqdm import tqdm

def browser_startup_sequence():
    # start browser
    base_url = "https://www.google.com/maps/"
    path = r'Google_Maps_Scraper/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument("--lang=en_US");
    driver = webdriver.Chrome(path, chrome_options=options)
    driver.maximize_window()
    return driver

def linkedin_login(webdriver, username, password):
    # username
    username_element = webdriver.find_element(By.XPATH, "//input[contains(@id, 'username')]")
    username_element.click()
    username_element.send_keys(username)
    # password
    password_element = webdriver.find_element(By.XPATH, "//input[contains(@id, 'password')]")
    password_element.click()
    password_element.send_keys(password)
    # sign-in button
    sign_in_element = webdriver.find_element(By.XPATH, "//button[contains(@type, 'submit')]")
    sign_in_element.click()

def start_linkedin():
    driver = browser_startup_sequence()
    driver.get("https://www.linkedin.com/login")
    return driver


email = ""
pw = ""
driver = start_linkedin()
linkedin_login(webdriver=driver, username=email, password=pw)

# PART ONE: Extract companies from LinkedIn
company_name_lst, company_url_lst = ([] for i in range(2))
for letter in list(string.ascii_lowercase):
    # customize linkedin url accordingly to your needs
    url = f"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%2290000828%22%5D&companySize=%5B%22B%22%2C%22C%22%2C%22D%22%2C%22E%22%5D&keywords={letter}*&origin=FACETED_SEARCH&sid=fCx"
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_tag = soup.find("ul", {"class": "artdeco-pagination__pages artdeco-pagination__pages--number"})
    page_number = page_tag.find_all("li")[-1].find("span").get_text()
    try:
        for page in range(1,int(page_number)+1):
            time.sleep(random.randint(6, 10))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            companies = soup.find_all("li", {"class": "reusable-search__result-container"})
            for company in companies:
                company_name = company.find("span", {"class": re.compile("entity-result__title-text")}).get_text().replace("\n\n ","").replace("\n\n","")
                company_name_lst.append(company_name)
                company_url = company.find('a', href=True)["href"]
                company_url_lst.append(company_url)
                print(f"Extracting Company Name: {company_name} with url: {company_url}")
            next_element = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Weiter')]")
            next_element.click()
            if page == int(page_number)+1:
                print(f"*** No next button available. Scraping for Letter '{letter}' finished ***")
    except:
        print(f"*** Error. Scraping for Letter '{letter}' finished ***")
        pass
driver.quit()
linkedin_company_df = pd.DataFrame({"Company Name": company_name_lst, "LinkedIn URL": company_url_lst})
linkedin_company_df = linkedin_company_df.drop_duplicates()
linkedin_company_df.to_csv("LinkedIn_Masterdata.csv")

# PART TWO: Extract Company Information in detail
driver = start_linkedin()
linkedin_login(driver)
linkedin_company_df = pd.read_csv("LinkedIn_Masterdata.csv", index_col=0)

company_name_lst, company_url_lst, company_employee_count_lst, company_location_lst, company_employees_linkedin_lst = ([] for i in range(5))
for index, row in tqdm(linkedin_company_df.iterrows()):
    company_name = row["Company Name"]
    company_info_url = row["LinkedIn URL"] + "about"
    driver.get(company_info_url)
    time.sleep(random.randint(3, 7))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    info_body = soup.find("dl",  {"class": "overflow-hidden"})
    for tag in info_body.find_all("dd"):
        if "Beschäftigte" in tag.text.replace("\n            ", "").replace("\n        ", ""):
            employee_count = tag.text.replace("\n            ", "").replace("\n        ", "")
    try:
        location_body = soup.select('div[class*="org-location-card"]')[0]
        location = location_body.find("p").text.replace("\n    ", "").replace("\n  ", "")
    except:
        location = "Several locations available"
    company_linkedin_employee_url = row["LinkedIn URL"] + "people"
    driver.get(company_linkedin_employee_url)
    time.sleep(random.randint(2, 4))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        people_info = soup.find("div", {"class": "artdeco-card pb2"})
        for tag in people_info.find_all("h2"):
            if "Beschäftigte" in tag.text.replace("\n          ", "").replace("\n      ", ""):
                linkedin_employees = tag.text.replace("\n          ", "").replace("\n      ", "").replace(" Beschäftigte", "").replace(".", "")
    except:
        linkedin_employees = 0
    # add all info to lists
    company_name_lst.append(company_name)
    company_url_lst.append(row["LinkedIn URL"])
    company_employee_count_lst.append(employee_count)
    company_location_lst.append(location)
    company_employees_linkedin_lst.append(linkedin_employees)
    print(f"*** Summary --- Name: {company_name}, Employee Count: {employee_count}, Location: {location}, "
          f"Employees on LinkedIn: {linkedin_employees}")

linkedin_company_detailed_df = pd.DataFrame({"Company Name": company_name_lst,
                                             "LinkedIn URL": company_url_lst,
                                             "Employee Range": company_employee_count_lst,
                                             "LinkedIn Employees Listed": company_employees_linkedin_lst,
                                             "Location": company_location_lst})
linkedin_company_detailed_df = linkedin_company_detailed_df.drop_duplicates()
linkedin_company_detailed_df.to_csv("LinkedIn_Masterdata_Detailed.csv")
