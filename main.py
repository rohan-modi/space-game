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
startGameFont = pygame.font.Font('freesansbold.ttf', 32)


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

def startGameText():
    startGameText = startGameFont.render("Press s to start the game", True, (255, 255, 255))
    screen.blit(startGameText, (200, 250))

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
        startGameText()
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

highscoreUpdated = False
running = True

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
    if highscoreUpdated == False:
        highScoreText()
        highscoreUpdated = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bulletState == "ready":
                    # fire bullet
                    bulletSound = mixer.Sound("goat scream short.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
            if event.key == pygame.K_LEFT:
                playerXChange =  -4
            if event.key == pygame.K_RIGHT:
                playerXChange = 4
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
    # player border security
    playerX += playerXChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 710:
        playerX = 710

    # bullet border
    if bulletY <= 0:
        bulletY = 400
        bulletState = "ready"

    # move bullet
    if bulletState == "fired":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange
    
    # enemy movement
    for number in range(numberOfEnemies):
    # Game over
        if enemyY[number] > 365:
            for num in range(numberOfEnemies):
                enemyY[num] = 1000
            if scoreRecorded == False:
                scoreValue = str(scoreValue)
                scoreValue = f"{scoreValue}\n"
                f = open("scores.csv", "a")
                f.write(scoreValue)
                f.close()
                scoreRecorded = True
                scoreValue = int(scoreValue)
            gameOverText()
            break

        enemyX[number] += enemyXChange[number]
        if enemyX[number] <= 0:
            enemyXChange[number] = 3
            enemyY[number] += enemyYChange[number]
        elif enemyX[number] >= 736:
            enemyXChange[number] = -3
            enemyY[number] += enemyYChange[number]
        # collision
        collision = isCollision(enemyX[number], enemyY[number], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("grenade.wav")
            explosionSound.play()
            bulletY = 400
            bulletState = "ready"
            scoreValue += 1
            enemyX[number] = random.randint(0, 700)
            enemyY[number] = random.randint(50, 150)
        
        enemy(enemyX[number], enemyY[number], number)

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()