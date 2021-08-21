import os
from Webscraping_Reecipe import AllRecipesWebScraper


carousel_category_url_list = ["https://www.allrecipes.com/recipes/23070/everyday-cooking/cookware-and-equipment/air-fryer/",
                              "https://www.allrecipes.com/recipes/76/appetizers-and-snacks/",
                              "https://www.allrecipes.com/recipes/663/meat-and-poultry/chicken/chicken-wings/"]
recipe_url = "https://www.allrecipes.com/recipe/272666/sweet-chili-and-orange-marmalade-glazed-chicken-wings/"

driver_path = os.path.join(os.getcwd(), "driver", "chromedriver.exe")
output_path = os.path.join(os.getcwd(), "json_output", "example.json")

scraper = AllRecipesWebScraper(driver_path, hidden=False)

# this method scrapes from the main page:
scraper.scrape_main_page(max_recipes_per_carousel_page=3,verbose=False)

# this method allows you to pass a list of category pages directly to be scraped
scraper.scrape_carousel(carousel_category_url_list, max_recipes_per_carousel_page=3,verbose=False)

# this method allows you to scrape a recipy directly
scraper.scrape_recipe_page(recipe_url,verbose=False,auto_close_browser=True)

# this method returns a dict for all scraped urls
output = scraper.return_dict()

# this method writes the current dict as a json to an output path
scraper.save_dict(output_path)

# this method clears the current dict to allow for the generation of a fresh one

scraper.clear_dict()

