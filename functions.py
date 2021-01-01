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

def enemy(x, y, number):
    screen.blit(enemyImage[number], (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fired"
    screen.blit(bulletImage, (x, y))

def dropHomework(x, y, number):
    global homeworkState
    homeworkState[number] = "dropped"
    screen.blit(homeworkImage[number], (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    midEnemyX = enemyX + 32
    midEnemyY = enemyY + 32
    midBulletX = bulletX + 5.5
    midBulletY = bulletY + 22.5
    distanceX = abs(midEnemyX - midBulletX)
    distanceY = abs(midEnemyY - midBulletY)
    if distanceX < 37.5 and distanceY < 54.5 and bulletState == "fired":
        return True
    else:
        return False

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
                print("found it first")
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