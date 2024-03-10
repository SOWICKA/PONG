import pygame
import sys
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox

def ekran_powitalny():
    root = tk.Tk()
    root.withdraw()

    instrukcje_pl = """
    Witaj w grze "KAMILOWY Pong"!

    Autor: Kamil S.

    Zasady gry:
    Sterowanie graczem:
    - Poruszaj paletką w lewo i w prawo, używając myszy lub strzałek.

    Cel gry:
    - Odbijaj piłkę paletką tak, aby przeciwnik nie zdołał jej odbić.
    - Za każdym razem, gdy przeciwnik nie odbije piłki, zdobywasz punkt.

    Gra kończy się, gdy:
    - Jeden z graczy zdobędzie 11 punktów.

    Naciśnij OK, aby rozpocząć!
    """

    instrukcje_en = """
    Welcome to the game "KAMILOWY Pong"!

    Author: Kamil S.

    Game Rules:
    Player Controls:
    - Move the paddle left and right using the mouse or arrow keys.

    Objective:
    - Bounce the ball off the paddle so that the opponent fails to return it.
    - Each time the opponent misses the ball, you score a point.

    The game ends when:
    - One of the players reaches 11 points.

    Press OK to start!
    """

    lang_choice = messagebox.askquestion("Language Selection", "Choose language:\n\nEnglish - Yes\nPolski - No")

    if lang_choice == 'yes':
        result = messagebox.showinfo("Welcome to the game!", instrukcje_en)
    else:
        result = messagebox.showinfo("Witaj w grze!", instrukcje_pl)

    if result == "ok":
        return True
    else:
        return False

def gra():
    pygame.init()

    OKNOGRY_SZER = 800
    OKNOGRY_WYS = 400
    LT_BLUE = (230, 255, 255)

    oknogry = pygame.display.set_mode((OKNOGRY_SZER, OKNOGRY_WYS), 0, 32)
    pygame.display.set_caption('KAMILOWY Pong')

    PALETKA_SZER = 100
    PALETKA_WYS = 20
    BLUE = (0, 0, 255)
    PALETKA_1_POZ = (350, 360)
    paletka1 = pygame.Surface([PALETKA_SZER, PALETKA_WYS])
    paletka1.fill(BLUE)
    paletka1_prost = paletka1.get_rect()
    paletka1_prost.x = PALETKA_1_POZ[0]
    paletka1_prost.y = PALETKA_1_POZ[1]

    P_SZER = 20
    P_WYS = 20
    P_PREDKOSC_X = 3.5
    P_PREDKOSC_Y = 3.5
    GREEN = (0, 255, 0)
    pilka = pygame.Surface([P_SZER, P_WYS], pygame.SRCALPHA, 32).convert_alpha()
    pygame.draw.ellipse(pilka, GREEN, [0, 0, P_SZER, P_WYS])
    pilka_prost = pilka.get_rect()
    pilka_prost.x = OKNOGRY_SZER / 2
    pilka_prost.y = OKNOGRY_WYS / 2

    tlo = pygame.image.load('tlo.jpeg').convert()
    tlo = pygame.transform.scale(tlo, (OKNOGRY_SZER, OKNOGRY_WYS))

    FPS = 70
    fpsClock = pygame.time.Clock()

    RED = (255, 0, 0)
    PALETKA_AI_POZ = (350, 20)
    paletkaAI = pygame.Surface([PALETKA_SZER, PALETKA_WYS])
    paletkaAI.fill(RED)
    paletkaAI_prost = paletkaAI.get_rect()
    paletkaAI_prost.x = PALETKA_AI_POZ[0]
    paletkaAI_prost.y = PALETKA_AI_POZ[1]
    PREDKOSC_AI = 2.5

    PKT_1 = '0'
    PKT_AI = '0'
    fontObj = pygame.font.Font('freesansbold.ttf', 64)

    def drukuj_punkty1():
        tekst1 = fontObj.render(PKT_1, True, (0, 0, 0))
        tekst_prost1 = tekst1.get_rect()
        tekst_prost1.center = (OKNOGRY_SZER / 2, OKNOGRY_WYS * 0.75)
        oknogry.blit(tekst1, tekst_prost1)

    def drukuj_punktyAI():
        tekstAI = fontObj.render(PKT_AI, True, (0, 0, 0))
        tekst_prostAI = tekstAI.get_rect()
        tekst_prostAI.center = (OKNOGRY_SZER / 2, OKNOGRY_WYS / 4)
        oknogry.blit(tekstAI, tekst_prostAI)

    pygame.key.set_repeat(50, 25)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEMOTION:
                myszaX, myszaY = event.pos
                przesuniecie = myszaX - (PALETKA_SZER / 2)
                przesuniecie = max(0, min(OKNOGRY_SZER - PALETKA_SZER, przesuniecie))

                if przesuniecie > OKNOGRY_SZER - PALETKA_SZER:
                    przesuniecie = OKNOGRY_SZER - PALETKA_SZER
                if przesuniecie < 0:
                    przesuniecie = 0
                paletka1_prost.x = przesuniecie

        pilka_prost.move_ip(P_PREDKOSC_X, P_PREDKOSC_Y)

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            paletka1_prost.x -= 4
            if paletka1_prost.x < 0:
                paletka1_prost.x = 0
        if keys[K_RIGHT]:
            paletka1_prost.x += 4
            if paletka1_prost.x > OKNOGRY_SZER - PALETKA_SZER:
                paletka1_prost.x = OKNOGRY_SZER - PALETKA_SZER

        if pilka_prost.right >= OKNOGRY_SZER:
            P_PREDKOSC_X *= -1
        if pilka_prost.left <= 0:
            P_PREDKOSC_X *= -1

        if pilka_prost.top <= 0:
            P_PREDKOSC_Y *= -1
            pilka_prost.x = OKNOGRY_SZER / 2
            pilka_prost.y = OKNOGRY_WYS / 2
            PKT_1 = str(int(PKT_1) + 1)

        if pilka_prost.bottom >= OKNOGRY_WYS:
            pilka_prost.x = OKNOGRY_SZER / 2
            pilka_prost.y = OKNOGRY_WYS / 2
            PKT_AI = str(int(PKT_AI) + 1)

        if int(PKT_1) == 11 or int(PKT_AI) == 11:
            winner = "GRACZ" if int(PKT_1) == 11 else "KOMPUTER"
            pygame.quit()

            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()
            result = messagebox.showinfo("Koniec gry", f"{winner} wygrywa!")

            if result == "ok":
                return

        if pilka_prost.centerx > paletkaAI_prost.centerx:
            paletkaAI_prost.x += PREDKOSC_AI
        elif pilka_prost.centerx < paletkaAI_prost.centerx:
            paletkaAI_prost.x -= PREDKOSC_AI

        if pilka_prost.colliderect(paletkaAI_prost):
            P_PREDKOSC_Y *= -1
            pilka_prost.top = paletkaAI_prost.bottom

        if pilka_prost.colliderect(paletka1_prost):
            P_PREDKOSC_Y *= -1
            pilka_prost.bottom = paletka1_prost.top

        oknogry.blit(tlo, (0, 0))

        drukuj_punkty1()
        drukuj_punktyAI()

        oknogry.blit(paletka1, paletka1_prost)
        oknogry.blit(paletkaAI, paletkaAI_prost)

        oknogry.blit(pilka, pilka_prost)

        pygame.display.update()

        fpsClock.tick(FPS)

if ekran_powitalny():
    gra()
