import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Tableau de commande")

font = pygame.font.SysFont(None, 32)

# Définition des boutons
buttons = [
    {"rect": pygame.Rect(150, 80, 200, 50), "text": "Baisser le levier", "msg": "Levier baissé !"},
    {"rect": pygame.Rect(150, 160, 200, 50), "text": "Appuyer sur le bouton", "msg": "Bouton pressé !"},
    {"rect": pygame.Rect(150, 240, 200, 50), "text": "Écouter le message radio", "msg": "Message radio : 'Attention, anomalie détectée...'"},
]

message = ""

while True:
    screen.fill((30, 30, 30))

    # Affichage des boutons
    for btn in buttons:
        pygame.draw.rect(screen, (70, 130, 180), btn["rect"])
        txt = font.render(btn["text"], True, (255, 255, 255))
        screen.blit(txt, (btn["rect"].x + 10, btn["rect"].y + 10))

    # Affichage du message
    if message:
        msg_txt = font.render(message, True, (255, 255, 0))
        screen.blit(msg_txt, (50, 330))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn in buttons:
                if btn["rect"].collidepoint(event.pos):
                    message = btn["msg"]

    pygame.display.flip()