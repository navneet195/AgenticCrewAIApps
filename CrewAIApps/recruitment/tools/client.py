import os
import urllib
import selenium
from selenium.webdriver.common.by import By

from .driver import Driver
    
from os import environ as env
from dotenv import load_dotenv
load_dotenv()
linkedin_cookie = env["LINKEDIN_COOKIE"]


class Client:
  def __init__(self):
    url = 'https://linkedin.com/'
    cookie = {
      "name": "li_at",
      "value": linkedin_cookie,
      "domain": ".linkedin.com"
    }

    self.driver = Driver(url, cookie)

  def find_people(self, skills):
    skills = skills.split(",")
    search = " ".join(skills)
    encoded_string = urllib.parse.quote(search.lower())
    url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_string}"
    self.driver.navigate(url)

    people = self.driver.get_elements("ul li div div.linked-area")

    results = []
    for person in people:
      try:
        result = {}
        result["name"] = person.find_element(By.CSS_SELECTOR, "span.entity-result__title-line").text
        result["position"] = person.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text
        result["location"] = person.find_element(By.CSS_SELECTOR, "div.entity-result__secondary-subtitle").text
        result["profile_link"] = person.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
      except Exception as e:
        print(e)
        continue
      results.append(result)
    return results

  def close(self):
    self.driver.close()