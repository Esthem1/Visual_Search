import pygame
import math
from queue import PriorityQueue, Queue
from collections import deque

pygame.font.init()
pygame.init()
font = pygame.font.Font(None, 25)
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithms")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path.append(current.get_pos())
    path.reverse()
    print("Path:", path)


def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dfs(draw, grid, start, end):
    stack = deque([start])
    came_from = {}
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                stack.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                queue.put(neighbor)
                visited.add(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def ucs(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    cost_so_far = {spot: float("inf") for row in grid for spot in row}
    cost_so_far[start] = 0

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1
            if new_cost < cost_so_far[neighbor]:
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
                open_set.put((new_cost, neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    cost_so_far = {spot: float("inf") for row in grid for spot in row}
    cost_so_far[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1
            if new_cost < cost_so_far[neighbor]:
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
                open_set.put((new_cost, neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def draw_menu():
    button_texts = ["A*", "DFS", "BFS", "UCS", "Dijkstra"]
    buttons = []
    y_offset = 150
    button_width = 200
    button_height = 80
    button_spacing = 30
    title_font = pygame.font.SysFont("Comic Sans MS", 45, bold=True)
    title_surface = title_font.render("Select Algorithm", True, WHITE)
    WIN.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

    for i, text in enumerate(button_texts):
        button_rect = pygame.Rect(
            WIDTH // 2 - button_width // 2,
            y_offset + i * (button_height + button_spacing),
            button_width,
            button_height
        )
        buttons.append((button_rect, text))

        pygame.draw.rect(WIN, GREY, button_rect, border_radius=10)
        text_surface = font.render(text, True, WHITE)
        WIN.blit(
            text_surface,
            (
                button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
                button_rect.y + (button_rect.height - text_surface.get_height()) // 2
            )
        )

    pygame.display.update()
    return buttons


def algorithm_selector():
    buttons = draw_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, text in buttons:
                    if button_rect.collidepoint(event.pos):
                        return text
            elif event.type == pygame.MOUSEMOTION:
                for button_rect, text in buttons:
                    color = GREY
                    if button_rect.collidepoint(event.pos):
                        color = (100, 100, 100)
                    pygame.draw.rect(WIN, color, button_rect, border_radius=10)
                    text_surface = pygame.font.SysFont("Comic Sans MS", 35).render(text, True, WHITE)
                    WIN.blit(
                        text_surface,
                        (
                            button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
                            button_rect.y + (button_rect.height - text_surface.get_height()) // 2
                        )
                    )
                pygame.display.update()


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start, end = None, None
    algorithm = algorithm_selector()  # Select algorithm

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if algorithm == "A*":
                        a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == "DFS":
                        dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == "BFS":
                        bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == "UCS":
                        ucs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == "Dijkstra":
                        dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid(ROWS, width)

    pygame.quit()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row, col = y // gap, x // gap
    return row, col


main(WIN, WIDTH)
