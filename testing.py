import random

import pygame
from pygame import mixer

import csv

pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))

scoreRecorded = False
running = False

# background
background = pygame.image.load('hell back.png')

# background music
mixer.music.load("think about this.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Kewl game")
icon = pygame.image.load('ufo logo.png')
pygame.display.set_icon(icon)

playerImage = pygame.image.load('edgy kid.png')
playerX = 370
playerY = 440
playerXChange = 0

# enemy stuff
enemyImage = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
numberOfEnemies = 6

highscore = 0

# make enemies
for num in range (numberOfEnemies):
    enemyImage.append(pygame.image.load('school.png'))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(3)
    enemyYChange.append(40)

# bullet stuff
bulletImage = pygame.image.load('baguette.png')
bulletX = 0
bulletY = 440
bulletXChange = 0
bulletYChange = 4
bulletState = "ready"

# score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
gameOverFont = pygame.font.Font('freesansbold.ttf', 35)

highScoreFont = pygame.font.Font('freesansbold.ttf', 32)


# functions for stuff
def getHighScore(highscore):
    with open('scores.csv', newline='') as scores:
        allTheScores = csv.reader(scores, delimiter=' ', quotechar='|')
        for row in allTheScores:
            aScore = int(row[0])
            if aScore > highscore:
                highscore = aScore
    return highscore

highscore = getHighScore(highscore)

def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOverText():
    gameOverText = gameOverFont.render("YOU LOST, YOU MASSIVE DISAPPOINTMENT", True, (255, 255, 255))
    screen.blit(gameOverText, (10, 250))

def highScoreText():
    highScoreText = highScoreFont.render("High score: " + str(highscore), True, (255, 255, 255))
    screen.blit(highScoreText, (550, 10))

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y, number):
    screen.blit(enemyImage[number], (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fired"
    screen.blit(bulletImage, (x + 35, y - 40))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
    if distance < 40:
        return True
    else:
        return False

def show_start_screen():
    start_screen = True
    game_running=True
    while start_screen:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        highScoreText()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                game_running=False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_screen = False

        showScore(textX, textY)
        pygame.display.update()

    return game_running

#===============================================================
# Main Game Starts here
#===============================================================

highscoreUpdated = False
game_running=True

game_running = show_start_screen()

while game_running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    highScoreText()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                scoreValue += 10

    showScore(textX, textY)
    pygame.display.update()
