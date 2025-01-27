import pygame
import random
import sys
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Game settings
CELL_SIZE = 64
WIDTH = 25 * CELL_SIZE
HEIGHT = 15 * CELL_SIZE + 100
FPS = 30
CYBER_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_YELLOW = (255, 255, 0)
DARK_BG = (0, 0, 20)
DOT_COLOR = (255, 255, 255)
NEON_PURPLE = (128, 0, 255)
TERMINAL_GREEN = (0, 255, 64)
GLITCH_OFFSET = 2

# Load custom font
try:
    CYBER_FONT = pygame.font.Font("fonts/cyberpunk.ttf", 72)
except:
    CYBER_FONT = pygame.font.SysFont("couriernew", 72)
    print("Missing cyberpunk.ttf - using fallback font")

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberPunk-Man v2.0")
clock = pygame.time.Clock()

# UI Sound Effects
# menu_move_sound = pygame.mixer.Sound("sounds/ui_move.wav")
# menu_select_sound = pygame.mixer.Sound("sounds/ui_select.wav")


class CyberUI:
    @staticmethod
    def draw_glitch_text(text, font_size, position, color=NEON_PINK, alpha=255):
        text_surf = CYBER_FONT.render(text, True, color)
        text_surf.set_alpha(alpha)

        # Primary text
        screen.blit(text_surf, position)

        # Glitch effect
        for i in range(3):
            offset = (
                random.randint(-GLITCH_OFFSET, GLITCH_OFFSET),
                random.randint(-GLITCH_OFFSET, GLITCH_OFFSET),
            )
            glitch_surf = text_surf.copy()
            glitch_surf.fill(
                (random.randint(0, 255), 0, 0), special_flags=BLEND_RGB_ADD
            )
            screen.blit(glitch_surf, (position[0] + offset[0], position[1] + offset[1]))

    @staticmethod
    def create_cyber_button(text, rect, base_color, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        time = pygame.time.get_ticks()

        # Animated border
        border_width = 2 + int(abs(math.sin(time * 0.005)) * 3)
        color = hover_color if hovered else base_color

        # Hologram effect
        if hovered:
            hologram = pygame.Surface(rect.size, SRCALPHA)
            for i in range(rect.height // 2):
                alpha = max(50 - i * 5, 0)  # Prevent negative alpha values
                y = i * 4 + (time // 20) % 16
                pygame.draw.line(
                    hologram, (*base_color, alpha), (0, y), (rect.width, y), 2
                )
            screen.blit(hologram, rect.topleft)

        # Button background
        pygame.draw.rect(screen, DARK_BG, rect.inflate(20, 20), border_radius=12)
        pygame.draw.rect(screen, color, rect, border_width, border_radius=8)

        # Text
        text_rect = CYBER_FONT.render(text, True, color).get_rect(center=rect.center)
        CyberUI.draw_glitch_text(text, 36, text_rect.topleft, color)

    @staticmethod
    def level_select_menu():
        selected = 0
        options = [("NEURAL PATH", 0), ("CYBER CORE", 1), ("SYNTH MAZE", 2)]

        while True:
            screen.fill(DARK_BG)

            # Animated grid background
            time = pygame.time.get_ticks()
            for y in range(0, HEIGHT, 40):
                pygame.draw.line(
                    screen,
                    (*CYBER_BLUE, 30),
                    (time % 40 - 40, y),
                    (WIDTH + time % 40, y),
                )
            for x in range(0, WIDTH, 40):
                pygame.draw.line(
                    screen,
                    (*CYBER_BLUE, 30),
                    (x, time % 40 - 40),
                    (x, HEIGHT + time % 40),
                )

            # Title
            CyberUI.draw_glitch_text(
                "MAINFRAME ACCESS", 90, (WIDTH // 2 - 500, 50), CYBER_BLUE
            )

            # Buttons
            button_rects = []
            y_pos = HEIGHT // 4  # Start higher to accommodate larger spacing
            for i, (text, level) in enumerate(options):
                btn_rect = pygame.Rect(WIDTH // 2 - 500, y_pos, 1000, 80)
                color = NEON_PURPLE if i == selected else NEON_PINK
                CyberUI.create_cyber_button(text, btn_rect, color, CYBER_BLUE)
                button_rects.append((btn_rect, level))
                y_pos += 150  # Increased from 100 to 150 for more spacing

            # Input handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    for rect, level in button_rects:
                        if rect.collidepoint(event.pos):
                            # menu_select_sound.play()
                            return level
                if event.type == KEYDOWN:
                    if event.key in [K_1, K_KP1]:
                        return 0
                    elif event.key in [K_2, K_KP2]:
                        return 1
                    elif event.key in [K_3, K_KP3]:
                        return 2
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            clock.tick(FPS)

    @staticmethod
    def draw_hud(score, lives, level):
        # Left status panel
        CyberUI.draw_glitch_text(
            f"CREDITS: {score}", 32, (20, HEIGHT - 90), TERMINAL_GREEN
        )
        CyberUI.draw_glitch_text(
            f"BIO-CORES: {'◉'*lives}", 32, (20, HEIGHT - 50), NEON_PURPLE
        )

        # Right system info
        CyberUI.draw_glitch_text(
            f"SECTOR: 0x{level+1:02X}", 32, (WIDTH - 320, HEIGHT - 90), CYBER_BLUE
        )

        # Central scanner
        scanner_y = (pygame.time.get_ticks() // 20) % HEIGHT
        scanner = pygame.Surface((WIDTH - 600, 4), SRCALPHA)
        scanner.fill((*NEON_PINK, 50))
        screen.blit(scanner, (300, scanner_y))


# Game settings
CELL_SIZE = 64
WIDTH = 25 * CELL_SIZE
HEIGHT = 15 * CELL_SIZE + 100  # Extra space for UI
FPS = 30
CYBER_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_YELLOW = (255, 255, 0)
DARK_BG = (0, 0, 20)
DOT_COLOR = (255, 255, 255)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberPunk-Man")
clock = pygame.time.Clock()

# Define levels
levels = [
    {
        # Level 0: Revised Easy
        "maze": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        "power_pellets": [(2, 2), (22, 2), (2, 12), (22, 12)],
    },
    {  # Level 1: Medium (original maze)
        "maze": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        "power_pellets": [(1, 1), (23, 1), (1, 13), (23, 13)],
    },
    {  # Level 2: Hard
        "maze": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        "power_pellets": [(1, 1), (23, 1), (1, 13), (23, 13)],
    },
]

# Add to constants
CONFETTI_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]


class ConfettiParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(CONFETTI_COLORS)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 5)
        self.velocity = (
            math.cos(self.angle) * self.speed,
            math.sin(self.angle) * self.speed,
        )
        self.size = random.randint(4, 8)
        self.lifetime = random.randint(20, 40)
        self.age = 0

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity = (self.velocity[0] * 0.95, self.velocity[1] + 0.25)
        self.age += 1
        return self.age < self.lifetime

    def draw(self):
        alpha = 255 - int(255 * (self.age / self.lifetime))
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color + (alpha,), (0, 0, self.size, self.size))
        screen.blit(surface, (self.x, self.y))


class ConfettiManager:
    def __init__(self):
        self.particles = []

    def add_confetti(self, x, y, count=60):
        for _ in range(count):
            self.particles.append(ConfettiParticle(x, y))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self):
        for p in self.particles:
            p.draw()


# Add to game initialization
confetti = ConfettiManager()


class CyberPacman:
    def __init__(self):
        self.reset_game()

    def reset_state(self):
        self.x = 12 * CELL_SIZE + CELL_SIZE // 2
        self.y = 7 * CELL_SIZE + CELL_SIZE // 2
        self.speed = CELL_SIZE // 4
        self.direction = 0  # 0=Right, 1=Down, 2=Left, 3=Up
        self.radius = CELL_SIZE // 2 - 4
        self.power_mode = False
        self.power_timer = 0

    def reset_game(self):
        self.reset_state()
        self.lives = 3
        self.score = 0

    def move(self, dx, dy, current_maze):
        new_x = self.x + dx
        new_y = self.y + dy

        current_cell_x = int(self.x // CELL_SIZE)
        current_cell_y = int(self.y // CELL_SIZE)

        target_cell_x = current_cell_x
        target_cell_y = current_cell_y

        if dx > 0:
            target_cell_x = current_cell_x + 1
        elif dx < 0:
            target_cell_x = current_cell_x - 1
        elif dy > 0:
            target_cell_y = current_cell_y + 1
        elif dy < 0:
            target_cell_y = current_cell_y - 1

        current_cell_valid = (
            0 <= current_cell_x < 25
            and 0 <= current_cell_y < 15
            and current_maze[current_cell_y][current_cell_x] == 0
        )

        target_cell_valid = (
            0 <= target_cell_x < 25
            and 0 <= target_cell_y < 15
            and current_maze[target_cell_y][target_cell_x] == 0
        )

        if dx != 0:
            new_y = current_cell_y * CELL_SIZE + CELL_SIZE // 2
            valid = current_cell_valid and target_cell_valid
        else:
            new_x = current_cell_x * CELL_SIZE + CELL_SIZE // 2
            valid = current_cell_valid and target_cell_valid

        if valid:
            self.x = new_x
            self.y = new_y
        else:
            cell_left = current_cell_x * CELL_SIZE
            cell_right = (current_cell_x + 1) * CELL_SIZE
            cell_top = current_cell_y * CELL_SIZE
            cell_bottom = (current_cell_y + 1) * CELL_SIZE

            if dx > 0:
                self.x = min(new_x, cell_right - self.radius - 1)
            elif dx < 0:
                self.x = max(new_x, cell_left + self.radius)
            elif dy > 0:
                self.y = min(new_y, cell_bottom - self.radius - 1)
            elif dy < 0:
                self.y = max(new_y, cell_top + self.radius)

    def draw(self):
        mouth_open = 0.3 + 0.2 * math.sin(pygame.time.get_ticks() * 0.01)
        angles = {
            0: (mouth_open, 2 * math.pi - mouth_open),
            3: (math.pi / 2 + mouth_open, math.pi / 2 - mouth_open),
            2: (math.pi + mouth_open, math.pi - mouth_open),
            1: (-math.pi / 2 + mouth_open, -math.pi / 2 - mouth_open),
        }
        pygame.draw.circle(screen, DARK_BG, (self.x, self.y), self.radius)
        pygame.draw.arc(
            screen,
            (255, 255, 0),
            (
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2,
            ),
            *angles[self.direction],
            self.radius,
        )
        if self.power_mode:
            pygame.draw.circle(screen, CYBER_BLUE, (self.x, self.y), self.radius, 3)
            self.speed = 3 * CELL_SIZE / 16
        if not self.power_mode:
            self.speed = CELL_SIZE / 8


# ... [Previous code remains the same until Ghost class] ...


class Ghost:
    def __init__(self, color, x, y):
        self.reset(color, x, y)

    def reset(self, color, x, y):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.color = color
        self.direction = random.choice([0, 1, 2, 3])
        self.desired_direction = self.direction
        self.speed = CELL_SIZE // 16
        self.flee = False
        self.base_color = color
        self.radius = CELL_SIZE // 2 - 4

    def get_valid_directions(self, current_maze):
        current_cell_x = int(self.x // CELL_SIZE)
        current_cell_y = int(self.y // CELL_SIZE)
        directions = []

        # Check all four directions
        for direction in [0, 1, 2, 3]:
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
            new_x = current_cell_x + dx
            new_y = current_cell_y + dy

            if 0 <= new_x < 25 and 0 <= new_y < 15:
                if current_maze[new_y][new_x] == 0:
                    directions.append(direction)

        return directions

    def is_centered(self):
        return (self.x % CELL_SIZE) == CELL_SIZE // 2 and (
            self.y % CELL_SIZE
        ) == CELL_SIZE // 2

    def move(self, current_maze):
        if self.is_centered():
            current_cell_x = int(self.x // CELL_SIZE)
            current_cell_y = int(self.y // CELL_SIZE)

            # Get all valid directions (non-wall paths)
            valid_directions = []
            for direction in [0, 1, 2, 3]:
                dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
                test_x = current_cell_x + dx
                test_y = current_cell_y + dy
                if 0 <= test_x < 25 and 0 <= test_y < 15:
                    if current_maze[test_y][test_x] == 0:
                        valid_directions.append(direction)

            # Remove opposite direction initially
            opposite_dir = (self.direction + 2) % 4
            filtered_directions = [d for d in valid_directions if d != opposite_dir]

            # Safety check: if no directions left but opposite is valid
            if not filtered_directions and opposite_dir in valid_directions:
                filtered_directions = [opposite_dir]

            # Final fallback to prevent empty list
            if not filtered_directions:
                filtered_directions = valid_directions.copy()

            # Choose new direction only if options exist
            if filtered_directions:
                # 25% chance to keep current direction if possible
                if self.direction in filtered_directions and random.random() < 0.25:
                    new_direction = self.direction
                else:
                    new_direction = random.choice(filtered_directions)

                self.direction = new_direction

        # Rest of movement code remains the same
        dx_movement, dy_movement = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.direction]
        new_x = self.x + dx_movement * self.speed
        new_y = self.y + dy_movement * self.speed

        # Axis locking
        current_cell_x = int(self.x // CELL_SIZE)
        current_cell_y = int(self.y // CELL_SIZE)
        if dx_movement != 0:
            new_y = current_cell_y * CELL_SIZE + CELL_SIZE // 2
        else:
            new_x = current_cell_x * CELL_SIZE + CELL_SIZE // 2

        # Final position validation
        target_cell_x = int(new_x // CELL_SIZE)
        target_cell_y = int(new_y // CELL_SIZE)
        if (
            0 <= target_cell_x < 25
            and 0 <= target_cell_y < 15
            and current_maze[target_cell_y][target_cell_x] == 0
        ):
            self.x = new_x
            self.y = new_y
        else:
            self.x = current_cell_x * CELL_SIZE + CELL_SIZE // 2
            self.y = current_cell_y * CELL_SIZE + CELL_SIZE // 2

    def draw(self):
        # Main ghost body
        color = (0, 0, 255) if self.flee else self.color
        if self.flee and pygame.time.get_ticks() % 200 < 100:
            color = (255, 255, 255)  # Flash white when fleeing

        # Draw main body
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

        # Draw eyes
        eye_offset = self.radius // 2
        eye_size = self.radius // 3
        pupil_size = self.radius // 6

        # Left eye
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (self.x - eye_offset, self.y - eye_offset // 2),
            eye_size,
        )
        pygame.draw.circle(
            screen,
            (0, 0, 200),
            (self.x - eye_offset, self.y - eye_offset // 2),
            pupil_size,
        )

        # Right eye
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (self.x + eye_offset, self.y - eye_offset // 2),
            eye_size,
        )
        pygame.draw.circle(
            screen,
            (0, 0, 200),
            (self.x + eye_offset, self.y - eye_offset // 2),
            pupil_size,
        )

        # Draw wavy bottom effect
        points = []
        for i in range(5):
            angle = i * math.pi / 2 + pygame.time.get_ticks() * 0.005
            offset = math.sin(angle) * 3
            points.append(
                (
                    self.x - self.radius + i * self.radius // 2,
                    self.y + self.radius + offset,
                )
            )
        pygame.draw.polygon(screen, color, points)


def draw_maze(current_maze):
    for y, row in enumerate(current_maze):
        for x, cell in enumerate(row):
            if cell == 1:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, CYBER_BLUE, rect.inflate(-4, -4))
                pygame.draw.rect(screen, DARK_BG, rect.inflate(-8, -8))


def draw_dots(current_dots):
    for y, row in enumerate(current_dots):
        for x, dot in enumerate(row):
            if dot == 1:
                pygame.draw.circle(
                    screen,
                    DOT_COLOR,
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                    4,
                )
            elif dot == 2:
                pygame.draw.circle(
                    screen,
                    NEON_PINK,
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                    8,
                )


def level_select_menu():
    selected_level = 0  # Default to first level
    buttons = []

    # Create level buttons
    level_options = [("Level 1", 0), ("Level 2", 1), ("Level 3", 2)]

    font = pygame.font.Font(None, 74)
    title_text = font.render("SELECT LEVEL", True, NEON_PINK)

    button_font = pygame.font.Font(None, 50)
    y_pos = HEIGHT // 3

    for option, level_num in level_options:
        text = button_font.render(option, True, CYBER_BLUE)
        button_rect = pygame.Rect(WIDTH // 2 - 150, y_pos, 300, 60)
        buttons.append((button_rect, text, level_num))
        y_pos += 100

    running = True
    while running:
        screen.fill(DARK_BG)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()

        for button_rect, text, level_num in buttons:
            color = NEON_YELLOW if button_rect.collidepoint(mouse_pos) else NEON_PINK
            pygame.draw.rect(screen, color, button_rect, border_radius=10)
            screen.blit(
                text,
                (
                    button_rect.centerx - text.get_width() // 2,
                    button_rect.centery - text.get_height() // 2,
                ),
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, _, level_num in buttons:
                    if button_rect.collidepoint(event.pos):
                        return level_num
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    return 0
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    return 1
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    return 2
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)


def game_loop(starting_level=0):
    pacman = CyberPacman()
    current_level = starting_level
    ghost_spawn = (12, 9)
    ghosts = []
    dots = []
    power_pellets = []

    def initialize_level():
        nonlocal dots, power_pellets, ghosts
        level_data = levels[current_level]
        maze = level_data["maze"]
        power_pellets = level_data["power_pellets"]

        # Initialize dots
        dots = [[1 if cell == 0 else 0 for cell in row] for row in maze]
        for x, y in power_pellets:
            dots[y][x] = 2

        # Reset ghosts
        ghosts = [
            Ghost((255, 0, 0), 10, 5),
            Ghost((0, 255, 0), 14, 5),
            Ghost((255, 192, 203), 10, 9),
            Ghost(NEON_PINK, 14, 9),
        ]
        pacman.reset_state()

    initialize_level()
    running = True
    game_over = False
    level_complete = False
    victory = False
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    while running:
        CyberUI.draw_hud(pacman.score, pacman.lives, current_level)
        screen.fill(DARK_BG)
        confetti.update()
        confetti.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over and restart_button.collidepoint(event.pos):
                    current_level = 0
                    initialize_level()
                    pacman.reset_game()
                    game_over = False
                elif victory and restart_button.collidepoint(event.pos):
                    current_level = 0
                    initialize_level()
                    pacman.reset_game()
                    victory = False

        if not game_over and not victory and not level_complete:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                pacman.direction = 2
            if keys[pygame.K_RIGHT]:
                pacman.direction = 0
            if keys[pygame.K_UP]:
                pacman.direction = 3
            if keys[pygame.K_DOWN]:
                pacman.direction = 1

            dx, dy = 0, 0
            if pacman.direction == 0:
                dx = pacman.speed
            elif pacman.direction == 1:
                dy = pacman.speed
            elif pacman.direction == 2:
                dx = -pacman.speed
            else:
                dy = -pacman.speed
            pacman.move(dx, dy, levels[current_level]["maze"])

            current_cell_x = int(pacman.x // CELL_SIZE)
            current_cell_y = int(pacman.y // CELL_SIZE)
            if dots[current_cell_y][current_cell_x]:
                if dots[current_cell_y][current_cell_x] == 2:
                    pacman.power_mode = True
                    pacman.power_timer = pygame.time.get_ticks()
                    for ghost in ghosts:
                        ghost.flee = True
                pacman.score += 100 if dots[current_cell_y][current_cell_x] == 2 else 10
                dots[current_cell_y][current_cell_x] = 0

            if (
                pacman.power_mode
                and pygame.time.get_ticks() - pacman.power_timer > 7000
            ):
                pacman.power_mode = False
                for ghost in ghosts:
                    ghost.flee = False

            for ghost in ghosts:
                ghost.move(levels[current_level]["maze"])

            for ghost in ghosts:
                distance = math.hypot(pacman.x - ghost.x, pacman.y - ghost.y)
                if distance < CELL_SIZE // 2:
                    if pacman.power_mode and ghost.flee:
                        confetti.add_confetti(ghost.x, ghost.y)
                        ghost.x = ghost_spawn[0] * CELL_SIZE + CELL_SIZE // 2
                        ghost.y = ghost_spawn[1] * CELL_SIZE + CELL_SIZE // 2
                        ghost.flee = False
                        pacman.score += 200

                    elif not pacman.power_mode and not ghost.flee:
                        pacman.lives -= 1
                        if pacman.lives <= 0:
                            game_over = True
                        else:
                            pacman.reset_state()
                        break

            if not any(cell in row for row in dots for cell in (1, 2)):
                if current_level < len(levels) - 1:
                    current_level += 1
                    initialize_level()
                else:
                    victory = True

        draw_maze(levels[current_level]["maze"])
        draw_dots(dots)
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()

        font = pygame.font.Font(None, 36)
        screen.blit(
            font.render(f"SCORE: {pacman.score}", True, CYBER_BLUE), (10, HEIGHT - 80)
        )
        screen.blit(
            font.render(f"LIVES: {pacman.lives}", True, CYBER_BLUE), (10, HEIGHT - 50)
        )
        screen.blit(
            font.render(f"LEVEL: {current_level+1}", True, CYBER_BLUE),
            (WIDTH - 200, HEIGHT - 80),
        )

        if game_over:
            screen.fill((0, 0, 0, 200), special_flags=pygame.BLEND_RGBA_MULT)
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", True, NEON_PINK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(
                font.render(f"FINAL SCORE: {pacman.score}", True, CYBER_BLUE),
                (WIDTH // 2 - 150, HEIGHT // 2 - 50),
            )
            pygame.draw.rect(screen, NEON_PINK, restart_button)
            screen.blit(
                font.render("RESTART", True, DARK_BG),
                (restart_button.x + 50, restart_button.y + 10),
            )

        if victory:
            screen.fill((0, 0, 0, 200), special_flags=pygame.BLEND_RGBA_MULT)
            font = pygame.font.Font(None, 72)
            text = font.render("YOU WON!", True, NEON_PINK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(
                font.render(f"FINAL SCORE: {pacman.score}", True, CYBER_BLUE),
                (WIDTH // 2 - 150, HEIGHT // 2 - 50),
            )
            pygame.draw.rect(screen, NEON_PINK, restart_button)
            screen.blit(
                font.render("PLAY AGAIN", True, DARK_BG),
                (restart_button.x + 30, restart_button.y + 10),
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # starting_level = level_select_menu()
    starting_level = CyberUI.level_select_menu()
    game_loop(starting_level)
