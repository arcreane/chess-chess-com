import pygame
import sys
import os



def draw_chessboard(surface, x, y, size):
    LIGHT = (240, 217, 181)
    DARK = (181, 136, 99)
    font = pygame.font.SysFont("arial", 20)
    square_size = size // 8

    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            rect = pygame.Rect(x + col * square_size, y + row * square_size, square_size, square_size)
            pygame.draw.rect(surface, color, rect)

            # Chiffres à gauche
            if col == 0:
                number = str(8 - row)
                text = font.render(number, True, (0, 0, 0))
                surface.blit(text, (x - 20, y + row * square_size + 10))

            # Lettres en bas
            if row == 7:
                letter = chr(ord('A') + col)
                text = font.render(letter, True, (0, 0, 0))
                surface.blit(text, (x + col * square_size + 10, y + size + 5))




def demo():
    # Initialisation de Pygame
    pygame.init()

    # Taille de la fenêtre
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu Chess")

    # Couleurs
    WHITE = (255, 255, 255)
    LIGHT = (240, 217, 181)
    DARK = (181, 136, 99)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    BLACK = (0, 0, 0)

    Partie_lance = False

    # Image

    image_path = os.path.join("..", "assets", "Menu.png")
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (900, 600))

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Clic

        if event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_rect.collidepoint(event.pos):
                print(">>> Bouton cliqué !")
                Partie_lance = True

        if Partie_lance == False:
            # Remplir l'écran
            screen.blit(background, (0, 0))

            # Bouton

            bouton_rect = pygame.Rect(290, 400, 325, 60)
            #pygame.draw.rect(screen, (255, 0, 0), bouton_rect)
        if Partie_lance == True:
            screen.fill((WHITE))
            draw_chessboard(screen, 300, 20, 500)

        # Rafraîchir l'affichage
        pygame.display.flip()



    # Quitter proprement
    pygame.quit()
    sys.exit()