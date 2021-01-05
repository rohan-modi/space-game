import random

import pygame
from pygame import mixer

import csv
notwith open("scores.csv","a+") as f:
    f.write("0\n")

pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('hell back.png')

# background music
mixer.music.load("think about this.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Kewl game")
icon = pygame.image.load('ufo logo.png')
pygame.display.set_icon(icon)

# player stuff
playerImage = pygame.image.load('edgy kid.png')
playerY = 440
playerXChange = 0

numberOfEnemies = 5

# lonely images
homeworkImage = pygame.image.load('homework.png')

# fonts
gameOverFont = pygame.font.Font('freesansbold.ttf', 35)
highScoreFont = pygame.font.Font('freesansbold.ttf', 32)
startGameFont = pygame.font.Font('freesansbold.ttf', 32)
instructionsFont = pygame.font.Font('freesansbold.ttf', 32)
restartFont = pygame.font.Font('freesansbold.ttf', 35)

# score stuff
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
highscore = 0

# bullet stuff, baguette size 11 x 45
bulletImage = pygame.image.load('baguette.png')
bulletYChange = 5

# classes for stuff
class enemy(): 
    def __init__(self):
        enemyImage.append(pygame.image.load('school.png'))
        thisEnemyX = random.randint(0, 700)
        thisEnemyY = random.randint(50, 150)
        enemyX.append(thisEnemyX)
        enemyY.append(thisEnemyY)
        enemyXChange.append(3)
        enemyYChange.append(40)
        enemySpeed.append(3)

    def move(self, number):
        global scoreRecorded
        global scoreValue
        if enemyY[number] > 365:
            dead = True
            for num in range(numberOfEnemies):
                enemyY[num] = 1000
            if scoreRecorded == False:
                scoreValue = str(scoreValue)
                scoreValue = f"{scoreValue}\n"
                with open("scores.csv","a+") as f:
                    f.write(scoreValue)
                f = open("scores.csv", "a")
                f.write(scoreValue)
                scoreRecorded = True
                scoreValue = int(scoreValue)
            gameOverText()
            restartText()

class homework():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        homeworkX.append(self.x)
        homeworkY.append(self.y)
        homeworkYChange.append(2)
        homeworkState.append("ready")

    def move(self, number):
        homeworkY[number] += homeworkYChange[number]
        homeworkState[number] = "dropped"
        screen.blit(homeworkImage, (homeworkX[number], homeworkY[number]))

class bullet():
    def __init__(self, playerX):
        global bulletState
        self.bulletX = playerX
        bulletSound = mixer.Sound("goat scream short.wav")
        bulletSound.play()
        bulletX = playerX + 55
        bulletState = "fired"
    
    def move(self):
        global bulletY
        global bulletState
        global scoreValue
        bulletY -= bulletYChange
        screen.blit(bulletImage, (self.bulletX, bulletY))
        for number in range (numberOfEnemies):
            midEnemyX = enemyX[number] + 32
            midEnemyY = enemyY[number] + 32
            midBulletX = self.bulletX + 5.5
            midBulletY = bulletY + 22.5
            distanceX = abs(midEnemyX - midBulletX)
            distanceY = abs(midEnemyY - midBulletY)
            if distanceX < 37.5 and distanceY < 54.5 and bulletState == "fired":
                explosionSound = mixer.Sound("grenade.wav")
                explosionSound.play()
                bulletY = 390
                bulletState = "ready"
                scoreValue += 1
                enemyX[number] = random.randint(0, 700)
                enemyY[number] = random.randint(50, 150)
                enemySpeed[number] += 0.5

# functions for stuff
def getHighScore(highscore):
    with open('scores.csv', newline='') as scores:
        allTheScores = csv.reader(scores, delimiter=' ', quotechar='|')
        for row in allTheScores:
            aScore = int(row[0])
            if aScore > highscore:
                highscore = aScore
    return highscore

def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOverText():
    gameOverText = gameOverFont.render("YOU LOST, YOU MASSIVE DISAPPOINTMENT", True, (255, 255, 255))
    screen.blit(gameOverText, (10, 250))

def restartText():
    restartText = restartFont.render("PRESS R TO PLAY AGAIN", True, (255, 255, 255))
    screen.blit(restartText, (200, 300))

def highScoreText():
    highScoreText = highScoreFont.render("High score: " + str(highscore), True, (255, 255, 255))
    textWidth = highScoreText.get_width()
    screen.blit(highScoreText, (780 - textWidth, 10))

def startGameText():
    startGameText = startGameFont.render("Press s to start the game", True, (255, 255, 255))
    screen.blit(startGameText, (200, 250))

def instructionsText():
    instructionsText = instructionsFont.render("Use the arrow keys to move and shoot", True, (255, 255, 255))
    screen.blit(instructionsText, (100, 220))

def player(x, y):
    screen.blit(playerImage, (x, y))

def drawEnemy(x, y, number):
    screen.blit(enemyImage[number], (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fired"
    screen.blit(bulletImage, (x, y))

def isKilled(playerX, playerY, homeworkX, homeworkY):
    if homeworkY >= 440 and homeworkY <= 540:
        midPlayerX = playerX + 50
        midHomeworkX = homeworkX + 16
        distanceX = abs(midPlayerX - midHomeworkX)
        if distanceX <= 66:
            game_running = False
            return True

def show_start_screen():
    start_screen = True
    game_running = True
    while start_screen:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        highScoreText()
        startGameText()
        instructionsText()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                game_running = False
                global playing
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_screen = False

        showScore(textX, textY)
        pygame.display.update()

    return game_running

# Giant loop
playing = True
while playing == True:

    scoreRecorded = False
    running = False
    dead = False
    restart = False
    bulletY = 390
    playerX = 370

    # enemy stuff, enemy size 64 x 64
    enemyImage = []
    enemyX = []
    enemyY = []
    enemyXChange = []
    enemyYChange = []
    enemySpeed = []

    # score
    scoreValue = 0

    # make enemies
    for number in range (numberOfEnemies):
        enemy()

    # homework stuff
    homeworkX = []
    homeworkY = []
    homeworkYChange = []
    homeworkState = []

    # make homework
    for number in range (numberOfEnemies):
        coordinateX = enemyX[number] + 32
        coordinateY = enemyY[number] + 64
        homework(coordinateX, coordinateY)

    # bullet stuff
    bulletX = 0
    bulletY = 390
    bulletState = "ready"

    highscore = getHighScore(highscore)
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
        for number in range(numberOfEnemies):
            drawEnemy(enemyX[number], enemyY[number], number)
        if highscoreUpdated == False:
            highScoreText()
            highscoreUpdated = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False
                playing = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_r) and (dead):
                    restart = True
                if event.key == pygame.K_UP:
                    if bulletState == "ready":
                        # fire bullet
                        baguette = bullet(playerX + 52)
                if event.key == pygame.K_LEFT:
                    playerXChange =  -4
                if event.key == pygame.K_RIGHT:
                    playerXChange = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerXChange = 0
        if restart:
            break
        # player border security
        playerX += playerXChange
        if playerX <= 0:
            playerX = 0
        elif playerX >= 710:
            playerX = 710

        # bullet border
        if bulletY <= 0:
            bulletY = 390
            bulletState = "ready"

        # move bullet
        if bulletState == "fired":
            baguette.move()

        # homework border
        for number in range(numberOfEnemies):
            if homeworkY[number] >= 768:
                homeworkY[number] = enemyY[number] + 64
                homeworkState[number] = "ready"

        for number in range(numberOfEnemies):
            if homeworkState[number] == "ready":
                # drop homework
                homeworkX[number] = enemyX[number] + 32
                homeworkY[number] = enemyY[number] + 64
                bomb = homework(homeworkX[number], homeworkY[number])
                homeworkState[number] = "dropped"

        # homework movement
        for number in range(numberOfEnemies):
            if homeworkState[number] == "dropped":
                # move homework
                bomb.move(number)

        # enemy movement
        for number in range(numberOfEnemies):
            school = enemy()
            school.move(number)
            # Game over
            if dead:
                break
        for number in range(numberOfEnemies):
            if isKilled(playerX, playerY, homeworkX[number], homeworkY[number]):
                dead = True
                for num in range(numberOfEnemies):
                        enemyY[num] = 1000
                        homeworkY[num] = 1000
                if scoreRecorded == False:
                    scoreValue = str(scoreValue)
                    scoreValue = f"{scoreValue}\n"
                    f = open("scores.csv", "a")
                    f.write(scoreValue)
                    f.close()
                    scoreRecorded = True
                    scoreValue = int(scoreValue)
                gameOverText()
                restartText()
                break
        for number in range(numberOfEnemies):
            enemyX[number] += enemyXChange[number]
            if enemyX[number] <= 0:
                enemyXChange[number] = enemySpeed[number]
                enemyY[number] += enemyYChange[number]
            elif enemyX[number] >= 736:
                enemyXChange[number] = -enemySpeed[number]
                enemyY[number] += enemyYChange[number]
            # collision

        player(playerX, playerY)
        showScore(textX, textY)
        pygame.display.update()