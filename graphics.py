import pygame
import os

import main

class character_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rows = 4
        self.cols = 5
        self.totalCell = self.rows * self.cols

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / self.cols
        h = self.cellHeight = self.rect.height / self.rows

        self.cells = list()
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells.append([x * w, y * h, w, h])

    def draw(self, surface, x, y, cellIndex, direction):
        if direction == "UP":
            pass
        if direction == "RIGHT":
            cellIndex = cellIndex + 5
        if direction == "DOWN":
            cellIndex = cellIndex + 10
        if direction == "LEFT":
            cellIndex = cellIndex + 15
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class wall_spritesheet:
    def __init__(self, image_spritesheet_path, maze_size):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.left_wall = []
        self.right_wall =[]
        self.up_wall = []
        # Mỗi bộ 4 thông số bên dưới ý nghĩa là: x, y, width, height
        # Cắt từ ảnh bắt đầu từ tọa độ (x, y) cắt ngang width và xuống height
        # Anh tính sẵn cho mình hiểu vậy là được
        if maze_size == 6:
            self.left_wall = [0, 0, 12, 78]
            self.right_wall = [84, 0, 12, 78]
            self.up_wall = [12, 0, 72, 18]
            self.up_wall_no_shadow = [12, 0, 66, 18]
        elif maze_size == 8:
            self.left_wall = [0, 0, 12, 63]
            self.right_wall = [69, 0, 12, 63]
            self.up_wall = [12, 0, 57, 18]
            self.up_wall_no_shadow = [12, 0, 51, 18]
        elif maze_size == 10:
            self.left_wall = [0, 0, 8, 48]
            self.right_wall = [52, 0, 8, 48]
            self.up_wall = [8, 0, 44, 12]
            self.up_wall_no_shadow = [8, 0, 38, 12]

    def draw_left_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.left_wall)

    def draw_right_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.right_wall)

    def draw_up_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall)

    def draw_up_wall_no_shadow(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall_no_shadow)

class stairs_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell_w = self.rect.width // 4
        self.cell_h = self.rect.height

        self.stairs = []
        for x in range(4):
            self.stairs.append([x * self.cell_w, 0, self.cell_w, self.cell_h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.stairs[cellIndex])

def draw_screen(screen, input_maze, backdrop, floor, maze_size, cell_rect, stair,
                stair_position,
                mummy_white,
                wall,
                explorer):
    coordinate_X = 67
    coordinate_Y = 80
    # DRAW BACKDROP AND FLOOR
    screen.blit(backdrop, (0, 0))
    screen.blit(floor, (coordinate_X, coordinate_Y))

    # DRAW STAIR
    stair_px = stair_position[1] // 2
    stair_py = stair_position[0] // 2
    stair_x = coordinate_X + cell_rect * (stair_px)
    stair_y = coordinate_Y + cell_rect * (stair_py)
    stair_index = 0
    # STAIR IS RIGHT
    if (stair_px == maze_size and stair_position[0] > 0 and stair_position[0] < 2 * maze_size):
        stair_index = 1
    # STAIR IS LEFT
    elif (stair_px == 0 and stair_position[0] > 0 and stair_position[0] < 2 * maze_size):
        stair_index = 3
    # STAIR IS DOWN
    elif (stair_py == maze_size and stair_position[1] > 0 and stair_position[1] < 2 * maze_size):
        stair_index = 2
    if (stair_index == 0):
        stair_y = coordinate_Y - stair.cell_h
    if (stair_index == 3):
        stair_x = coordinate_X - stair.cell_w
    stair.draw(screen, stair_x, stair_y, stair_index)

    # DRAW EXPLORER
    if explorer["coordinates"]:
        explorer["sprite_sheet"].draw(screen, explorer["coordinates"][0],
                                              explorer["coordinates"][1],
                                              explorer["cellIndex"],
                                              explorer["direction"])

    # DRAW MUMMY WHITE
    if mummy_white:
        mummy_white["sprite_sheet"].draw(screen, mummy_white["coordinates"][0],
                                                 mummy_white["coordinates"][1],
                                                 mummy_white["cellIndex"],
                                                 mummy_white["direction"])

    # DRAW WALL
    # Horizontal Wall
    # Hàng chẵn chứa tường ngang
    # Tường nằm giữa 2 ô trống ngang nên ở cột lẻ
    for x in range(2, len(input_maze)-1, 2):
        for y in range(1, len(input_maze[x]), 2):
            if input_maze[x][y] == "%":
                # Tính tọa độ tương tự hàm Cal_coordinate bên main
                wall_x = coordinate_X + cell_rect * (y // 2)
                wall_y = coordinate_Y + cell_rect * (x // 2)
                # Trừ lại cho nó không bị lệch
                # Anh test sẵn mình sài thôi
                if maze_size == 6 or maze_size == 8:
                    wall_x -= 6
                    wall_y -= 12
                if maze_size == 10:
                    wall_x -= 3
                    wall_y -= 9
                wall.draw_up_wall(screen, wall_x, wall_y)
    # Vertical Wall
    # Cột chẵn chứa tường dọc
    # Tường nằm giữa 2 ô trống dọc nên ở hàng lẻ
    for y in range(2, len(input_maze)-1, 2):
        for x in range(1, len(input_maze[y]), 2):
            if input_maze[x][y] == "%":
                wall_x = coordinate_X + cell_rect * (y // 2)
                wall_y = coordinate_Y + cell_rect * (x // 2)
                if maze_size == 6 or maze_size == 8:
                    wall_x -= 6
                    wall_y -= 12
                elif maze_size == 10:
                    wall_x -= 3
                    wall_y -= 9
                # Trường hợp mà tường tạo góc vuông thì sài right_wall bởi nó ngắn nó mới khớp
                if (input_maze[x+1][y+1] == "%"):
                    wall.draw_right_wall(screen, wall_x, wall_y)
                    redraw_x = coordinate_X + cell_rect * ((y+1) // 2)
                    redraw_y = coordinate_Y + cell_rect * ((x+1) // 2)
                    if maze_size == 6 or maze_size == 8:
                        redraw_x -= 6
                        redraw_y -= 12
                    if maze_size == 10:
                        redraw_x -= 3
                        redraw_y -= 9
                    # Vẽ lại tường ngang không bóng đổ
                    if (x + 1 < maze_size * 2 and y + 1 < maze_size * 2):
                        wall.draw_up_wall_no_shadow(screen, redraw_x, redraw_y)
                else:
                    wall.draw_left_wall(screen, wall_x, wall_y)