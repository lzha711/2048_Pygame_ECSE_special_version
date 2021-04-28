import pygame, sys, time
from pygame.locals import *  # copy all names in pygame.locals into my namespace. save typing
from colours import *
from random import *  # random is a built-in module that generate pseudo-random number
from images import *

TOTAL_POINTS = 0
DEFAULT_SCORE = 2
BOARD_SIZE = 4

pygame.init() # initialize pygame module

SURFACE = pygame.display.set_mode((400, 500), 0, 32) # second arg: flag, collection of additional option. third arg: depth: represent the number of bits to use for color
pygame.display.set_caption("2048 ECSE Lecturers Version")

# initialize the image tile, need to import blank image first
tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoMat = []

myfont = pygame.font.SysFont("monospace", 20, bold=True, italic=False)
scorefont = pygame.font.SysFont("comicsansms", 30)

def main(fromLoaded=False): # defined boolean variable and set the default function argument as this variable
    if not fromLoaded:
        printInfo()
        placeRandomTile()
    # printMatrix()

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if checkIfCanGo() == True:
                if event.type == KEYDOWN: # if the keyboard button is pressed
                    if isArrow(event.key):
                        rotations = getRotations(event.key)
                        addToUndo()

                        for i in range(0, rotations):
                            rotateMatrixClockwise()

                        if canMove():
                            moveTiles()
                            mergeTiles()
                            placeRandomTile()
                           # print(undoMat)

                        for j in range(0, (4 - rotations) % 4):
                            rotateMatrixClockwise()

                        printMatrix()
            else:
                printGameOver()

            if event.type == KEYDOWN:
                global BOARD_SIZE

                if event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_u:
                    undo()

            if checkifwin() == True:
                printWinning()

        pygame.display.update()

# print information board
def printInfo():
    SURFACE.fill(LIGHT_GREY)
    infofont = pygame.font.SysFont("comicsansms", 20)
    titleline = infofont.render("2048 ECSE Lecturers Version:", 1, LIGHT_ORANGE)
    firstline = infofont.render("This game is an image version", 1, BLACK)
    secondline = infofont.render("of the classic game 2048, the", 1, BLACK)
    thirdline = infofont.render("profile images are all screenshots", 1, BLACK)
    forthline = infofont.render("from UOA web pages, ", 1, BLACK)
    line5 = infofont.render("This game is created purely for fun, ", 1, RED)
    line6 = infofont.render("no meaning is behind the game logic.", 1, RED)
    line7 = infofont.render("Press any arrow keys (<-->) to start :)", 1, LIGHT_ORANGE)
    line8 = infofont.render("Merry Christmas 2019!", 1, RED)
    nameline = infofont.render("--Lily Zhang", 1, BLACK)

    SURFACE.blit(titleline, (20, 10))
    SURFACE.blit(firstline,(50,50))
    SURFACE.blit(secondline, (50, 100))
    SURFACE.blit(thirdline, (50, 150))
    SURFACE.blit(forthline, (50, 200))
    SURFACE.blit(line5, (30, 250))
    SURFACE.blit(line6, (30, 300))
    SURFACE.blit(line7, (30, 370))
    SURFACE.blit(line8, (150, 420))
    SURFACE.blit(nameline, (250, 450))

# display the tile matrix
def printMatrix():

    SURFACE.fill(LIGHT_PINK)
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            num_reference = [2,4,6,8,16,32,64,128,256,512,1024,2048]
            for k in num_reference:
                if tileMatrix[i][j] == k:
                    SURFACE.blit(image_dict[k], (i * (400 / BOARD_SIZE), j * (400 / BOARD_SIZE) + 100))

            scorefont = pygame.font.SysFont("comicsansms", 30)
            label1 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, DARK_GREY)
            label2 = scorefont.render("r: reset", 1, LIGHT_ORANGE)
            label3 = scorefont.render("u: undo", 1, LIGHT_ORANGE)
            SURFACE.blit(label1, (10, 20))
            SURFACE.blit(label2, (250, 0))
            SURFACE.blit(label3, (250, 30))

def printGameOver():

    SURFACE.fill(DARK_GREY)

    label = scorefont.render("Game Over!", 1, ORANGE)
    label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, WHITE)
    label3 = myfont.render("Press r to restart...", 1, WHITE)

    SURFACE.blit(label, (50, 100))
    SURFACE.blit(label2, (50, 200))
    SURFACE.blit(label3, (50, 300))

def checkifwin():
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if tileMatrix[i][j] >= 2048:
                return True
    return False

def printWinning():

    win_label = scorefont.render("Congrats! You win!", 1, ORANGE)
    reset_label = scorefont.render("Press r to restart...", 1, GREEN)
    SURFACE.blit(win_label, (60,60))
    SURFACE.blit(reset_label, (40, 200))

# Place number 2 in a random chosen tile:
# step--1: generate a random integer k \in [0,15]
# step--2: put number 2 at tileMatrix[floor(k/4)][k%4], if this place is empty
def placeRandomTile():
    count = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if tileMatrix[i][j] == 0:
                count += 1

    k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0:
        k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2

def floor(n):
    return int(n - (n % 1))

# moving up is set as the default moving state. Moving down/left/right can be derived by rotating the tile matrix
def moveTiles():
    # We want to work column by column shifting up each element in turn.
    for i in range(0, BOARD_SIZE):  # Work through our 4 columns.
        for j in range(0, BOARD_SIZE - 1):  # Now consider shifting up each element by checking top 3 elements if 0.
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:  # If any element is 0 and there is a number to shift we want to shift up elements below.
                for k in range(j, BOARD_SIZE - 1):  # Move up elements below.
                    tileMatrix[i][k] = tileMatrix[i][k + 1]  # Move up each element one.
                tileMatrix[i][BOARD_SIZE - 1] = 0


def mergeTiles():
    global TOTAL_POINTS
    for i in range(0, BOARD_SIZE):
        for k in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k] * 2
                tileMatrix[i][k + 1] = 0
                TOTAL_POINTS += tileMatrix[i][k]
                moveTiles()


def checkIfCanGo():
    # another way to loop through the 2D matrix
    for i in range(0, BOARD_SIZE ** 2):
        if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
            return True

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][j] == tileMatrix[i][j + 1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
                return True
    return False


def reset():
    global TOTAL_POINTS
    global tileMatrix

    TOTAL_POINTS = 0
    SURFACE.fill(LIGHT_PINK)

    tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]

    main()


def canMove():
    for i in range(0, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if tileMatrix[i][j - 1] == 0 and tileMatrix[i][j] > 0:
                return True
            elif (tileMatrix[i][j - 1] == tileMatrix[i][j]) and tileMatrix[i][j - 1] != 0:
                return True

    return False


def rotateMatrixClockwise():
    for i in range(0, int(BOARD_SIZE / 2)):
        for k in range(i, BOARD_SIZE - i - 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

            tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
            tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
            tileMatrix[i][k] = temp4

# cheked if the pressed key is arrow button
def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)


def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


def convertToLinearMatrix():
    mat = []

    for i in range(0, BOARD_SIZE ** 2):
        mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

    mat.append(TOTAL_POINTS)

    return mat


def addToUndo():
    undoMat.append(convertToLinearMatrix())


def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()

        for i in range(0, BOARD_SIZE ** 2):
            tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = mat[i]

        global TOTAL_POINTS
        TOTAL_POINTS = mat[BOARD_SIZE ** 2]

        printMatrix()

main()
