import sys
import yaml
import mariadb
from JsonUploader import JsonUploader


class DatabaseUploader:
    def __init__(self, host, username, password):
        # Connect to AWS MariaDB
        try:
            self.conn = mariadb.connect(
                user=username,
                password=password,
                host=host,
                port=3306,
                database="Recipes"
            )
        except mariadb.Error as exc:
            print(f"Error connecting to MariaDB Platform: {exc}")
            sys.exit(1)
        self.cur = self.conn.cursor()

    def upload_recipe(self, url, ingredients, cuisineType, recipeName, nutritionFacts):
        try:
            self.cur.execute(
                "INSERT INTO recipes_table (URL, ingredient_list, type, name, nutrition) VALUES (?, ?, ?, ?, ?)",
                (url, ingredients, cuisineType, recipeName, nutritionFacts))
        except mariadb.Error as exc:
            print(f"Error: {exc}")
        self.conn.commit()

    def upload_instruction(self, stepNumber, url, text):
        try:
            self.cur.execute(
                "INSERT INTO instruction_step_table  (URL, step_number, text) VALUES (?, ?, ?)",
                (stepNumber, url, text))
        except mariadb.Error as exc:
            print(f"Error: {exc}")
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    # Read the yml file saved locally in conf/credentials.yml
    try:
        conf = yaml.safe_load(open('conf/credentials.yml'))
        dbHost = conf['databaselogin']['host']
        dbUsername = conf['databaselogin']['username']
        dbPassword = conf['databaselogin']['password']
        dbUploader = DatabaseUploader(dbHost, dbUsername, dbPassword)
        json_data = JsonUploader()
        json_data.json_data_extraction(dbUploader, json_file_path='C:/Users/Reece/Desktop/JsonTest.json')
        dbUploader.close_connection()
    except yaml.YAMLError as e:
        print(f"Error reading yml file: {e}")
