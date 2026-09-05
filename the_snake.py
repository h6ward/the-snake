from random import randint

import pygame

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
MISSING_COLOR = (255, 0, 255)
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Основной класс для объектов."""

    def __init__(self, position=None, body_color=MISSING_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки, будет переопределен в дочерних классах."""
        

    @staticmethod
    def draw_cell(position, color, draw_border=True):
        """Метод для отрисовки одной клетки игрового поля."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if draw_border:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для объекта яблока, наследуется от GameObject."""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        super().__init__(position, body_color)

    def randomize_position(self, occupied_positions):
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_pos = (x, y)
            if new_pos not in occupied_positions:
                self.position = new_pos
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        if self.position:
            self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс для объекта змея, наследовано от GameObject."""

    def __init__(self, position=None, body_color=SNAKE_COLOR):
        default_position = position if position else CENTER_POSITION
        super().__init__(default_position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    @property
    def get_head_position(self):
        """Возвращение кординатов головы змейки."""
        return self.positions[0]

    def update_direction(self, direction):
        """Обновляет направление движения головы змейки."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def move(self) -> None:
        """Перемещает змею на одну клетку в текущем направлении."""
        head = self.get_head_position
        x, y = self.direction
        new_head = (
            (head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Если длина не увеличилась, удаляем хвост
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовка змейки на игровом поле."""
        if self.last is not None:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, draw_border=False)
        self.draw_cell(self.get_head_position, self.body_color)

    def reset(self) -> None:
        """Сброс в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.position = CENTER_POSITION
        self.direction = RIGHT
        self.last = None


def handle_keys(snake: Snake) -> None:
    """Обработка событий."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основная логика игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    # Первоначальная отрисовка всего
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()
    apple.draw()
    pygame.display.update()

    running = True
    while running:
        try:
            handle_keys(snake)
        except SystemExit:
            running = False
            continue

        snake.move()

        # Проверка столкновения с самим собой
        if snake.get_head_position in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
            continue

        # Проверка съедания яблока
        elif snake.get_head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
