import json
import os

class Settings:
    def __init__(self):
        self.__settings = None
        self.__settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
        self.__load_settings()

    def __load_settings(self):
        with open(self.__settings_path, "r") as file:
            self.__settings = json.load(file)

    def get(self, key):
        return self.__settings[key]

    def set(self, key, value):
        self.__settings[key] = value
        with open(self.__settings_path, "w") as file:
            json.dump(self.__settings, file, indent=4)