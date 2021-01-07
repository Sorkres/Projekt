import pygame
import os
import random

class Settings:          #Eine Klasse für Settings (Einstellungen) die wir später brauchen.
    window_width = 1000  #In die Klasse gibt man die ganze wichtigste Einstellungen ein, wie z.B
    window_height = 600  #Fenster Grösse, Höhe, Gegneranzahl usw.
    border = 50
    second_border = 0
    enemy_count = 6
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    title = "Projekt Vilkevicius" 
    
class Background(object):  #Eine einzelne Klasse für Hintegrund
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename)) #Ladet den Hintegrund 
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height)).convert() #Convertiert und transformiert
        self.rect = self.image.get_rect()
    def draw(self, screen): # "Malt" das Hintergrund
        screen.blit(self.image, self.rect) 

class Airplane(pygame.sprite.Sprite): #Eine Klasse für den Spieler Modell
    def __init__(self, filename):
        super().__init__()
        bitmap = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = bitmap.convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = (Settings.window_width - 50) // 2
        self.rect.bottom = Settings.window_height - Settings.second_border -10 #Gibt Fenstergränzen ein
        self.direction = 0 #Damit der Spieler Modell am amfang Stehen bleibt
        self.speed = 5 #Hier kann man den Geschwindigkeit von den Spieler Modell einstellen
    def update(self): #Akutalisierung der Spieler Modell
        newrect = self.rect.move(self.direction * self.speed, 0) 
        if newrect.left <= Settings.second_border:
             self.move_stop() #Lässt den Spieler Modell nicht aus dem Spielfenster rausfliegen
        if newrect.right >= Settings.window_width - Settings.second_border:
             self.move_stop() #Lässt den Spieler Modell nicht aus dem Spielfenster rausfliegen
        self.rect.move_ip(self.direction * self.speed, 0)
    def move_left(self):
        self.direction = -1   #Gibt den Direction input für bewegung
    def move_right(self):
        self.direction = 1    #Gibt den Direction input für bewegung
    def move_stop(self):
        self.direction = 0    #Gibt den Direction input für bewegung

class Enemy(pygame.sprite.Sprite): #Eine Klasse für die Gegner (Hindernisse)
    def __init__(self, filename, column, row):
        super().__init__()
        bitmap = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = bitmap.convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75)).convert_alpha() #Skalierung von die Gegner
        self.rect = self.image.get_rect()
        self.distance = 85 #Abstand zwischen die Gegner
        newx = Settings.border+(self.rect.width + self.distance) * column #Gegner Spawnpoints
        newy = Settings.second_border + (self.rect.height + self.distance) * row #Gegner Spawnpoints
        self.rect.move_ip(newx, newy) #Bewegt die neue Gegner auf deren Spawnpoints
        
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(Settings.title)
    screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
    clock = pygame.time.Clock() 
    all_sprites = pygame.sprite.Group()
    background = Background("nebula.bmp") #Hier gibt man die name von den Background
    airplane = Airplane("airplane.bmp") #Hier gibt man die name von den Spieler Modell
    all_sprites.add(airplane)
    for row in range(0, 1):
        for column in range(0, Settings.enemy_count):
            all_sprites.add(Enemy("enemy_airplane.bmp", column, row)) #Hier gibt man die name von den Gegner Modell
    
    run = True
    while run:
        clock.tick(60) #FPS einstellung
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN: #Stellt ein welche Keys was macht. z.B Like Pfeiltaste bewegt den Modell nach links
                if event.key == pygame.K_LEFT:
                    airplane.move_left()
                elif event.key == pygame.K_RIGHT:
                    airplane.move_right()
                elif event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    airplane.move_stop()

        airplane.update()         
        background.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()      #Akutalisiert die Fenster
pygame.quit()
        