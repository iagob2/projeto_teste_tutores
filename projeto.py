import pgzrun
import random
from pgzero.rect import Rect

# ------------------- CONFIGURAÇÕES -------------------
WIDTH = 800
HEIGHT = 600
FLOOR_Y = 480
GRAVITY = 0.5
JUMP_STRENGTH = -15

HERO_WIDTH = 64
HERO_HEIGHT = 37
NUM_HERO_FRAMES = 5 # Corrigido para 11 frames

NUM_ENEMIES = 4
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 37
NUM_ENEMY_FRAMES = 5
ENEMY_SPEED = 4
MIN_ENEMY_DISTANCE = 300

music_intro = "jango"
music_death = "death"
music_gameplay = "fauxdoor"

# ------------------- ESTADOS -------------------
game_started = False
game_over = False
menu = True
music_enabled = True

# ------------------- CLASSES -------------------
class Hero:
    def __init__(self):
        self.pos = [WIDTH // 4, FLOOR_Y]
        self.velocity_y = 0
        self.is_jumping = False
        self.frame = 0
        self.elapsed = 0
        self.time_between_frames = 0.1

    def update(self, dt):
        # Animação
        self.elapsed += dt
        if self.elapsed >= self.time_between_frames:
            self.frame = (self.frame + 1) % NUM_HERO_FRAMES
            self.elapsed = 0

        # Gravidade
        self.velocity_y += GRAVITY
        self.pos[1] += self.velocity_y

        # Chão
        if self.pos[1] >= FLOOR_Y:
            self.pos[1] = FLOOR_Y
            self.velocity_y = 0
            self.is_jumping = False

        # Pulo
        if keyboard.space and not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

    def draw(self):
        frame_x = self.frame * HERO_WIDTH
        screen.surface.blit(images.hero, (self.pos[0], self.pos[1]), (frame_x, 0, HERO_WIDTH, HERO_HEIGHT))

    def get_rect(self):
        return Rect(self.pos[0], self.pos[1], HERO_WIDTH, HERO_HEIGHT)


class Enemy:
    def __init__(self, x):
        self.pos = [x, FLOOR_Y]
        self.frame = 0
        self.elapsed = 0
        self.time_between_frames = 0.15

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.time_between_frames:
            self.frame = (self.frame + 1) % NUM_ENEMY_FRAMES
            self.elapsed = 0

        self.pos[0] -= ENEMY_SPEED
        if self.pos[0] < -ENEMY_WIDTH:
            self.pos[0] = random.randint(WIDTH, WIDTH + MIN_ENEMY_DISTANCE)

    def draw(self):
        frame_x = self.frame * ENEMY_WIDTH
        screen.surface.blit(images.enemy, (self.pos[0], self.pos[1]), (frame_x, 0, ENEMY_WIDTH, ENEMY_HEIGHT))

    def get_rect(self):
        return Rect(self.pos[0], self.pos[1], ENEMY_WIDTH, ENEMY_HEIGHT)


# ------------------- INICIALIZAÇÃO -------------------
hero = Hero()
enemies = []

def init_enemies():
    global enemies
    enemies = []
    for i in range(NUM_ENEMIES):
        x = random.randint(WIDTH + i * MIN_ENEMY_DISTANCE, WIDTH + (i + 1) * MIN_ENEMY_DISTANCE)
        enemies.append(Enemy(x))

init_enemies()

# ------------------- MÚSICA -------------------
def play_music(track):
    if music_enabled:
        music.play(track)
        music.set_volume(0.5)

# ------------------- MENU -------------------
def draw_menu():
    screen.draw.text("MENU", center=(WIDTH // 2, 100), fontsize=50, color="white")
    screen.draw.filled_rect(Rect(WIDTH // 2 - 100, 200, 200, 50), "green")
    screen.draw.text("Start Game", center=(WIDTH // 2, 225), fontsize=30, color="white")
    screen.draw.filled_rect(Rect(WIDTH // 2 - 100, 300, 200, 50), "blue")
    screen.draw.text("Music: On" if music_enabled else "Music: Off", center=(WIDTH // 2, 325), fontsize=30, color="white")
    screen.draw.filled_rect(Rect(WIDTH // 2 - 100, 400, 200, 50), "red")
    screen.draw.text("Exit", center=(WIDTH // 2, 425), fontsize=30, color="white")

def check_menu_click(pos):
    global menu, music_enabled, game_started
    if Rect(WIDTH // 2 - 100, 200, 200, 50).collidepoint(pos):
        menu = False
        game_started = True
        play_music(music_intro)
    elif Rect(WIDTH // 2 - 100, 300, 200, 50).collidepoint(pos):
        music_enabled = not music_enabled
        if music_enabled:
            play_music(music_intro)
        else:
            music.stop()
    elif Rect(WIDTH // 2 - 100, 400, 200, 50).collidepoint(pos):
        exit()

def on_mouse_down(pos):
    if menu:
        check_menu_click(pos)

# ------------------- UPDATE -------------------
def check_collisions():
    global game_over
    hero_rect = hero.get_rect()
    for enemy in enemies:
        if hero_rect.colliderect(enemy.get_rect()):
            game_over = True
            if music_enabled:
                play_music(music_death)

def restart_game():
    global game_over, game_started, menu
    hero.pos = [WIDTH // 4, FLOOR_Y]
    hero.velocity_y = 0
    hero.is_jumping = False
    init_enemies()
    game_over = False
    game_started = False
    menu = True
    play_music(music_intro)

def update(dt):
    if menu:
        return
    if game_over:
        if keyboard.RETURN:
            restart_game()  # ✅ Corrigido botão ENTER funcionando corretamente
    else:
        hero.update(dt)
        for enemy in enemies:
            enemy.update(dt)
        check_collisions()

# ------------------- DRAW -------------------
def draw():
    screen.fill((135, 206, 250))  # Fundo azul
    screen.draw.filled_rect(Rect(0, FLOOR_Y + HERO_HEIGHT, WIDTH, HEIGHT - FLOOR_Y), "brown")  # Chão

    if menu:
        draw_menu()
    elif game_started and not game_over:
        hero.draw()
        for enemy in enemies:
            enemy.draw()
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
        screen.draw.text("Press ENTER to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

pgzrun.go()
