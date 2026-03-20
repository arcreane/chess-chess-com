import pygame
import sys
import os


Partie_lance = False





def demo():
    # Initialisation de Pygame
    pygame.init()

    # Taille de la fenêtre
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu Chess")

    # Couleurs
    WHITE = (255, 255, 255)

    BLACK = (0, 0, 0)

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
                running = False  # on quitte le menu

        # Remplir l'écran
        screen.blit(background, (0, 0))

        # Bouton

        bouton_rect = pygame.Rect(290, 400, 325, 60)
        #pygame.draw.rect(screen, (255, 0, 0), bouton_rect)

        # Rafraîchir l'affichage
        pygame.display.flip()



    # Quitter proprement
    pygame.quit()
    sys.exit()