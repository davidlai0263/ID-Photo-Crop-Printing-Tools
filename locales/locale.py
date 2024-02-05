import json
import os

class Locale:
    def __init__(self, language):
        self.language = language
        self.translations = self.load_translations()

    def set_language(self, language):
        self.language = language
        self.translations = self.load_translations()
    
    def get_language(self):
        return self.language

    def load_translations(self):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, f'{self.language}.json'), 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def get_translations(self):
        return self.translations

    def translate(self, section, key):
        return self.translations.get(section, {}).get(key, key)
