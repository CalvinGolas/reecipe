import sys

import mariadb

from JsonUploader import JsonUploader


class DatabaseUploader:
    def __init__(self, username, password):
        # Connect to AWS MariaDB
        try:
            self.conn = mariadb.connect(
                user=username,
                password=password,
                host="reecipy-2.c5gknunzqmr7.us-west-2.rds.amazonaws.com",
                port=3306,
                database="Recipes"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.cur = self.conn.cursor()

    def upload_recipe(self, url, ingredients, cuisineType, recipeName, nutritionFacts):
        try:
            self.cur.execute(
                "INSERT INTO recipes_table (URL, ingredient_list, type, name, nutrition) VALUES (?, ?, ?, ?, ?)",
                (url, ingredients, cuisineType, recipeName, nutritionFacts))
        except mariadb.Error as e:
            print(f"Error: {e}")
        self.conn.commit()

    def upload_instruction(self, stepNumber, url, text):
        try:
            self.cur.execute(
                "INSERT INTO instruction_step_table  (URL, step_number, text) VALUES (?, ?, ?)",
                (stepNumber, url, text))
        except mariadb.Error as e:
            print(f"Error: {e}")
        self.conn.commit()

    def upload_ingredient(self, ingredientName, measurementUnit, amount):
        try:
            self.cur.execute(
                "INSERT INTO user_pantry_items (ingredient, unit, amount) VALUES (?, ?, ?)",
                (ingredientName, measurementUnit, amount))
        except mariadb.Error as e:
            print(f"Error: {e}")
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    dbUsername = input("Enter database username: ")
    dbPassword = input("Enter database password: ")
    dbUploader = DatabaseUploader(dbUsername, dbPassword)
    json_data = JsonUploader()
    json_data.json_data_extraction(dbUploader, json_file_path='C:/Users/Reece/Desktop/JsonTest.json')
    dbUploader.close_connection()
