import json


class JsonUploader:
    def __init__(self):
        return

    @staticmethod
    def json_data_extraction(uploader, json_file_path):
        with open(json_file_path, 'r') as f:
            dictionary_test = json.load(f)
            for URLs in dictionary_test.keys():
                uploader.upload_recipe(URLs, str(dictionary_test[URLs]['Ingredients']),
                                       str(dictionary_test[URLs]['Tags']), dictionary_test[URLs]['Recipe Name'],
                                       str(dictionary_test[URLs]['Nutrition']))
                for i in range(len(dictionary_test[URLs]['Steps'])):
                    uploader.upload_instruction(URLs, i, str(dictionary_test[URLs]['Steps']))
