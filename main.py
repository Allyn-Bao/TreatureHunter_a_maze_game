"""
Main.py
This file contains main game loop and all necessary functions.
Run the script to start the game.

Author: Allyn Bao
Date last modified: 9/9/2021
"""

import pygame
from maze import Maze
from assets import *
from random import randint
from datetime import datetime, timedelta
import sqlite3
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

# game preparation
WIN = pygame.display.set_mode((LEN, LEN + LEN // 11))
pygame.display.set_caption("aMAZEing Fortune")
pygame.display.set_icon(pygame.image.load(os.path.join("Assets", "icon.png")))
walls = []
paths = []
treasure_list = []
num_treasures = 0
treasure_collected = []
trap_wall_list = []
trap_wall_moving_dir = []
trap_wall_last_motion = []
obstacles = []

connection = sqlite3.connect("scores.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS scores(past_scores int)")
connection.commit()
connection.close()


def init_maze(maze):
    """
    create maze elements using generated maze class object
    add maze elements including walls, path, and treasures onto the screen
    :param maze: Maze class object. maze.list -> 2D array of the text-based maze
    :return: None
    """
    global obstacles
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            block = pygame.Rect(i * BLOCK_SIZE + 4 * BLOCK_SIZE,
                                j * BLOCK_SIZE + 4 * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE)
            if maze.list[i][j] == maze.PATH:
                paths.append(block)
            else:
                walls.append(block)
    obstacles += walls


def draw_game(player, start_time, score, player_view, start_game):
    """
    draw and update graphic elements onto the screen
    :param player: pygame.Rect object, player
    :param start_time: datetime, time when game started
    :param score: int, number of treasure collected
    :param player_view: pygame.image, formatted player image
    :param start_game: Boolean, True if the game has started
    :return: None
    """
    # background colour
    WIN.fill(BACKGROUND_COLOUR)
    draw_maze(player, player_view)
    draw_progress_bar(start_time, score)
    # display start-game guide if game has not started
    if not start_game:
        WIN.blit(guide_view, (0, 0))
    pygame.display.update()


def draw_progress_bar(start_time, score):
    """
    draw progress bar which includes the time countdown bar and score
    :param start_time: datetime, time when game started
    :param score: int, number of treasures collected
    :return: None
    """
    # progress bar
    WIN.blit(bar_view, (0, 11 * BLOCK_SIZE))
    # score
    score_text = SCORE_FONT.render(f"{score}/{num_treasures}", 1, PROGRESS_TOP_COLOUR)
    WIN.blit(score_text, (BLOCK_SIZE * 9 + 2 * BLOCK_SIZE // 3, BLOCK_SIZE * 11 + BLOCK_SIZE // 3))
    # countdown
    countdown_percentage = (timedelta(minutes=TIME) - (datetime.now() - start_time)) / timedelta(minutes=TIME)
    back_bar = pygame.Rect(BLOCK_SIZE // 3,
                           BLOCK_SIZE * 11 + BLOCK_SIZE // 3 + BLOCK_SIZE // 20,
                           BLOCK_SIZE * 9,
                           BLOCK_SIZE // 4)
    pygame.draw.rect(WIN, PROGRESS_BACK_COLOUR, back_bar)
    top_bar = pygame.Rect(BLOCK_SIZE // 3,
                          BLOCK_SIZE * 11 + BLOCK_SIZE // 3 + BLOCK_SIZE // 20,
                          int(BLOCK_SIZE * 9 * countdown_percentage),
                          BLOCK_SIZE // 4)
    pygame.draw.rect(WIN, PROGRESS_TOP_COLOUR, top_bar)


def draw_maze(player, player_view):
    """
    draw and update all elements of the maze through out the game
    :param player: pygame.Rect, player
    :param player_view: formatted player image
    :return: None
    """
    # paths
    for path in paths:
        WIN.blit(path_view, (path.x, path.y))
    # treasures
    for i, treasure in enumerate(treasure_list):
        if not treasure_collected[i]:
            WIN.blit(treas_view, (treasure.x, treasure.y))
    # player
    WIN.blit(player_view, (player.x, player.y))
    # trapping walls
    for i, trap_wall in enumerate(trap_wall_list):
        if trap_wall_moving_dir[i] == "up":
            current_trap_wall_view = pygame.transform.rotate(trap_wall_view, 0)
        elif trap_wall_moving_dir[i] == "down":
            current_trap_wall_view = pygame.transform.rotate(trap_wall_view, 180)
        elif trap_wall_moving_dir[i] == "left":
            current_trap_wall_view = pygame.transform.rotate(trap_wall_view, 90)
        else:
            current_trap_wall_view = pygame.transform.rotate(trap_wall_view, 270)
        WIN.blit(current_trap_wall_view, (trap_wall.x, trap_wall.y))
    # walls
    for wall in walls:
        WIN.blit(wall_view, (wall.x, wall.y))


def move_maze(keys_pressed, player, player_heading_dir):
    """
    transform the position of the maze elements on screen responded to the user input
    :param keys_pressed: dict, dict of keys pressed, a key is pressed if keys_pressed[key] == True
    :param player: pygame.Rect, player
    :param player_heading_dir: int, record the direction player is moving towards, up-0, down-1, left-2, right-3
    :return: player_heading_dir (updated), player_standing_still [Boolean] (updated)
    """
    distance = SPEED
    direction = avoid_collision(player)
    player_standing_still = True
    if keys_pressed[KEYBOARD[0]]:  # up
        if not walls_ahead(player, [0, -1 * SPEED]):
            direction[1] += distance
            player_heading_dir = 0
    if keys_pressed[KEYBOARD[1]]:  # down
        if not walls_ahead(player, [0, 1 * SPEED]):
            direction[1] -= distance
            player_heading_dir = 1
    if keys_pressed[KEYBOARD[2]]:  # left
        if not walls_ahead(player, [-1 * SPEED, 0]):
            direction[0] += distance
            player_heading_dir = 2
    if keys_pressed[KEYBOARD[3]]:  # right
        if not walls_ahead(player, [1 * SPEED, 0]):
            direction[0] -= distance
            player_heading_dir = 3
    # move elements of the maze
    # walls
    for wall in walls:
        wall.x += direction[0]
        wall.y += direction[1]
    # paths
    for path in paths:
        path.x += direction[0]
        path.y += direction[1]
    # treasures
    for treasure in treasure_list:
        treasure.x += direction[0]
        treasure.y += direction[1]
    # trapping walls
    for trap_wall in trap_wall_list:
        trap_wall.x += direction[0]
        trap_wall.y += direction[1]
    # update player status if player end up standing still
    if direction != [0, 0]:
        player_standing_still = False
    return player_heading_dir, player_standing_still


def walls_ahead(player, dir):
    """
    check if player will collide into wall heading to given direction
    :param player: Rect
    :param dir: [x, y], direction player's going
    :return: True/False, if will collide into wall -> return True
    """
    new_position = pygame.Rect(player.x + dir[0], player.y + dir[1], player.width, player.height)
    for wall in walls:
        if new_position.colliderect(wall):
            return True
    return False


def avoid_collision(player):
    """
    adjust direction and player is moving to according to the obstacles
    :param player: pygame.Rect, player
    :return: dir, list, [x, y] direction player is moving to
    """
    direction = [0, 0]
    for wall in walls:
        if player.colliderect(wall):
            direction = adjust_dir_to_avoid_collision(player, wall, direction)
    return direction


def adjust_dir_to_avoid_collision(player, wall, dir):
    """
    correct the direction player is moving to if player will collide with walls in the maze
    player can't move trough walls
    :param player: pygame.Rect, player
    :param wall: pygame.Rect, block of wall
    :param dir: list, [x, y] direction player is moving to
    :return: dir
    """
    safe_position = pygame.Rect(player.x, player.y, player.width, player.height)
    while player.colliderect(wall):
        safe_position.x -= SPEED
        if not safe_position.colliderect(wall):
            dir[0] += SPEED
            break
        safe_position.x += 2 * SPEED
        if not safe_position.colliderect(wall):
            dir[0] -= SPEED
            break
        safe_position.x -= SPEED
        safe_position.y -= SPEED
        if not safe_position.colliderect(wall):
            dir[1] += SPEED
            break
        safe_position.y += 2 * SPEED
        if not safe_position.colliderect(wall):
            dir[1] -= SPEED
            break
    return dir


def distribute_treasures(maze):
    """
    distribute treasures into the maze
    :param maze: Maze class object
    :return: treasure_position
    """
    global treasure_list
    global num_treasures
    global treasure_collected
    treasure_positions = []
    for i in range(TREAS_NUM_PER_ROW):
        for j in range(TREAS_NUM_PER_ROW):
            # position relating to maze.list, not on the actual gui
            position = random_location([TREAS_PADDING + i * TREAS_DENSITY,
                                                 TREAS_PADDING + j * TREAS_DENSITY],
                                                [TREAS_PADDING + i * TREAS_DENSITY + TREAS_DENSITY,
                                                 TREAS_PADDING + j * TREAS_DENSITY + TREAS_DENSITY], maze)
            treasure_positions.append(position)
            treasure = pygame.Rect(position[0] * BLOCK_SIZE + 4 * BLOCK_SIZE,
                                   position[1] * BLOCK_SIZE + 4 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            treasure_list.append(treasure)
    num_treasures = len(treasure_list)
    treasure_collected = [False for _ in range(num_treasures)]
    return treasure_positions


def collect_treasure(player, score):
    """
    record treasures that has been collected by players
    :param player: pygame.Rect, player
    :param score: int, number of treasures collected
    :return: score (updated)
    """
    for i, treasure in enumerate(treasure_list):
        if not treasure_collected[i] and player.colliderect(treasure):
            score += 1
            treasure_collected[i] = True
            COLLECTED_SOUND.play()
    return score


def random_location(top_left, bottom_right, maze):
    """
    generate a random position in the range of two input position according to treasure position rule
    :param top_left: list, [i, j], top left location index
    :param bottom_right: list, [i, j], bottom right location index
    :param maze: Maze class object
    :return: list, [i, j], the random generated location
    """
    min_i = top_left[0]
    max_i = bottom_right[0]
    min_j = top_left[1]
    max_j = bottom_right[1]
    rand_i = randint(min_i, max_i)
    rand_j = randint(min_j, max_j)
    while not treasure_position_rule_satisfied(maze, rand_i, rand_j):
        rand_i = randint(min_i, max_i)
        rand_j = randint(min_j, max_j)
    return [rand_i, rand_j]


def treasure_position_rule_satisfied(maze, i, j):
    """
    rules:
    1. treasure cannot be in the same position as wall.
    2. treasure must have walls on either top-bottom or left-right
    3. treasure can't be near an entrance (a gap on a continuous wall)
    4. there must be space between any 2 treasures
    :param maze: maze object
    :param i: int, 1st index for treasure
    :param j: int, 2nd index for treasure
    :return: True if all rules satisfied
    """
    # rule 1
    if maze.list[i][j] == maze.WALL:
        return False
    # rule 2
    if not ((maze.list[i-1][j] == maze.WALL and maze.list[i+1][j] == maze.WALL)
            or (maze.list[i][j-1] == maze.WALL and maze.list[i][j+1] == maze.WALL)):
        return False
    # rule 3
    if not (maze.list[i-1][j-1] == maze.WALL
            and maze.list[i+1][j-1] == maze.WALL
            and maze.list[i-1][j+1] == maze.WALL
            and maze.list[i+1][j+1] == maze.WALL):
        return False
    # rule 4
    for treasure in treasure_list:
        if (i - 1 == treasure.x or i + 1 == treasure.x or j - 1 == treasure.y or j + 1 == treasure.y
                or i - 2 == treasure.x or i + 2 == treasure.x or j - 2 == treasure.y or j + 2 == treasure.y):
            return False
    return True


def distribute_trapping_walls(maze, treasure_positions):
    """
    distribute trapping walls into the maze
    each trapping wall should be near the corresponded treasure
    :param maze: Maze class object
    :param treasure_positions: list, positions of the treausres in maze.list
    :return: None
    """
    global trap_wall_list
    global trap_wall_moving_dir
    global trap_wall_last_motion
    global obstacles
    trap_wall_positions = []
    for i in range(len(treasure_list)):
        position = treasure_positions[i]
        x, y = position[0], position[1]
        # check surrounding
        # up-down walls
        if maze.list[x-1][y] == maze.WALL and maze.list[x+1][y] == maze.WALL:
            space_on_left = 0
            space_on_right = 0
            cur_x, cur_y = x, y
            # left
            while maze.list[cur_x][cur_y] != maze.WALL:
                cur_y -= 1
                space_on_left += 1
            cur_x, cur_y = x, y
            # right
            while maze.list[cur_x][cur_y] != maze.WALL:
                cur_y += 1
                space_on_right += 1
            if space_on_left >= space_on_right and space_on_left > 1:
                trap_wall_positions.append([x, y-1])
                trap_wall_moving_dir.append("left")
            elif space_on_left <= space_on_right and space_on_right > 1:
                trap_wall_positions.append([x, y+1])
                trap_wall_moving_dir.append("right")
        elif maze.list[x][y-1] == maze.WALL and maze.list[x][y+1] == maze.WALL:
            space_on_top = 0
            space_on_bottom = 0
            cur_x, cur_y = x, y
            # up
            while maze.list[cur_x][cur_y] != maze.WALL:
                cur_x -= 1
                space_on_top += 1
            cur_x, cur_y = x, y
            # down
            while maze.list[cur_x][cur_y] != maze.WALL:
                cur_x += 1
                space_on_bottom += 1
            if space_on_top >= space_on_bottom and space_on_top > 1:
                trap_wall_positions.append([x-1, y])
                trap_wall_moving_dir.append("up")
            elif space_on_top <= space_on_bottom and space_on_bottom > 1:
                trap_wall_positions.append([x+1, y])
                trap_wall_moving_dir.append("down")
    for i in range(len(trap_wall_positions)):
        position = trap_wall_positions[i]
        trap_wall = pygame.Rect(position[0] * BLOCK_SIZE + 4 * BLOCK_SIZE,
                                position[1] * BLOCK_SIZE + 4 * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE)
        trap_wall_list.append(trap_wall)
    obstacles += trap_wall_list
    trap_wall_last_motion = [[] for _ in range(len(trap_wall_list))]


def move_trap_walls(counter, current_index):
    """
    update trapping walls movements
    :param counter: int, count number of frames past
    :param current_index: current index of trap_walls status according to the motion list
    :return: counter (updated), current_index (updated)
    """
    global trap_wall_last_motion
    motion_list = [0, 0, -(BLOCK_SIZE // 4), -(BLOCK_SIZE // 4), -(BLOCK_SIZE // 4), -(BLOCK_SIZE // 4) - 2,
                   0, 0, (BLOCK_SIZE // 4), (BLOCK_SIZE // 4), (BLOCK_SIZE // 4), (BLOCK_SIZE // 4) + 2]
    motion = 0
    if counter > FPS // 8:
        current_index = (current_index + 1) % 12
        motion = motion_list[current_index]
        counter = 0
        for i, trap_wall in enumerate(trap_wall_list):
            if treasure_collected[i] and trap_wall_last_motion[i] != [] and (trap_wall_last_motion[i][-1] == 6
                                                                             or trap_wall_last_motion[i][-1] == 7):
                continue
            elif treasure_collected[i]:
                trap_wall_last_motion[i].append(current_index)
            if trap_wall_moving_dir[i] == "up":
                trap_wall.y += motion
            elif trap_wall_moving_dir[i] == "down":
                trap_wall.y -= motion
            elif trap_wall_moving_dir[i] == "left":
                trap_wall.x += motion
            elif trap_wall_moving_dir[i] == "right":
                trap_wall.x -= motion
    return counter, current_index


def player_killed_by_trap_walls(player, current_trap_wall_status_index, player_killed_music_played):
    """
    check if player is killed by the trapping walls
    :param player: pygame.Rect, player
    :param current_trap_wall_status_index: int, value == 0, 1, 6, 7 when the wall's in closed position
    :param player_killed_music_played: Boolean, True if the sound has already been played
    :return: True if player collide with any of the trap_wall while the wall is in closed status
    """
    close_index = [0, 1, 2, 3, 10, 11]
    for trap_wall in trap_wall_list:
        if player.colliderect(trap_wall) and current_trap_wall_status_index in close_index:
            if not player_killed_music_played:
                PLAYER_KILLED_SOUND.play()
            return True
    return False


def show_score_page(score, background, highest, average):
    """
    display the end score showing page
    :param score: int, number of treasures collected
    :param background: pygame.Rect, page background
    :param highest: int, highest score
    :param average: float, the scores' average
    :return: None
    """
    if background.y > 0:
        background.y -= BLOCK_SIZE // 2
        WIN.blit(background_view, (background.x, background.y))
    else:
        final_score = FINAL_FONT.render(f"{score}/{num_treasures}", 2, FINAL_FONT_COLOUR)
        WIN.blit(final_score, (LEN // 2 - BLOCK_SIZE - BLOCK_SIZE // 3, LEN // 2 - BLOCK_SIZE * 2))
        # additional text
        if score == num_treasures:
            additional_text = ADDITIONAL_FONT.render("Congratulations!", 1, ADDITIONAL_FONT_COLOUR)

        elif score >= 5:
            additional_text = ADDITIONAL_FONT.render("       Not Bad! ", 1, ADDITIONAL_FONT_COLOUR)
        else:
            additional_text = ADDITIONAL_FONT.render("         Oops!  ", 1, ADDITIONAL_FONT_COLOUR)
        WIN.blit(additional_text, (LEN // 2 - BLOCK_SIZE - int(BLOCK_SIZE * 1.7), LEN // 2 - int(BLOCK_SIZE * 3)))

        if highest != -1 and average != -1:
            highest_score = PAST_SCORE_FONT.render(f"Highest Score: {max(highest, score)}/{num_treasures}",
                                                   1, PAST_SCORES_FONT_COLOUR)
            average_score = PAST_SCORE_FONT.render(f"Average Score: {round(average, 1)}/{num_treasures}",
                                                   1, PAST_SCORES_FONT_COLOUR)
            WIN.blit(highest_score, (LEN // 2 - BLOCK_SIZE * 2, LEN // 2 - BLOCK_SIZE // 2))
            WIN.blit(average_score, (int(LEN // 2 - BLOCK_SIZE * 2.3), LEN // 2 + BLOCK_SIZE // 4))
        WIN.blit(replay_view, (BLOCK_SIZE * 3, BLOCK_SIZE * 7))
        WIN.blit(quit_view, (BLOCK_SIZE * 3, int(BLOCK_SIZE * 8.5)))
    pygame.display.update()


def scores_list(past_scores):
    """
    return a list of integer
    :param past_scores: list, a list of tuples which each tuple contains and intager
    :return: list, a list of integer
    """
    list = []
    for t in past_scores:
        list.append(t[0])
    return list


def update_player_img(counter, current_player_img_index, player_heading_dir, player_standing_still):
    """
    update player img according to the players' motion when walking
    *note: player_heading_dir: 0:up, 1:down, 2:left, 3:right
    *note: PLAYER_IMG_LIST[player_heading_dir][current_player_img_index]
    :param counter: int, count up 1 every frame
    :param current_player_img_index: int, index from 0-3, player posture
    :param player_heading_dir: int, index from 0-3, player heading direction
    :param player_standing_still: Boolean, true if player doesn't move
    :return: counter (updated, range(0, FPS//2)), current_player_img_index (updated), player_view (updated)
    """
    if counter > FPS // 6:
        counter = 0
        current_player_img_index = (current_player_img_index + 1) % 4
    if player_standing_still:
        current_player_img_index = 1
    player_view = pygame.transform.scale(PLAYER_IMG_LIST[player_heading_dir][current_player_img_index],
                                         (BLOCK_SIZE - 2 * CHARACTER_PADDING, BLOCK_SIZE - 2 * CHARACTER_PADDING))
    return counter, current_player_img_index, player_view


def init_database():
    """
    Create database if not exist
    :return: None
    """
    conn = sqlite3.connect("scores.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS scores(past_scores)")
    conn.commit()
    conn.close()


def update_database(score):
    """
    insert current score into database, and load all past scores to calculate and return the all time high and average.
    :param score: int, current score
    :return: int, float: highest_score, average
    """
    conn = sqlite3.connect("scores.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO scores(past_scores) VALUES (?)", (score,))  # add current score
    cur.execute("SELECT * FROM scores")
    past_scores = scores_list(cur.fetchall())
    conn.commit()
    conn.close()
    # past score data
    highest_score = max(past_scores)
    average = sum(past_scores) / len(past_scores)
    return highest_score, average


def check_button_restart_game(x, y):
    """
    check if restart button is clicked, restart the game if True
    :param x: mouse x index
    :param y: mouse y index
    :return: None
    """
    if BLOCK_SIZE * 3 <= x <= BLOCK_SIZE * 8 and BLOCK_SIZE * 7 <= y <= BLOCK_SIZE * 8:
        WIN.blit(pressed_replay_view, (BLOCK_SIZE * 3, BLOCK_SIZE * 7))
        BUTTON_SOUND.play()
        pygame.display.update()
        pygame.time.delay(200)
        new_maze = Maze(MAZE_SIZE)
        main(new_maze)


def check_button_quit_game(x, y):
    """
    quit the game if quit button is clicked
    :param x: mouse x index
    :param y: mouse y index
    :return: None
    """
    if (BLOCK_SIZE * 3 <= x <= BLOCK_SIZE * 8
            and int(BLOCK_SIZE * 8.5) <= y <= int(BLOCK_SIZE * 9.5)):
        WIN.blit(pressed_quit_view, (BLOCK_SIZE * 3, BLOCK_SIZE * 8.5))
        BUTTON_SOUND.play()
        pygame.display.update()
        pygame.time.delay(200)
        pygame.quit()
        sys.exit()


def check_times_up(start_time, sound_played):
    """
    check if times almost up and play the game ending sound.
    :param start_time:
    :param sound_played:
    :return:
    """
    if (not sound_played
            and (start_time + timedelta(minutes=TIME) - timedelta(seconds=1.5))
            < datetime.now() < (start_time + timedelta(minutes=TIME))):
        TIMES_UP_SOUND.play()
        sound_played = True
    return sound_played


def main(maze):
    # reset game parameters for replay function
    walls.clear()
    paths.clear()
    treasure_list.clear()
    trap_wall_list.clear()
    trap_wall_moving_dir.clear()
    score = 0
    clock = pygame.time.Clock()
    # prepare game
    init_maze(maze)
    treasure_positions = distribute_treasures(maze)
    distribute_trapping_walls(maze, treasure_positions)
    player = pygame.Rect(5 * BLOCK_SIZE + CHARACTER_PADDING,
                         5 * BLOCK_SIZE + CHARACTER_PADDING,
                         BLOCK_SIZE - 2 * CHARACTER_PADDING,
                         BLOCK_SIZE - 2 * CHARACTER_PADDING)
    database_accessed = False
    highest_score = -1
    average = -1
    # final score display page background
    background = pygame.Rect(0, BLOCK_SIZE * 12, BLOCK_SIZE * 11, BLOCK_SIZE * 12)
    # player img status
    player_counter = 0  # count how many frame has past
    current_player_img_index = 1  # standing still
    player_heading_dir = 1  # right
    player_view = pygame.transform.scale(PLAYER_IMG_LIST[player_heading_dir][current_player_img_index],
                                         (BLOCK_SIZE - 2 * CHARACTER_PADDING, BLOCK_SIZE - 2 * CHARACTER_PADDING))
    player_killed = False
    # trap walls time count
    trap_wall_counter = 0
    current_trap_wall_status_index = 0
    # start game control & countdown
    start_game = False
    start_time = datetime.now()
    times_up_sound_played = False
    # game loop
    while True:
        game_ended = False
        # Frame rate
        clock.tick(FPS)
        # if during game
        if (len(treasure_list) != 0 and datetime.now() < start_time + timedelta(minutes=TIME)
                and not player_killed):
            # times up sound effect
            times_up_sound_played = check_times_up(start_time, times_up_sound_played)
            player_killed = player_killed_by_trap_walls(player, current_trap_wall_status_index, player_killed)
            keys_pressed = pygame.key.get_pressed()
            # start game
            if not start_game and not keys_pressed[START_KEY]:
                start_time = datetime.now()
            if not start_game and keys_pressed[START_KEY]:
                start_game = True
                start_time = datetime.now()
                START_GAME_SOUND.play()
            elif start_game:
                # update maze
                player_heading_dir, player_standing_till = move_maze(keys_pressed, player, player_heading_dir)
                trap_wall_counter += 1
                trap_wall_counter, current_trap_wall_status_index = move_trap_walls(trap_wall_counter,
                                                                                    current_trap_wall_status_index)
                # update player img status
                player_counter += 1
                player_counter, current_player_img_index, player_view = update_player_img(player_counter,
                                                                                current_player_img_index,
                                                                                player_heading_dir,
                                                                                player_standing_till)
                # update score
                score = collect_treasure(player, score)
            # update game view
            draw_game(player, start_time, score, player_view, start_game)
        # if game ends
        else:
            if not database_accessed:
                # update score to database & fetch past scores
                init_database()
                highest_score, average = update_database(score)
                database_accessed = True
            game_ended = True
            # display score page
            show_score_page(score, background, highest_score, average)
        # control
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and game_ended:
                mouse_x, mouse_y = event.pos
                # restart game
                check_button_restart_game(mouse_x, mouse_y)
                # quit game
                check_button_quit_game(mouse_x, mouse_y)


if __name__ == "__main__":
    main(Maze(MAZE_SIZE))
