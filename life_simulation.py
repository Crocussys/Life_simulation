import pygame

from settings import Settings
from buttons import ButtonImage, ButtonText
from cells import Grid


class LifeSimulation:
    """Класс для управления ресурсами и поведением"""

    def __init__(self):
        """Инициализирует приложение и создаёт ресурсы"""
        self.settings = Settings()
        self._init_display()
        self._init_interface()

    def run(self):
        """Запуск основного цикла"""
        while True:
            self.screen.fill(self.settings.bg_color)
            if self._check_events() == "exit":
                return 0
            for obj in self.objects:
                obj.draw()
            self.grid.draw(self.screen, self.mode)
            pygame.display.flip()

    def _init_display(self):
        """Инициализирует дисплей"""
        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_size = pygame.display.get_window_size()
        else:
            self.screen_size = (self.settings.screen_width, self.settings.screen_height)
            self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Life simulation")

    def _init_interface(self):
        """Инициализация интерфейса"""
        self.objects = []
        if self.settings.full_screen:
            exit_button = ButtonImage(self.screen, "exit", "img/exit_button.png", self.screen_size[0] - 40, 0, 40, 20)
            exit_button.bg_color = (200, 0, 0)
            self.objects.append(exit_button)
        self.objects.append(ButtonText(self.screen, "new_world", "Создать новый мир",
                                       self.screen_size[0] - 255, self.screen_size[1] - 55, 250, 50))
        self.button_area = pygame.Rect(self.screen_size[0] - 5 - 250, 25, 250, self.screen_size[1] - 30)
        mods = (("relief", "Рельеф"), ("temperature", "Температура"), ("creature", "Существа"))
        i = 0
        for option in mods:
            button = ButtonText(self.screen, option[0], option[1], 0, 0, 250, 50)
            button.rect.topleft = self.button_area.topleft
            button.rect.y += 55 * i
            self.objects.append(button)
            i += 1
        self.mode = "temperature"
        self.grid = Grid(self)

    def _check_events(self):
        """Проверяет события пользователя"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return "exit"
            for obj in self.objects:
                my_event = obj.check_events(event)
                if my_event == "click":
                    if obj.id == "exit":
                        return "exit"
                    elif obj.id == "new_world":
                        self.grid.generate_world()
                    elif obj.id == "relief":
                        self.mode = "relief"
                    elif obj.id == "temperature":
                        self.mode = "temperature"


if __name__ == '__main__':
    pygame.init()
    app = LifeSimulation()
    print(app.run())
    pygame.quit()
