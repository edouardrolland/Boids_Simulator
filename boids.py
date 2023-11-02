import pygame

# Initialisation de Pygame
pygame.init()

# Taille de la première fenêtre
largeur_fenetre1 = 400
hauteur_fenetre1 = 300

# Taille de la deuxième fenêtre
largeur_fenetre2 = 800
hauteur_fenetre2 = 600

# Création des deux fenêtres
fenetre1 = pygame.display.set_mode((largeur_fenetre1, hauteur_fenetre1))
fenetre2 = pygame.display.set_mode((largeur_fenetre2, hauteur_fenetre2))

# Boucle principale
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Dessinez quelque chose dans la première fenêtre
    pygame.draw.rect(fenetre1, (255, 0, 0), (100, 100, 200, 100))

    # Dessinez quelque chose dans la deuxième fenêtre
    pygame.draw.rect(fenetre2, (0, 0, 255), (200, 200, 400, 200))

    # Mettez à jour les deux fenêtres
    pygame.display.update()

# Fermeture de Pygame
pygame.quit()