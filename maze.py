"""
maze.py
This file contains Maze class, and responsible for generating the maze map and control all its properties.

Author: Allyn Bao
Date last modified: 9/9/2021
"""

from random import randint


class Maze:

    # labels of maze elements for debugging
    WALL = "WWW"
    PATH = " . "
    PLAYER = "@"
    TREAS = "$"

    def __init__(self, size):
        """
        initialize the maze map
        :param size: int, the length of the square maze map with frame without outer paddings
        self.size = size (if size is valid) size = 1 + 2 * n where n is positive int
        self.list: list, store the information of the maze in a 2-D array
        """
        # check maze size
        if 10 < size < 60 and (size - 1) % 2 == 0:
            self.size = size
        else:
            raise ValueError

        self.list = [[self.PATH for _ in range(self.size)] for _ in range(self.size)]
        self.generate_maze()

    def __str__(self):
        string = ""
        for line in self.list:
            string += ("".join(line)) + "\n"
        return string[:-1]

    def generate_maze(self):
        """
        add walls to the maze map: through modifying self.list
        :return: None
        """
        #add frame
        #top
        self.list[0] = [self.WALL for _ in range(self.size)]
        #bottom
        self.list[self.size-1] = [self.WALL for _ in range(self.size)]
        #left & right
        for i in range(self.size):
            self.list[i][0] = self.WALL
            self.list[i][self.size-1] = self.WALL
        #draw inner walls
        self.list = self.division_generator(self.list, [])

    def division_generator(self, chamber, entrances):
        """
        Recursive division maze generator
        :param chamber: list, store the partial map / chamber of the maze
        :param entrances: list, a list of location of all the gaps on the outer wall
        :return: list, new map list with inner wall finished
        """
        height = len(chamber)
        width = len(chamber[0])
        # base case
        if height == 3 or width == 3:
            return chamber
        # one wall needed to add in the middle
        elif height == 5:
            # WWWWWWWWWWWW
            # W..........W
            # ...........W
            # W...........<-entrance
            # WWWWWWWWWWWW
            # check if the entrance to the chamber is in the middle where the inner wall will be added
            middle_entrance_on_left = False
            middle_entrance_on_right = False
            for entrance in entrances:
                if entrance == [2, 0]:
                    middle_entrance_on_left = True
                elif entrance == [2, width - 1]:
                    middle_entrance_on_right = True
            #draw middle wall
            # WWWWWWWWWWWW
            # W..........W
            # ..WWWWW.WWWW
            # W...........
            # WWWWWWWWWWWW
            for i in range(width)[1:-1]:
                if not ((i == 1 and middle_entrance_on_left) or (i == width - 2 and middle_entrance_on_right)):
                    chamber[2][i] = self.WALL
            # add entrance on middle wall
            if width == 5:
                chamber[2][2] = self.PATH
            # add entrance on middle wall if the wall is long enough
            elif width > 5:
                n = randint(1, width - 2)
                chamber[2][n] = self.PATH
            return chamber
        elif width == 5:
            # WW.WW
            # W...W
            # W...W
            # W...W
            # W...W
            # W...W
            # W...W
            # WWW.W
            # check for the existence of the middle entrances
            middle_entrance_on_top = False
            middle_entrance_on_bottom = False
            for entrance in entrances:
                if entrance == [0, 2]:
                    middle_entrance_on_top = True
                elif entrance == [height - 1, 2]:
                    middle_entrance_on_bottom = True
            # draw the middle wall
            for i in range(height)[1:-1]:
                if not ((i == 1 and middle_entrance_on_top) or (i == height - 2 and middle_entrance_on_bottom)):
                    chamber[i][2] = self.WALL
            # add entrance on middle wall
            if height == 5:
                chamber[2][2] = self.PATH
            # add entrance on middle wall if the wall is long enough
            elif height > 5:
                n = randint(1, width - 2)
                chamber[n][2] = self.PATH
            return chamber
        # large chamber - needs vertical as well as horizontal division
        elif height >= 7 and width >= 7:
            # WWWWW.WWWWWWW
            # W...........W
            # W...........W
            # W............
            # W...........W
            # ............W
            # W...........W
            # WWWWWWWW.WWWW
            # locate all entrances
            top_entrance = 0
            bottom_entrance = 0
            left_entrance = 0
            right_entrance = 0
            for entrance in entrances:
                if entrance[0] == 0:  # top
                    top_entrance = entrance[1]
                elif entrance[0] == height - 1:  # bottom
                    bottom_entrance = entrance[1]
                elif entrance[1] == 0:
                    left_entrance = entrance[0]
                elif entrance[1] == 0:
                    right_entrance = entrance[0]
            # generate random wall position
            vertical_wall_index = Maze.random_wall_position(2, width - 3, [top_entrance, bottom_entrance])
            horizontal_wall_index = Maze.random_wall_position(2, height - 3, [left_entrance, right_entrance])
            # add Walls
            # vertical wall
            for i in range(height)[1:-1]:
                chamber[i][vertical_wall_index] = self.WALL
            for i in range(width)[1:-1]:
                chamber[horizontal_wall_index][i] = self.WALL
            # add inner entrances
            if horizontal_wall_index > 2:
                top_half_entrance_index = Maze.random_path_position(1, horizontal_wall_index - 1)
                chamber[top_half_entrance_index][vertical_wall_index] = self.PATH
            else:
                chamber[1][vertical_wall_index] = self.PATH
            if height - horizontal_wall_index > 2:
                bottom_half_entrance_index = Maze.random_path_position(horizontal_wall_index + 1, height - 2)
                chamber[bottom_half_entrance_index][vertical_wall_index] = self.PATH
            else:
                chamber[height-2][vertical_wall_index] = self.PATH
            if vertical_wall_index > 2:
                left_half_entrance_index = Maze.random_path_position(1, vertical_wall_index - 1)
                chamber[horizontal_wall_index][left_half_entrance_index] = self.PATH
            else:
                chamber[horizontal_wall_index][1] = self.PATH
            if width - vertical_wall_index > 2:
                right_half_entrance_index = Maze.random_path_position(vertical_wall_index + 1, width - 2)
                chamber[horizontal_wall_index][right_half_entrance_index] = self.PATH
            else:
                chamber[horizontal_wall_index][width - 2] = self.PATH
            # chambers
            top_left = []
            top_right = []
            bottom_left = []
            bottom_right = []
            # top_left
            for row in chamber[:horizontal_wall_index + 1]:
                top_left.append(row[:vertical_wall_index + 1])
            for row in chamber[horizontal_wall_index:]:
                bottom_left.append(row[:vertical_wall_index + 1])
            for row in chamber[:horizontal_wall_index + 1]:
                top_right.append(row[vertical_wall_index:])
            for row in chamber[horizontal_wall_index:]:
                bottom_right.append(row[vertical_wall_index:])
            # further division
            new_top_left = self.division_generator(top_left, self.find_all_entrances(top_left))
            new_top_right = self.division_generator(top_right, self.find_all_entrances(top_right))
            new_bottom_left = self.division_generator(bottom_left, self.find_all_entrances(bottom_left))
            new_bottom_right = self.division_generator(bottom_right, self.find_all_entrances(bottom_right))
            # pieces it back
            new_chamber = []
            for i in range(len(new_top_left))[:-1]:
                new_chamber.append(new_top_left[i] + new_top_right[i][1:])
            for i in range(len(new_bottom_left)):
                new_chamber.append(new_bottom_left[i] + new_bottom_right[i][1:])
            return new_chamber

    @staticmethod
    def random_wall_position(min, max, num_to_avoid):
        """
        generate a radom number n where min <= n <= max and n is Even number and n not in num_to_avoid
        :param min: int, min value, min >= 0
        :param max: int, max value
        :param num_to_avoid: list of int
        :return: int
        """
        n = -1
        while n < min or n in num_to_avoid or n % 2 != 0:
            n = randint(min, max)
        return n

    @staticmethod
    def random_path_position(min, max):
        """
        return a random int n where min <= n <= max and n is a Odd number
        :param min: int, min value, min >= 0
        :param max: int, max value
        :return: int
        """
        n = -1
        while n < min or n % 2 == 0:
            n = randint(min, max)
        return n

    def find_all_entrances(self, chamber):
        """
        find all entrances on the sides of the chamber and return a list of all location of the entrances
        :param chamber: 2-D list
        :return: list, contain location of all entrances
        """
        entrances = []
        for i in range(len(chamber[0])):
            if chamber[0][i] == self.PATH:
                entrances.append([0, i])
            if chamber[len(chamber)-1][i] == self.PATH:
                entrances.append([len(chamber)-1, i])
        for i in range(len(chamber)):
            if chamber[i][0] == self.PATH:
                entrances.append([i, 0])
            if chamber[i][len(chamber[0])-1] == self.PATH:
                entrances.append([i, len(chamber[0])-1])
        return entrances
