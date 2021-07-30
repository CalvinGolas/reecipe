from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

option = webdriver.ChromeOptions()
option.add_argument("-incognito")

browser = webdriver.Chrome(executable_path= '/Users/Reece/PycharmProjects/Reecipe/Webscraper/chromedriver.exe', options=option)
browser.get("https://www.allrecipes.com/recipes/76/appetizers-and-snacks/")

timeout = 30

# Starting at a given webpage that includes others,
# collects the urls, and moves to the new pages.
Link_Elements = browser.find_elements_by_xpath("//a[@class='card__titleLink manual-link-behavior']")
Links = []
for i in range(0, len(Link_Elements), 2):
    Links.append(Link_Elements[i].get_attribute('href'))
for s in range(len(Links)):
    browser.get(Links[s])
    # Pulls out recipe name
    Recipe_Name_Elements = browser.find_element_by_xpath("//h1[@class='headline heading-content']")
    Recipe_Name = Recipe_Name_Elements.text
    print(Recipe_Name)
    print()

    # Pulls tags from the breadcrumb links, excluding those for Home and Recipe
    Recipe_Tags_Elements = browser.find_elements_by_xpath("//span[@class='breadcrumbs__title']")
    Recipe_Tag = [x.text for x in Recipe_Tags_Elements]
    for q in range(2, len(Recipe_Tag)):
        print(Recipe_Tag[q])
    print()
    # Searches through for any commas and cuts the string to exclude it
    Recipe_Ingredients_Elements = browser.find_elements_by_xpath("//span[@class='ingredients-item-name']")
    Recipe_Ingredients = [y.text for y in Recipe_Ingredients_Elements]
    for c in range(len(Recipe_Ingredients)):
        ingredient = Recipe_Ingredients[c]
        for c2 in range(len(ingredient)):
            if ingredient[c2] == ',':
                Recipe_Ingredients[c] = ingredient[0:c2]
    print(Recipe_Ingredients)
    print()


    # Looks for instructions and instruction steps in order
    Steps = browser.find_elements_by_xpath("//li[@class='subcontainer instructions-section-item']//p")
    Step_Text = [l2.text for l2 in Steps]
    print(Step_Text)
    print()

    CookTime_Element = browser.find_elements_by_xpath("//div[@class='recipe-meta-item']")
    CookTime = [t.text for t in CookTime_Element]
    for v in range(len(CookTime)):
        for n in range(len(CookTime[v])):
            CookTime[v] = re.sub("\n", " ", CookTime[v])
    print(CookTime)
    print()
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class=’component image-filmstrip']")))

except TimeoutException:
    print("Timed out waiting for the page to load")
    browser.quit()