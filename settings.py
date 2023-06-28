import json


class Settings:
    """Класс для хранения всех настроек"""

    def __init__(self):
        """Инициализирует настройки из файла"""
        self.json_arr = {}
        with open('settings.json') as f:
            self.json_arr = json.load(f)

        self.full_screen = self.json_arr.get('full_screen', False)
        self.screen_width = self.json_arr.get('screen_width', 1900)
        self.screen_height = self.json_arr.get('screen_height', 1000)
        self.cell_size = self.json_arr.get('cell_size', 5)
        self.bg_color = self.json_arr.get('bg_color', (230, 230, 230))
