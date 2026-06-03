import pygame
import random
import sys
from pygame.locals import *
import os

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Labyrinth")

pygame.mixer.init()

skript_ordner = os.path.dirname(os.path.abspath(__file__))
pfad = os.path.join(skript_ordner, "boden.jpg")

hintergrund = pygame.image.load(pfad)
hintergrund = pygame.transform.scale(hintergrund, (600, 600))

#Hintergrundmusik
music_pfad = os.path.join(skript_ordner, "music.mp3")
pygame.mixer.music.load(music_pfad)
pygame.mixer.music.set_volume(0.3)  
pygame.mixer.music.play(-1)  #-1 = dauerschleife

#Bewegungssounds
move_sound_pfad = os.path.join(skript_ordner, "move.mp3")
move_sound = pygame.mixer.Sound(move_sound_pfad)
move_sound.set_volume(0.3)  

#Gewinnersound
win_sound_pfad = os.path.join(skript_ordner, "win.mp3")
win_sound = pygame.mixer.Sound(win_sound_pfad)
win_sound.set_volume(0.5)

GROESSE = 30           #Zelle 30x30 Pixel
ZEILEN = 20            #600/30 = 20 Zeilen
SPALTEN = 20           #20 Spalten

GRAU = (170, 170, 170)
TUERKIS = (0, 120, 120)
ROT = (255, 0, 0)
GELB = (255, 255, 0)

#Spielstatus Variable
spiel_aktiv = True

#Pause-Status Variable
paused = False

#Timer Startzeit (in Millisekunden)
start_zeit = pygame.time.get_ticks()

#Variable für die pausierte Zeit (Timer läuft in Pause nicht weiter)
pause_start_zeit = 0
gesamte_pausen_dauer = 0

#Squish-Animation
squish_timer = 0       #verbleibende Animationszeit
SQUISH_DAUER = 220     #Animation dauert 220ms

waende = []
besucht = []

#Ein 20x20 Gitter. Jede Zelle hat 4 Wände. Am Anfang sind alle Wände da. Zellen noch nicht besucht.
for z in range(ZEILEN):
    wand_zeile = []
    besucht_zeile = []
    for s in range(SPALTEN):
        wand_zeile.append([True, True, True, True])  #4 Wände
        besucht_zeile.append(False)
    waende.append(wand_zeile)
    besucht.append(besucht_zeile)

"""Suche der Nachbarn die noch nicht besucht sind. Geht schritt für schritt zu die jeweiligen Nachbarn. Schaut nach oben, rechts, unten, links. Speichert alle nicht besuchten in einer Liste"""
def finde_nachbarn(z, s):
    nachbarn = []
    #Oben
    if z > 0 and not besucht[z-1][s]:      #wenn besucht [false] ist wird das false durch not zu true heißt Zelle wurde noch nicht besucht sonst besucht
        nachbarn.append((z-1, s, 0, 2))
    #Rechts
    if s < SPALTEN-1 and not besucht[z][s+1]:
        nachbarn.append((z, s+1, 1, 3))
    #Unten
    if z < ZEILEN-1 and not besucht[z+1][s]:
        nachbarn.append((z+1, s, 2, 0))
    #Links
    if s > 0 and not besucht[z][s-1]:
        nachbarn.append((z, s-1, 3, 1))
    return nachbarn

#generierung
stack = [(0, 0)] #setzt Start oben links
besucht[0][0] = True #Start besucht

while stack: #so lang Zellen vorhanden sind
    z, s = stack[-1] #aktuelle Zelle
    nachbarn = finde_nachbarn(z, s)
    
    if nachbarn:
        #Wählt zufälligen Nachbarn
        nz, ns, wand1, wand2 = random.choice(nachbarn)
        #Entfernt Wände
        waende[z][s][wand1] = False
        waende[nz][ns][wand2] = False
        besucht[nz][ns] = True  #setzt Nachbar auf besucht
        stack.append((nz, ns))
    else:
        stack.pop()

#Setzt Startposition der Spielfigur nach links oben
spieler_x = 0
spieler_y = 0

#Funktion zum Zurücksetzen des Spiels
def spiel_reset():
    global spieler_x, spieler_y, spiel_aktiv, start_zeit, squish_timer, paused, gesamte_pausen_dauer
    spieler_x = 0
    spieler_y = 0
    spiel_aktiv = True
    paused = False
    gesamte_pausen_dauer = 0
    start_zeit = pygame.time.get_ticks()
    squish_timer = 0
    
    #Musik wieder starten bei Reset
    pygame.mixer.music.play(-1)

#Pause Menü Funktion
def zeige_pause_menue():
    global paused, pause_start_zeit, gesamte_pausen_dauer
    
    #Speichere wann die Pause begonnen hat
    pause_start_zeit = pygame.time.get_ticks()
    
    schrift = pygame.font.Font(None, 48)
    kleine_schrift = pygame.font.Font(None, 32)
    
    #Pause Schleife
    while paused:
        #Zuerst das Spiel im Hintergrund zeichnen
        zeichnen()
        
        #Halbtransparenter Hintergrund drüberlegen
        overlay = pygame.Surface((600, 600))
        overlay.set_alpha(150) #wert für Sichtbarkeit
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        #Pause Text
        pause_text = schrift.render("PAUSE", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(300, 200))
        screen.blit(pause_text, text_rect)
        
        #Buttons
        button_fortsetzen = pygame.Rect(200, 300, 200, 50)
        button_neustart = pygame.Rect(200, 370, 200, 50)
        button_beenden = pygame.Rect(200, 440, 200, 50)
        
        #Buttons zeichnen mit abgerundeten Ecken
        pygame.draw.rect(screen, (0, 150, 0), button_fortsetzen, border_radius=10)
        pygame.draw.rect(screen, (150, 150, 0), button_neustart, border_radius=10)
        pygame.draw.rect(screen, (150, 0, 0), button_beenden, border_radius=10)
        
        #Button Ränder
        pygame.draw.rect(screen, (255, 255, 255), button_fortsetzen, width=2, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), button_neustart, width=2, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), button_beenden, width=2, border_radius=10)
        
        #Button Texte
        text_fortsetzen = kleine_schrift.render("Fortsetzen", True, (255, 255, 255))
        text_neustart = kleine_schrift.render("Neu Starten", True, (255, 255, 255))
        text_beenden = kleine_schrift.render("Beenden", True, (255, 255, 255))
        
        screen.blit(text_fortsetzen, (button_fortsetzen.x + 50, button_fortsetzen.y + 12))
        screen.blit(text_neustart, (button_neustart.x + 50, button_neustart.y + 12))
        screen.blit(text_beenden, (button_beenden.x + 60, button_beenden.y + 12))
        
        #Maus Hover Effekt
        maus_pos = pygame.mouse.get_pos()
        if button_fortsetzen.collidepoint(maus_pos):
            pygame.draw.rect(screen, (0, 200, 0), button_fortsetzen, border_radius=10)
            screen.blit(text_fortsetzen, (button_fortsetzen.x + 50, button_fortsetzen.y + 12))
        if button_neustart.collidepoint(maus_pos):
            pygame.draw.rect(screen, (200, 200, 0), button_neustart, border_radius=10)
            screen.blit(text_neustart, (button_neustart.x + 50, button_neustart.y + 12))
        if button_beenden.collidepoint(maus_pos):
            pygame.draw.rect(screen, (200, 0, 0), button_beenden, border_radius=10)
            screen.blit(text_beenden, (button_beenden.x + 60, button_beenden.y + 12))
        
        pygame.display.flip()
        
        #Event Handling für Pause Menü
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #Pause beenden und pausierte Zeit berechnen
                    pause_ende_zeit = pygame.time.get_ticks()
                    gesamte_pausen_dauer += (pause_ende_zeit - pause_start_zeit)
                    paused = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_fortsetzen.collidepoint(event.pos):
                    #Pause beenden und pausierte Zeit berechnen
                    pause_ende_zeit = pygame.time.get_ticks()
                    gesamte_pausen_dauer += (pause_ende_zeit - pause_start_zeit)
                    paused = False
                    return
                if button_neustart.collidepoint(event.pos):
                    #Spiel zurücksetzen
                    spiel_reset()
                    paused = False
                    return
                if button_beenden.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        clock.tick(30)  #Begrenzung für Pause-Menü

def zeichnen():
    #Hintergrundbild als "Weg"
    screen.blit(hintergrund, (0, 0))
    
    #Zeichnen der Wände, Start und Zielzell
    for z in range(ZEILEN):         #alle Zeilen
        for s in range(SPALTEN):    #alle Spalten
            x = s * GROESSE
            y = z * GROESSE
            
            #damit das Hintergrundbild als Weg erscheint.
            if z == 0 and s == 0:  #Start Zelle
                pygame.draw.rect(screen, TUERKIS, (x, y, GROESSE, GROESSE))
            elif z == ZEILEN-1 and s == SPALTEN-1: #Ziel Zelle
                pygame.draw.rect(screen, ROT, (x, y, GROESSE, GROESSE))
            
            #Wände zeichnen
            if waende[z][s][0]:  #oben
                pygame.draw.line(screen, GRAU, (x, y), (x+GROESSE, y), 5)
            if waende[z][s][1]:  #rechts
                pygame.draw.line(screen, GRAU, (x+GROESSE, y), (x+GROESSE, y+GROESSE), 5)
            if waende[z][s][2]:  #unten
                pygame.draw.line(screen, GRAU, (x, y+GROESSE), (x+GROESSE, y+GROESSE), 5)
            if waende[z][s][3]:  #links
                pygame.draw.line(screen, GRAU, (x, y), (x, y+GROESSE), 5)
    
    #Spieler (Gelber-Punkt) in mitte plazieren
    mitte_x = spieler_x * GROESSE + GROESSE // 2
    mitte_y = spieler_y * GROESSE + GROESSE // 2
    radius = GROESSE // 3

    #Squish berechnen in der Mitte der Animation am stärksten zerdrückt
    if squish_timer > 0:
        fortschritt = squish_timer / SQUISH_DAUER        #1.0 → 0.0
        squish = int(radius * 0.35 * fortschritt)        #35% kleiner
        rect = pygame.Rect(
            mitte_x - radius + squish,
            mitte_y - radius + squish,
            (radius - squish) * 2,
            (radius - squish) * 2,
        )
        pygame.draw.ellipse(screen, GELB, rect)
    else:
        pygame.draw.circle(screen, GELB, (mitte_x, mitte_y), radius)

#Funktion für Gewinnanimation
def zeige_gewinn(zeit):

    winner_pfad = os.path.join(skript_ordner, "winner.png")
    winner_bild = pygame.image.load(winner_pfad)
    winner_bild = pygame.transform.scale(winner_bild, (400, 300))
    
    #Warte auf Button-Klick
    while True:
        #Zuerst das Spiel im Hintergrund zeichnen
        zeichnen()
        
        #halbtransparenter Hintergrund
        overlay = pygame.Surface((600, 600))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        #Gewinn Bild
        bild_x = (600 - 400) // 2
        bild_y = (600 - 300) // 2 - 50
        screen.blit(winner_bild, (bild_x, bild_y))
        
        schrift = pygame.font.Font(None, 36)
        
        #Zeit
        zeit_text = schrift.render(f"Zeit: {zeit:.2f} Sekunden", True, (255, 255, 255))
        text_rect = zeit_text.get_rect(center=(300, bild_y + 320))
        screen.blit(zeit_text, text_rect)
        
        #Buttons
        button_neu = pygame.Rect(200, 450, 200, 50)
        button_beenden = pygame.Rect(200, 520, 200, 50)
        
        #Standard-Buttons
        pygame.draw.rect(screen, (0, 150, 0), button_neu, border_radius=10)
        pygame.draw.rect(screen, (150, 0, 0), button_beenden, border_radius=10)
        
        #Button Ränder
        pygame.draw.rect(screen, (255, 255, 255), button_neu, width=2, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), button_beenden, width=2, border_radius=10)
        
        text_neu = schrift.render("Neu Spielen", True, (255, 255, 255))
        text_beenden = schrift.render("Beenden", True, (255, 255, 255))
        screen.blit(text_neu, (button_neu.x + 35, button_neu.y + 12))
        screen.blit(text_beenden, (button_beenden.x + 50, button_beenden.y + 12))
        
        #Maus Hover Effekt
        maus_pos = pygame.mouse.get_pos()
        if button_neu.collidepoint(maus_pos):
            pygame.draw.rect(screen, (0, 200, 0), button_neu, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), button_neu, width=2, border_radius=10)
            screen.blit(text_neu, (button_neu.x + 35, button_neu.y + 12))
        if button_beenden.collidepoint(maus_pos):
            pygame.draw.rect(screen, (200, 0, 0), button_beenden, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), button_beenden, width=2, border_radius=10)
            screen.blit(text_beenden, (button_beenden.x + 50, button_beenden.y + 12))
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_neu.collidepoint(event.pos):
                    spiel_reset()
                    return
                if button_beenden.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        clock.tick(30)

#aktualisieren
zeichnen()
pygame.display.flip()

clock = pygame.time.Clock()  

while True:
    delta_time = clock.tick(40)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #ESC Taste für Pause Menü
        if spiel_aktiv and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = True
            zeige_pause_menue()
            continue  # Rest der Schleife überspringen nach Pause
        
        #Nur wenn Spiel aktiv ist, Steuerung erlauben (und nicht pausiert)
        if spiel_aktiv and not paused and event.type == pygame.KEYDOWN:
            bewegt = False  #schaut ob Bewegung statt findet
            
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                #checkt ob keine Wand nach oben
                if not waende[spieler_y][spieler_x][0]:
                    spieler_y -= 1
                    bewegt = True  
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                #nach unten
                if not waende[spieler_y][spieler_x][2]:
                    spieler_y += 1
                    bewegt = True  
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                #nach links
                if not waende[spieler_y][spieler_x][3]:
                    spieler_x -= 1
                    bewegt = True  
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                #nach recht
                if not waende[spieler_y][spieler_x][1]:
                    spieler_x += 1
                    bewegt = True  
            
            #wenn bewegt = True
            if bewegt:
                move_sound.play()
                squish_timer = SQUISH_DAUER

    #Squish-Timer herunterzählen
    if squish_timer > 0:
        squish_timer -= delta_time
        if squish_timer < 0:
            squish_timer = 0

    #Timer mit Pausenkorrektur
    if spiel_aktiv and not paused:
        aktuelle_zeit = pygame.time.get_ticks()
        verstrichen = (aktuelle_zeit - start_zeit - gesamte_pausen_dauer) / 1000.0
    else:
        verstrichen = 0

    #Überprüfung ob Ziel erreicht
    if spiel_aktiv and not paused and spieler_x == SPALTEN-1 and spieler_y == ZEILEN-1:
        spiel_aktiv = False
        end_zeit = pygame.time.get_ticks()
        benoetigte_zeit = (end_zeit - start_zeit - gesamte_pausen_dauer) / 1000.0
        pygame.mixer.music.stop()  #Hintergrundmusik stoppen
        win_sound.play()           #Gewinnersound abspielen
        zeige_gewinn(benoetigte_zeit)

    #aktualisieren
    zeichnen()
    pygame.display.flip()