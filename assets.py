"""
assets.py
This file is responsible for storing all constants and loading all the assets.

Author: Allyn Bao
Date last modified: 9/9/2021
"""

import pygame
import os

pygame.font.init()
pygame.mixer.init()

"""
Constants
"""
# parameters
LEN = 550
MAZE_SIZE = 43
BLOCK_SIZE = LEN // 11
CHARACTER_PADDING = BLOCK_SIZE // 6
FPS = 90
TIME = 1  # min
TREAS_DENSITY = 10  # a unit of treasure in # x # of blocks
TREAS_PADDING = MAZE_SIZE % TREAS_DENSITY - 1
TREAS_NUM_PER_ROW = (MAZE_SIZE - TREAS_PADDING) // TREAS_DENSITY
SPEED = int(BLOCK_SIZE * 0.08)
GARD_SPEED = int(BLOCK_SIZE * 0.1)

# keyboard
START_KEY = pygame.K_SPACE
KEYBOARD = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]

# colour
GREEN = (0, 250, 154)
BACKGROUND_COLOUR = (19, 41, 37)
FINAL_FONT_COLOUR = (11, 29, 7)
ADDITIONAL_FONT_COLOUR = (160, 203, 138)
PROGRESS_BACK_COLOUR = (80, 82, 101)
PROGRESS_TOP_COLOUR = (160, 203, 138)
PAST_SCORES_FONT_COLOUR = (27, 45, 30)

# fonts
SCORE_FONT_SIZE = BLOCK_SIZE // 2
SCORE_FONT = pygame.font.SysFont("San Francisco", SCORE_FONT_SIZE)
FINAL_FONT_SIZE = BLOCK_SIZE * 2
FINAL_FONT = pygame.font.SysFont("San Francisco", FINAL_FONT_SIZE)
ADDITIONAL_FONT = pygame.font.SysFont("San Francisco", FINAL_FONT_SIZE // 2)
PAST_SCORE_FONT = pygame.font.SysFont("San Francisco", FINAL_FONT_SIZE // 3)

# images
GUIDE_IMG = pygame.image.load(os.path.join("Assets", "startGuide.png"))
PATH_IMG = pygame.image.load(os.path.join("Assets", "grassPath.png"))
WALL_IMG = pygame.image.load(os.path.join("Assets", "mossyGreenBrick.png"))
TRAP_WALL_IMG = pygame.image.load(os.path.join("Assets", "circularSaw.png"))
TREAS_IMG = pygame.image.load(os.path.join("Assets", "magicStone.png"))
BAR_IMG = pygame.image.load(os.path.join("Assets", "greenBottomBar.png"))
BACKGROUND_IMG = pygame.image.load(os.path.join("Assets", "blurBackground.png"))
REPLAY_IMG = pygame.image.load(os.path.join("Assets", "replayButton.png"))
QUIT_IMG = pygame.image.load(os.path.join("Assets", "quitButton.png"))
PRESSED_REPLAY_IMG = pygame.image.load(os.path.join("Assets", "pressedReplayButton.png"))
PRESSED_QUIT_IMG = pygame.image.load(os.path.join("Assets", "pressedQuitButton.png"))
# player img
PLAYER_IMG_LIST = []
# up
PLAYER_IMG_1 = pygame.image.load(os.path.join("Assets", "player_img", "player_up_1.png"))
PLAYER_IMG_2 = pygame.image.load(os.path.join("Assets", "player_img", "player_up_still.png"))
PLAYER_IMG_3 = pygame.image.load(os.path.join("Assets", "player_img", "player_up_2.png"))
PLAYER_IMG_LIST.append([PLAYER_IMG_1, PLAYER_IMG_2, PLAYER_IMG_3, PLAYER_IMG_2])
# down
PLAYER_IMG_4 = pygame.image.load(os.path.join("Assets", "player_img", "player_down_1.png"))
PLAYER_IMG_5 = pygame.image.load(os.path.join("Assets", "player_img", "player_down_still.png"))
PLAYER_IMG_6 = pygame.image.load(os.path.join("Assets", "player_img", "player_down_2.png"))
PLAYER_IMG_LIST.append([PLAYER_IMG_4, PLAYER_IMG_5, PLAYER_IMG_6, PLAYER_IMG_5])
# left
PLAYER_IMG_7 = pygame.image.load(os.path.join("Assets", "player_img", "player_left_1.png"))
PLAYER_IMG_8 = pygame.image.load(os.path.join("Assets", "player_img", "player_left_still.png"))
PLAYER_IMG_9 = pygame.image.load(os.path.join("Assets", "player_img", "player_left_2.png"))
PLAYER_IMG_LIST.append([PLAYER_IMG_7, PLAYER_IMG_8, PLAYER_IMG_9, PLAYER_IMG_8])
# right
PLAYER_IMG_10 = pygame.image.load(os.path.join("Assets", "player_img", "player_right_1.png"))
PLAYER_IMG_11 = pygame.image.load(os.path.join("Assets", "player_img", "player_right_still.png"))
PLAYER_IMG_12 = pygame.image.load(os.path.join("Assets", "player_img", "player_right_2.png"))
PLAYER_IMG_LIST.append([PLAYER_IMG_10, PLAYER_IMG_11, PLAYER_IMG_12, PLAYER_IMG_11])

# formatted images
guide_view = pygame.transform.scale(GUIDE_IMG, (BLOCK_SIZE * 11, BLOCK_SIZE * 11))
path_view = pygame.transform.scale(PATH_IMG, (BLOCK_SIZE, BLOCK_SIZE))
wall_view = pygame.transform.scale(WALL_IMG, (BLOCK_SIZE, BLOCK_SIZE))
trap_wall_view = pygame.transform.scale(TRAP_WALL_IMG, (BLOCK_SIZE, BLOCK_SIZE))
treas_view = pygame.transform.scale(TREAS_IMG, (BLOCK_SIZE, BLOCK_SIZE))
bar_view = pygame.transform.scale(BAR_IMG, (BLOCK_SIZE * 11, BLOCK_SIZE))
replay_view = pygame.transform.scale(REPLAY_IMG, (BLOCK_SIZE * 5, BLOCK_SIZE))
quit_view = pygame.transform.scale(QUIT_IMG, (BLOCK_SIZE * 5, BLOCK_SIZE))
pressed_replay_view = pygame.transform.scale(PRESSED_REPLAY_IMG, (BLOCK_SIZE * 5, BLOCK_SIZE))
pressed_quit_view = pygame.transform.scale(PRESSED_QUIT_IMG, (BLOCK_SIZE * 5, BLOCK_SIZE))
background_view = pygame.transform.scale(BACKGROUND_IMG, (BLOCK_SIZE * 11, BLOCK_SIZE * 12))

# sound
START_GAME_SOUND = pygame.mixer.Sound(os.path.join("Assets", "startGame.mp3"))
COLLECTED_SOUND = pygame.mixer.Sound(os.path.join("Assets", "collected.mp3"))
TIMES_UP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "timesUp.mp3"))
PLAYER_KILLED_SOUND = pygame.mixer.Sound(os.path.join("Assets", "playerKilled.mp3"))
BUTTON_SOUND = pygame.mixer.Sound(os.path.join("Assets", "pushButton.mp3"))
