from random import randint

import pygame

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
MISSING_COLOR = (255, 0, 255)   # маркер отсутствующего цвета
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Основной класс для объектов"""

    def __init__(self, position=None, body_color=MISSING_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки, будет переопределен в дочерних объектах."""
        pass

    @staticmethod
    def draw_cell(position, color):
        """Метод для отрисовки одной клетки игрового поля"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для объекта яблока, наследуется от GameObject"""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        if position is None:
            self.randomize_position()

    def randomize_position(self) -> None:
        """Метод для генерации случайных координат"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self) -> None:
        """Метод для отрисовки яблока на игровом поле"""
        if self.position:
            GameObject.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс для объекта змея, наследовано от GameObject"""

    def __init__(self, position=None, body_color=SNAKE_COLOR):
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        default_position = position if position else (start_x, start_y)
        super().__init__(default_position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    @property
    def get_head_position(self):
        """Возвращение координат головы змейки"""
        return self.positions[0]

    def update_direction(self, direction):
        """Обновление направления движения головы змейки"""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction

    def move(self) -> None:
        """Передвижение змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head = self.positions[0]
        x, y = self.direction
        new_head = (
            (cur_head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (cur_head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )

        # Проверка столкновения с самим собой
        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def draw(self) -> None:
        """Отрисовка змейки на игровом поле"""
        # Отрисовка всех сегментов, кроме головы
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента (если был удалён)
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def reset(self) -> None:
        """Сброс в начальное состояние"""
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.position = (start_x, start_y)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(snake: Snake) -> None:
    """Обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основная логика игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        try:
            handle_keys(snake)
        except SystemExit:
            running = False
            continue

        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()