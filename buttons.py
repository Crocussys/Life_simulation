import pygame


class Button:
    def __init__(self, screen, identifier, left=0, top=0, width=0, height=0):
        self.screen = screen
        self.id = identifier
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(left, top)
        self.bg_color = (255, 255, 255)
        self.active = False

        self._init_active_color(None)

    def draw(self):
        if self.active:
            self.surf.fill(self.active_color)
        else:
            self.surf.fill(self.bg_color)
        self.screen.blit(self.surf, self.rect)

    def set_size(self, w, h):
        self.surf = pygame.Surface((w, h))
        self.rect.inflate_ip(w, h)

    def set_pos(self, left, top):
        self.rect.move_ip(left, top)

    def check_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.active:
                return "click"
        return None

    def _init_active_color(self, act_color):
        if act_color is None:
            if (self.bg_color[0] + self.bg_color[1] + self.bg_color[2]) // 3 < 128:
                temp_color = [self.bg_color[0] + 100, self.bg_color[1] + 100, self.bg_color[2] + 100]
            else:
                temp_color = [self.bg_color[0] - 100, self.bg_color[1] - 100, self.bg_color[2] - 100]
            for i in range(3):
                if temp_color[i] > 255:
                    temp_color[i] = 255
                if temp_color[i] < 0:
                    temp_color[i] = 0
            self.active_color = (temp_color[0], temp_color[1], temp_color[2])
        else:
            self.active_color = act_color


class ButtonImage(Button):
    def __init__(self, screen, identifier, img_path, left=0, top=0, width=0, height=0):
        super().__init__(screen, identifier, left, top, width, height)
        self.img = pygame.image.load(img_path)
        self.rect_img = self.img.get_rect()

    def draw(self):
        super().draw()
        self.rect_img.center = self.rect.center
        self.screen.blit(self.img, self.rect_img)


class ButtonText(Button):
    def __init__(self, screen, identifier, text="Sample", left=0, top=0, width=0, height=0):
        super().__init__(screen, identifier, left, top, width, height)
        self.text_surf = pygame.font.SysFont(None, 32).render(text, True, (0, 0, 0))
        self.rect_text = self.text_surf.get_rect()

    def draw(self):
        super().draw()
        self.rect_text.center = self.rect.center
        self.screen.blit(self.text_surf,  self.rect_text)

    def set_text(self, text, font, antialias, color):
        self.text_surf = font.render(text, antialias, color)
