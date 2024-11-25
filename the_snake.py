import pygame
from random import randint

# Константы для размеров экрана и сетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Ширина сетки в клетках
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE # Высота сетки в клетках

# Направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный фон
BORDER_COLOR = (93, 216, 228)       # Цвет границы клеток
APPLE_COLOR = (255, 0, 0)           # Красный цвет яблока
SNAKE_COLOR = (0, 255, 0)           # Зеленый цвет змейки

# Скорость игры (кадры в секунду)
SPEED = 20

# Инициализация Pygame
pygame.init()

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')  # Заголовок окна

# Объект для контроля времени
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, x, y, color):
        """Инициализация объекта: позиция (x, y) и цвет."""
        self.position = (x, y)
        self.color = color

    def draw(self, screen):
        """Отрисовка объекта на экране."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)  # Рисуем рамку


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока: вызов базового класса и установка случайной позиции."""
        super().__init__(0, 0, APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1),
            randint(0, GRID_HEIGHT - 1),
        )


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки: начальная позиция, длина, направление и т.д."""
        super().__init__(GRID_WIDTH // 2, GRID_HEIGHT // 2, SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None  # Позиция хвоста для затирания следа

    def move(self):
        """Обновление позиции змейки с учетом переноса через границы."""
        self.update_direction()
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % GRID_WIDTH,
            (head_y + dy) % GRID_HEIGHT,
        )  # Перенос через границы
        self.positions.insert(0, new_head)
        self.last = self.positions.pop() if len(self.positions) > self.length else None
        self.position = new_head

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, screen):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:  # Рисуем все сегменты кроме головы
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(
            self.positions[0][0] * GRID_SIZE,
            self.positions[0][1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:  # Затираем след
            last_rect = pygame.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def check_collision(self):
        """Проверка на столкновение змейки с самой собой или границами."""
        head = self.positions[0]
        return (
            head in self.positions[1:]
            or head[0] < 0
            or head[0] >= GRID_WIDTH
            or head[1] < 0
            or head[1] >= GRID_HEIGHT
        )


def handle_keys(snake):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        clock.tick(SPEED)  # Ограничение FPS
        handle_keys(snake)
        snake.move()

        if snake.position == apple.position:  # Змейка съела яблоко
            snake.length += 1
            apple.randomize_position()

        if snake.check_collision():  # Проверка на столкновение
            running = False

        screen.fill(BOARD_BACKGROUND_COLOR)  # Заливаем экран фоном
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()  # Обновляем экран

    pygame.quit()


if __name__ == "__main__":
    main()