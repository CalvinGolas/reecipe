from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import json


class AllRecipesWebScraper:

    def __init__(self,chrome_driver_path, hidden=False):
        option = webdriver.ChromeOptions()
        if hidden:
            option.add_argument("-incognito")
        self.browser = webdriver.Chrome(chrome_driver_path, options=option)
        self.scraped_dict = {}

    def scrape_main_page(self,max_recipes_per_carousel_page=10,verbose=False):

        url = "https://www.allrecipes.com/"
        self.browser.get(url)
        carousel_links = []
        carousel_elements = self.browser.find_elements_by_xpath("//a[@class='carouselNav__link recipeCarousel__link']")

        for carousel_element in carousel_elements[::2]:
            carousel_links.append(carousel_element.get_attribute('href'))

        self.scrape_carousel(carousel_links, max_recipes_per_carousel_page=max_recipes_per_carousel_page,verbose=verbose)

    def scrape_carousel(self, carousel, max_recipes_per_carousel_page=10,verbose=False):
        for carousel_link in carousel:
            self.browser.get(carousel_link)
            # Starting at a given webpage that includes others,
            # collects the urls, and moves to the new pages.

            page_link_elements = self.browser.find_elements_by_xpath("//a[@class='card__titleLink manual-link-behavior']")
            page_links = []
            recipe_count = 0

            for page_link_element in page_link_elements[::2]:
                page_links.append(page_link_element.get_attribute('href'))
                recipe_count += 1
                if recipe_count == max_recipes_per_carousel_page:
                    break

            for page_link in page_links:
                self.scrape_recipe_page(page_link, auto_close_browser=False,verbose=verbose)

        self.browser.close()

    def scrape_recipe_page(self, url, verbose=False, auto_close_browser=True):

        if url in self.scraped_dict.keys():
            if verbose:
                print(f"{url} already in json, skipping")
            return

        self.browser.get(url)
        if verbose:
            print(url)
        # Pulls out recipe name
        output_dictionary = {url: {}}

        recipe_name_elements = self.browser.find_element_by_xpath("//h1[@class='headline heading-content']")
        recipe_name = recipe_name_elements.text

        output_dictionary[url]["Recipe Name"] = recipe_name

        if verbose:
            print(recipe_name)
            print()

        # Pulls tags from the breadcrumb links, excluding those for Home and Recipe
        recipe_tags_elements = self.browser.find_elements_by_xpath("//span[@class='breadcrumbs__title']")
        recipe_tags = [x.text for x in recipe_tags_elements]

        if verbose:
            for tag in recipe_tags[1:]:
                print(tag)
            print()

        output_dictionary[url]["Tags"] = recipe_tags[1:]

        # Searches through for any commas and cuts the string to exclude it
        recipe_ingredients_elements = self.browser.find_elements_by_xpath("//span[@class='ingredients-item-name']")
        recipe_ingredients = [y.text for y in recipe_ingredients_elements]
        recipe_ingredients = list(map(lambda ingredient: ingredient.split(",")[0], recipe_ingredients))

        if verbose:
            print(recipe_ingredients)
            print()

        output_dictionary[url]["Ingredients"] = recipe_ingredients

        # Looks for instructions and instruction steps in order
        steps = self.browser.find_elements_by_xpath("//li[@class='subcontainer instructions-section-item']//p")
        step_text = [l2.text for l2 in steps]

        if verbose:
            print(step_text)
            print()

        output_dictionary[url]["Steps"] = step_text

        meta_info_element = self.browser.find_elements_by_xpath("//div[@class='recipe-meta-item']")
        meta_info_list = [t.text for t in meta_info_element]

        for meta_info in meta_info_list:
            meta_type, meta_value = meta_info.split(":\n")
            if verbose:
                print(f"{meta_type}: {meta_value}")
                print()
            output_dictionary[url][meta_type] = meta_value

        Nutrition_Fact_Element = self.browser.find_element_by_xpath(
            "//div[@class = 'partial recipe-nutrition-section']/div[@class = 'section-body']")
        Nutrition_Facts = Nutrition_Fact_Element.text

        if verbose:
            print(Nutrition_Facts)

        output_dictionary[url]["Nutrition"] = Nutrition_Facts

        self.scraped_dict.update(output_dictionary)

        if auto_close_browser:
            self.browser.close()

    def save_dict(self,file_output_location):
        with open(file_output_location, "w") as f:
            json.dump(self.scraped_dict, f)

    def clear_dict(self):
        self.scraped_dict = {}

    def return_dict(self):
        return self.scraped_dict






