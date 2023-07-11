import pygame
import random
import math

# Initialize pygame
pygame.init()

# Create game screen
screen = pygame.display.set_mode((800, 600))
# Set icon and title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ovni.png")
pygame.display.set_icon(icon)
background = pygame.image.load("fondo.jpg")

# Add player
img_player = pygame.image.load("fredyy.png")
player_x = 368
player_y = 536
player_x_change = 0

img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 5

# Add enemy
for i in range(number_of_enemies):
    img_enemy.append(pygame.image.load("boy.gif"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(30, 200))
    enemy_x_change.append(0.3)
    enemy_y_change.append(30)

# Bullet variables
img_bullet = pygame.image.load("piz.png")
bullet_x = 0
bullet_y = 536
bullet_y_change = 0.5
bullet_visible = False

# Score values
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_text_x = 10
score_text_y = 10

#end game
end_font = pygame.font.Font("freesansbold.ttf", 64)

#Game over
def final_message():
    final_text = end_font.render(f"GAME OVER: {score}", True, (255, 255, 255))
    screen.blit(final_text, (200, 200))

#show score

def show_score(x, y):
    text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))

# Show player on screen
def player(x, y):
    screen.blit(img_player, (x, y))

# Show enemy
def enemy(x, y, enemy_index):
    screen.blit(img_enemy[enemy_index], (x, y))

# Shoot
def shoot_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(img_bullet, (x + 16, y + 10))

# Detect collision
def detect_collision(x_1, y_1, x_2, y_2):
    x_sub = x_2 - x_1
    y_sub = y_2 - y_1
    distance = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
    if distance < 27:
        return True
    else:
        return False

# Game loop
is_running = True
while is_running:
    screen.blit(background, (0, 0))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 0.3
            if event.key == pygame.K_RIGHT:
                player_x_change += 0.3
            if event.key == pygame.K_SPACE:
                if not bullet_visible:
                    bullet_x = player_x
                    shoot_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_of_enemies):
        #End of game
        if enemy_y[i] > 450:
            for j in range(number_of_enemies):
                enemy_y[j] = 1000
            final_message()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        collision = detect_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(30, 200)
            bullet_visible = False
            score += 1
            bullet_y = 536
            #print(score)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= -64:
        bullet_y = 536
        bullet_visible = False

    if bullet_visible:
        shoot_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)

    #show score
    show_score(score_text_x, score_text_y)

    pygame.display.update()  # Update screen

# Quit pygame
pygame.quit()