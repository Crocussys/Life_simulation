import pygame
import math
import random


class Cell:
    """Класс для управления ячейками"""
    def __init__(self, size, i, j):
        super().__init__()
        self.pos = (i, j)
        self.rect = pygame.Rect(j * size, i * size, size, size)
        self.height = 0
        self.temperature = 0
        self.contains = []


class Sun:
    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.main_pos = [self.x_max, self.y_max // 2]
        self.pre_pos = [0, self.y_max // 2]
        self.next_pos = [2 * self.x_max, self.y_max // 2]
        self.max = self.y_max * 4 // 10
        self.min = self.y_max * 6 // 10
        self.r = self.y_max // 2
        self.up = True

    def start_pos(self):
        self.main_pos = [self.x_max, self.y_max // 2]
        self.pre_pos = [0, self.y_max // 2]
        self.next_pos = [2 * self.x_max, self.y_max // 2]
        self.up = True

    def next(self):
        self.main_pos[0] -= 1
        if self.main_pos[0] < 0:
            self.main_pos[0] = self.x_max
            if self.up:
                self.main_pos[1] -= 1
                if self.main_pos[1] == self.max:
                    self.up = False
            else:
                self.main_pos[1] += 1
                if self.main_pos[1] == self.min:
                    self.up = True
        self.pre_pos = [self.main_pos[0] - self.x_max, self.main_pos[1]]
        self.next_pos = [self.main_pos[0] + self.x_max, self.main_pos[1]]

    def get_distance(self, cell_pos):
        for sun_pos in [self.main_pos, self.pre_pos, self.next_pos]:
            distance = ((cell_pos[1] - sun_pos[0]) ** 2 + (cell_pos[0] - sun_pos[1]) ** 2) ** 0.5
            if distance <= self.r:
                return distance
        return -1


class Noise:
    """Класс управляющий шумом"""
    def __init__(self, width, height):
        """Инициализирует шум"""
        # random.seed(1)
        self.width = width
        self.height = height
        self.cell_width = 0
        self.cell_height = 0
        self.form = []
        self.matrix = []

    def generate(self, octave):
        """Создаёт шум"""
        self.cell_width = math.ceil(self.width / octave)
        self.cell_height = math.ceil(self.height / octave)
        for k in range(octave):
            line = []
            form_line = []
            for j in range(octave):
                num = random.betavariate(3, 3)
                # num = random.randint(0, 1)
                form_line.append(num)
                for i in range(self.cell_width):
                    line.append(num)
            for i in range(self.cell_height):
                self.matrix.append(line)
            self.form.append(form_line)

    def smoothing(self):
        """Размывает шум"""
        new_matrix = []
        size = len(self.form)
        x = -self.cell_width // 2
        y = -self.cell_height // 2
        for i in range(size + 1):
            for j in range(size + 1):
                new_line = False
                if j == 0:
                    x = -self.cell_width // 2
                    new_line = True
                new_matrix = self._blur_square(y, x, size, new_line, new_matrix, self._get_points(i, j, size))
                x += self.cell_width
                if j == size:
                    y += self.cell_height
        self.matrix = new_matrix

    def _get_points(self, i, j, size):
        """Возвращает значения точект квадрата размытия по координатам"""
        if j == 0:
            if i == 0:
                q11 = 0.5
                q12 = self.form[i][(j + size // 2) % size]
                q21 = self.form[i][size - 1]
                q22 = self.form[i][j]
            elif i == size:
                q11 = self.form[i - 1][size - 1]
                q12 = self.form[i - 1][j]
                q21 = 0.5
                q22 = self.form[i - 1][(j + size // 2) % size]
            else:
                q11 = self.form[i - 1][size - 1]
                q12 = self.form[i - 1][j]
                q21 = self.form[i][size - 1]
                q22 = self.form[i][j]
        elif j == size:
            if i == 0:
                q11 = self.form[i][(j - 1 + size // 2) % size]
                q12 = 0.5
                q21 = self.form[i][j - 1]
                q22 = self.form[i][0]
            elif i == size:
                q11 = self.form[i - 1][j - 1]
                q12 = self.form[i - 1][0]
                q21 = self.form[i - 1][(j - 1 + size // 2) % size]
                q22 = 0.5
            else:
                q11 = self.form[i - 1][j - 1]
                q12 = self.form[i - 1][0]
                q21 = self.form[i][j - 1]
                q22 = self.form[i][0]
        elif i == 0:
            q11 = self.form[i][(j - 1 + size // 2) % size]
            q12 = self.form[i][(j + size // 2) % size]
            q21 = self.form[i][j - 1]
            q22 = self.form[i][j]
        elif i == size:
            q11 = self.form[i - 1][j - 1]
            q12 = self.form[i - 1][j]
            q21 = self.form[i - 1][(j - 1 + size // 2) % size]
            q22 = self.form[i - 1][(j + size // 2) % size]
        else:
            q11 = self.form[i - 1][j - 1]
            q12 = self.form[i - 1][j]
            q21 = self.form[i][j - 1]
            q22 = self.form[i][j]
        return q11, q12, q21, q22

    def _blur_square(self, y, x, size, line_flag, new_matrix, q):
        """Размывает квадрат"""
        for n in range(y, y + self.cell_height + 1):
            flag = True
            for k in range(x, x + self.cell_width + 1):
                if 0 <= k <= size * self.cell_width and 0 <= n <= size * self.cell_height:
                    if line_flag and flag:
                        new_matrix.append([])
                        flag = False
                    new_matrix[n].append(self._blur_formula(k, x, n, y, q))
        return new_matrix

    def _blur_formula(self, k, x, n, y, q):
        """Формула размытия точки в квадрате"""
        q11, q12, q21, q22 = (q[i] for i in range(4))
        r1 = (k - x) * (q12 - q11) / self.cell_width + q11
        r2 = (k - x) * (q22 - q21) / self.cell_width + q21
        return (n - y) * (r2 - r1) / self.cell_height + r1


class Grid:
    def __init__(self, app):
        self.bg_color = app.settings.bg_color
        self.cell_size = app.settings.cell_size
        self.surf_w = app.screen_size[0] - 5 * 3 - 250
        self.surf_h = app.screen_size[1] - 5 * 2
        self.surf = pygame.Surface((self.surf_w, self.surf_h))
        self.cells = []
        self.x_max = self.surf_w // self.cell_size
        self.y_max = self.surf_h // self.cell_size
        self.sun = Sun(self.x_max, self.y_max)
        self.distance = -1

    def generate_world(self):
        self.sun.start_pos()
        self.cells = []
        relief = self._create_relief(self.x_max, self.y_max)
        for i in range(self.y_max):
            for j in range(self.x_max):
                cell = Cell(self.cell_size, i, j)
                cell.height = relief[i][j] * 16000 - 8000
                self.cells.append(cell)

    def draw(self, screen, mode):
        self._next()
        self.surf.fill(self.bg_color)
        for cell in self.cells:
            pygame.draw.rect(self.surf, self._get_color(cell, mode), cell.rect)
        screen.blit(self.surf, (5, 5))

    def get_random_neighboring_cell(self, pos):
        i = pos[0]
        j = pos[1]
        i += random.randint(-1, 1)
        j += random.randint(-1, 1)
        if i < 0:
            i = 0
            j = j + self.x_max // 2
        elif i < self.y_max:
            i = self.y_max
            j = j + self.x_max // 2
        if j < 0:
            j = self.x_max
        elif j > self.x_max:
            j = 0
        for cell in self.cells:
            if cell.pos == (i, j):
                return cell
        raise ValueError

    def _next(self):
        for cell in self.cells:
            warming_up = cell.temperature
            self.distance = self.sun.get_distance(cell.pos)
            if self.distance != -1:
                warming_up = 50 * (1 - self.distance / self.sun.r)
            if cell.height >= 0:
                warming_up -= 6 * cell.height / 1000
            else:
                warming_up += 24 * cell.height / 1000
            if warming_up > cell.temperature:
                cell.temperature = (cell.temperature + warming_up) / 2
            if cell.temperature > -50:
                if cell.height >= 0:
                    cell.temperature -= 4 / self.y_max
                else:
                    cell.temperature -= 1 / self.y_max
            else:
                if cell.height >= 0:
                    cell.temperature -= 4 * (cell.temperature + 100) / 200 / self.y_max
                else:
                    cell.temperature -= (cell.temperature + 100) / 50 / self.y_max
        self.sun.next()

    def _noise_addition(self, noises):
        """Находит средний шум между шумами в массиве"""
        average = []
        count = len(noises)
        for i in range(noises[0].height):
            average.append([])
            for j in range(noises[0].width):
                summ = 0
                for noise in noises:
                    summ += noise.matrix[i][j]
                average[i].append(summ / count)
        return average

    def _create_relief(self, width, height, complexity=-1, size=1):
        """Создаёт рельев"""
        noises = []
        octaves = 4
        i = 0
        while octaves <= width // size and octaves <= height // size:
            if i >= complexity != -1:
                break
            noise = Noise(width, height)
            noise.generate(octaves)
            noise.smoothing()
            noises.append(noise)
            octaves *= 2
            i += 1
        return self._noise_addition(noises)

    def _get_color(self, cell, mode):
        """Получить цвет пикселя в зависимости от mode"""
        color = (255, 255, 255)
        if mode == "relief":
            if cell.height >= 5000:
                color = (229, 50, 18)
            elif 3000 <= cell.height < 5000:
                color = (255, 102, 0)
            elif 2000 <= cell.height < 3000:
                color = (254, 145, 60)
            elif 1000 <= cell.height < 2000:
                color = (254, 197, 90)
            elif 500 <= cell.height < 1000:
                color = (254, 217, 137)
            elif 200 <= cell.height < 500:
                color = (255, 255, 141)
            elif 0 <= cell.height < 200:
                color = (204, 233, 105)
            elif -200 <= cell.height < 0:
                color = (218, 241, 247)
            elif -2000 <= cell.height < -200:
                color = (179, 225, 238)
            elif -4000 <= cell.height < -2000:
                color = (141, 212, 230)
            elif -6000 <= cell.height < -4000:
                color = (103, 197, 222)
            elif cell.height < -6000:
                color = (103, 168, 208)
        elif mode == "temperature":
            t = cell.temperature
            if t >= 50:
                color = (255 * (100 - t) / 50, 0, 0)
            elif 30 <= t < 50:
                color = (255, 255 * (t - 50) / -20, 0)
            elif 10 <= t < 30:
                color = (255 * (t - 10) / 20, 255, 0)
            elif -10 <= t < 10:
                color = (0, 255, 255 * (t - 10) / -20)
            elif -30 <= t < -10:
                color = (0, 255 * (t + 30) / 20, 255)
            elif -50 <= t < -30:
                color = (255 * (t + 30) / -20, 0, 255)
            elif t < -50:
                rb = 255 * (t + 50) / 50 + 255
                color = (rb, 0, rb)
        elif mode == "noise":
            h = 255 * (cell.height + 8000) / 16000
            color = (h, h, h)
        for i in range(3):
            if color[i] < 0 or color[i] > 255:
                raise ValueError
        return color
