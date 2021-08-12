from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import json

option = webdriver.ChromeOptions()
option.add_argument("-incognito")

file_output_location = "C:/Users/Reece/Desktop/JsonTest.json"

browser = webdriver.Chrome('/Users/Reece/PycharmProjects/Reecipe/Webscraper/chromedriver.exe', options=option)
browser.get("https://www.allrecipes.com")
carousel_links = []
carousel_elements = browser.find_elements_by_xpath("//a[@class='carouselNav__link recipeCarousel__link']")
for carousel_element in carousel_elements[::2]:
    carousel_links.append(carousel_element.get_attribute('href'))

max_recipe = 3
recipe_count = 0
output_dictionary = {}

for carousel in carousel_links:
    browser.get(carousel)
    # Starting at a given webpage that includes others,
    # collects the urls, and moves to the new pages.
    link_elements = browser.find_elements_by_xpath("//a[@class='card__titleLink manual-link-behavior']")
    links = []
    for link_element in link_elements[::2]:
        links.append(link_element.get_attribute('href'))
    for link in links:
        browser.get(link)
        print(link)
    # Pulls out recipe name

        output_dictionary[link] = {}

        recipe_name_elements = browser.find_element_by_xpath("//h1[@class='headline heading-content']")
        recipe_name = recipe_name_elements.text

        output_dictionary[link]["Recipe Name"] = recipe_name

        print(recipe_name)
        print()

        # Pulls tags from the breadcrumb links, excluding those for Home and Recipe
        recipe_tags_elements = browser.find_elements_by_xpath("//span[@class='breadcrumbs__title']")
        recipe_tags = [x.text for x in recipe_tags_elements]
        for tag in recipe_tags[1:]:
            print(tag)
        print()

        output_dictionary[link]["Tags"] = recipe_tags[1:]

        # Searches through for any commas and cuts the string to exclude it
        recipe_ingredients_elements = browser.find_elements_by_xpath("//span[@class='ingredients-item-name']")
        recipe_ingredients = [y.text for y in recipe_ingredients_elements]
        recipe_ingredients = list(map(lambda ingredient: ingredient.split(",")[0], recipe_ingredients))
        print(recipe_ingredients)
        print()

        output_dictionary[link]["Ingredients"] = recipe_ingredients

        # Looks for instructions and instruction steps in order
        steps = browser.find_elements_by_xpath("//li[@class='subcontainer instructions-section-item']//p")
        step_text = [l2.text for l2 in steps]
        print(step_text)
        print()

        output_dictionary[link]["Steps"] = step_text

        meta_info_element = browser.find_elements_by_xpath("//div[@class='recipe-meta-item']")
        meta_info_list = [t.text for t in meta_info_element]

        for meta_info in meta_info_list:
            meta_type, meta_value = meta_info.split(":\n")
            print(f"{meta_type}: {meta_value}")
            print()
            output_dictionary[link][meta_type] = meta_value

        Nutrition_Fact_Element = browser.find_element_by_xpath("//div[@class = 'partial recipe-nutrition-section']/div[@class = 'section-body']")
        Nutrition_Facts = Nutrition_Fact_Element.text
        print(Nutrition_Facts)
        output_dictionary[link]["Nutrition"] = Nutrition_Facts

        recipe_count += 1
        if recipe_count >= max_recipe:
            recipe_count = 0
            break
            break
browser.close()
with open(file_output_location, "w") as f:
    json.dump(output_dictionary, f)
