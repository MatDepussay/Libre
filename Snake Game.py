import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()


cell_size = 15
cols = screen.get_width() // cell_size
rows = screen.get_height() // cell_size

snake = [(cols // 2, rows // 2)]
direction = (1, 0)
score = 0
paused = False

def random_food_position():
    while True:
        position = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if position not in snake:
            return position

food = random_food_position()

def draw_button(surface, rect, text):
    pygame.draw.rect(surface, (200, 200, 200), rect)
    pygame.draw.rect(surface, (100, 100, 100), rect, 3)
    btn_font = pygame.font.SysFont(None, 40)
    txt = btn_font.render(text, True, (0, 0, 0))
    txt_rect = txt.get_rect(center=rect.center)
    surface.blit(txt, txt_rect)

def load_best_score():
    try:
        with open("best_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_best_score(score):
    with open("best_score.txt", "w") as f:
        f.write(str(score))

best_score = load_best_score()

while True:
    screen.fill((30, 30, 30))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_UP or event.key == pygame.K_z and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_q and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and direction != (-1, 0):
                direction = (1, 0)

    if paused:
        pause_txt = font.render("Pause", True, (255, 255, 0))
        screen.blit(pause_txt, (250, 180))
        pygame.display.flip()
        clock.tick(10)
        continue

    # Déplacement du serpent
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Vérification des collisions
    if (
        head[0] < 0 or head[0] >= cols or
        head[1] < 0 or head[1] >= rows or
        head in snake
    ):
        if score > best_score:
            best_score = score
            save_best_score(best_score)
        msg = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
        best_txt = font.render(f"Best: {best_score}", True, (255, 215, 0))
        screen.blit(msg, (120, 120))
        screen.blit(best_txt, (120, 180))
        btn_rect = pygame.Rect(200, 240, 200, 60)
        draw_button(screen, btn_rect, "Rejouer")
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_rect.collidepoint(event.pos):
                        snake = [(cols // 2, rows // 2)]
                        direction = (1, 0)
                        score = 0
                        food = random_food_position()
                        waiting = False
            clock.tick(10)
        continue

    snake.insert(0, head)

    # Vérification de la pomme
    if head == food:
        score += 1
        food = random_food_position()
    else:
        snake.pop()

    # Dessin de la pomme
    pygame.draw.rect(
        screen, (255, 0, 0),
        (food[0] * cell_size, food[1] * cell_size, cell_size, cell_size)
    )

    # Dessin du serpent
    for s in snake:
        pygame.draw.rect(
            screen, (0, 255, 0),
            (s[0] * cell_size, s[1] * cell_size, cell_size, cell_size)
        )

    # Affichage du score
    score_txt = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_txt, (10, 10))

    # Affichage du best score
    best_txt = font.render(f"Best: {best_score}", True, (255, 215, 0))
    screen.blit(best_txt, (10, 50))

    pygame.display.flip()
    clock.tick(10)