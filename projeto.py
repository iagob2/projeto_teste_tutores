import pgzrun
import random
from pgzero.rect import Rect

# Configurações
WIDTH = 800
HEIGHT = 600
HERO_WIDTH = 64
HERO_HEIGHT = 64
FLOOR_Y = 480  # O chão está mais próximo do limite inferior
GRAVITY = 0.5
JUMP_STRENGTH = -15  # Aumentei a força do pulo

# Estado do herói
hero_pos = [WIDTH // 4, FLOOR_Y]
velocity_y = 0
is_jumping = False
current_hero_frame = 0
hero_elapsed_time = 0
time_between_hero_frames = 0.1
NUM_HERO_FRAMES = 5

# Estado dos inimigos
NUM_ENEMIES = 5
ENEMY_SPEED = 4
MIN_ENEMY_DISTANCE = 300  # Distância mínima entre os inimigos
enemies = [{"pos": [random.randint(WIDTH + i * MIN_ENEMY_DISTANCE, WIDTH + (i + 1) * MIN_ENEMY_DISTANCE), FLOOR_Y]} for i in range(NUM_ENEMIES)]
current_enemy_frame = 0
enemy_elapsed_time = 0
time_between_enemy_frames = 0.15
ENEMY_FRAME_WIDTH = 64
ENEMY_FRAME_HEIGHT = 64
NUM_ENEMY_FRAMES = 5

# Estados do jogo
game_started = False
game_over = False
menu = True
music_enabled = True

# Variáveis para as músicas
music_intro = "jango"  # Música que toca quando o jogo começa
music_death = "death"  # Música que toca quando o personagem morre
music_gameplay = "fauxdoor"  # Música de fundo durante o jogo

# Função para tocar música
def play_music(track):
    if music_enabled:
        music.play(track)
        music.set_volume(0.5)

# Função do menu principal
def draw_menu():
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, 100), fontsize=50, color="white")
    screen.draw.filled_rect(Rect(WIDTH // 2 - 100, 200, 200, 50), "green")
    screen.draw.text("Start Game", center=(WIDTH // 2, 225), fontsize=30, color="white")
    screen.draw.filled_rect(Rect(WIDTH // 2 - 100, 300, 200, 50), "blue")
    screen.draw.text("Music: On" if music_enabled else "Music: Off", center=(WIDTH // 2, 325), fontsize=30, color="white")
    screen.draw.filled_rect(Rect(WIDTH // 2 - 100, 400, 200, 50), "red")
    screen.draw.text("Exit", center=(WIDTH // 2, 425), fontsize=30, color="white")

# Verificar cliques no menu
def check_menu_click(pos):
    global menu, music_enabled, game_started
    if Rect(WIDTH // 2 - 100, 200, 200, 50).collidepoint(pos):  # Botão "Start Game"
        menu = False
        game_started = True
        play_music(music_intro)  # Tocar a música de introdução ao iniciar o jogo
    elif Rect(WIDTH // 2 - 100, 300, 200, 50).collidepoint(pos):  # Botão "Music"
        music_enabled = not music_enabled
        if music_enabled:
            play_music(music_intro)  # Caso a música seja ativada, toca a música de introdução
        else:
            music.stop()
    elif Rect(WIDTH // 2 - 100, 400, 200, 50).collidepoint(pos):  # Botão "Exit"
        exit()

# Evento de clique do mouse
def on_mouse_down(pos):
    if menu:
        check_menu_click(pos)

# Atualizar frames do herói
def animate_hero(dt):
    global current_hero_frame, hero_elapsed_time
    hero_elapsed_time += dt
    if hero_elapsed_time >= time_between_hero_frames:
        current_hero_frame = (current_hero_frame + 1) % NUM_HERO_FRAMES
        hero_elapsed_time = 0

# Atualizar frames dos inimigos
def animate_enemies(dt):
    global current_enemy_frame, enemy_elapsed_time
    enemy_elapsed_time += dt
    if enemy_elapsed_time >= time_between_enemy_frames:
        current_enemy_frame = (current_enemy_frame + 1) % NUM_ENEMY_FRAMES
        enemy_elapsed_time = 0

# Verificar colisões gerais
def check_collisions():
    global game_over
    hero_rect = Rect(hero_pos[0], hero_pos[1], HERO_WIDTH, HERO_HEIGHT)
    for enemy in enemies:
        enemy_rect = Rect(enemy["pos"][0], enemy["pos"][1], ENEMY_FRAME_WIDTH, ENEMY_FRAME_HEIGHT)
        if hero_rect.colliderect(enemy_rect):
            game_over = True
            if music_enabled:
                play_music(music_death)  # Tocar a música de "morte" quando o personagem colide com um inimigo

# Reiniciar o jogo
def restart_game():
    global hero_pos, enemies, game_over, game_started, menu, velocity_y, is_jumping
    hero_pos = [WIDTH // 4, FLOOR_Y]
    velocity_y = 0
    is_jumping = False
    enemies = [{"pos": [random.randint(WIDTH + i * MIN_ENEMY_DISTANCE, WIDTH + (i + 1) * MIN_ENEMY_DISTANCE), FLOOR_Y]} for i in range(NUM_ENEMIES)]
    game_over = False
    game_started = False
    menu = True
    play_music(music_intro)  # Tocar a música de introdução ao reiniciar o jogo

# Atualizar o jogo
def update(dt):
    global velocity_y, is_jumping
    if menu or not game_started:
        return
    if game_over:
        if keyboard.RETURN:
            restart_game()
    else:
        # Gravidade
        velocity_y += GRAVITY
        hero_pos[1] += velocity_y

        # Limitar ao chão
        if hero_pos[1] >= FLOOR_Y:
            hero_pos[1] = FLOOR_Y
            velocity_y = 0
            is_jumping = False

        # Pulo
        if keyboard.space and not is_jumping:
            velocity_y = JUMP_STRENGTH
            is_jumping = True

        # Movimentar inimigos para a esquerda
        for enemy in enemies:
            enemy["pos"][0] -= ENEMY_SPEED
            if enemy["pos"][0] < -ENEMY_FRAME_WIDTH:
                enemy["pos"][0] = random.randint(WIDTH, WIDTH + MIN_ENEMY_DISTANCE)

        # Atualizar animações e colisões
        animate_hero(dt)
        animate_enemies(dt)
        check_collisions()

# Desenhar herói
def draw_hero():
    hero_frame_x = current_hero_frame * HERO_WIDTH
    screen.surface.blit(images.hero, (hero_pos[0], hero_pos[1]), (hero_frame_x, 0, HERO_WIDTH, HERO_HEIGHT))

# Desenhar inimigos
def draw_enemies():
    for enemy in enemies:
        enemy_frame_x = current_enemy_frame * ENEMY_FRAME_WIDTH
        screen.surface.blit(images.enemy, (enemy["pos"][0], enemy["pos"][1]), (enemy_frame_x, 0, ENEMY_FRAME_WIDTH, ENEMY_FRAME_HEIGHT))

# Desenhar o jogo
def draw():
    screen.fill((135, 206, 250))  # Fundo azul claro (céu)
    screen.draw.filled_rect(Rect(0, FLOOR_Y + HERO_HEIGHT, WIDTH, HEIGHT - FLOOR_Y), "brown")  # Chão

    if menu:
        draw_menu()
    elif game_started and not game_over:
        draw_hero()
        draw_enemies()
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
        screen.draw.text("Press ENTER to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

pgzrun.go()
