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

class key_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class gate_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        # 8 is number of sheet in image
        w = self.rect.width / 8
        h = self.rect.height
        self.cells = []
        for x in range(8):
            self.cells.append([x * w, 0, w, h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class trap_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class stairs_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell_w = self.rect.width // 4
        self.cell_h = self.rect.height
        # Stair is UP, RIGHT, DOWN, LEFT = (0, 1, 2, 3) in list stairs
        self.stairs = []
        for x in range(4):
            self.stairs.append([x * self.cell_w, 0, self.cell_w, self.cell_h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.stairs[cellIndex])

def draw_screen(screen, input_maze, maze_size, cell_rect, backdrop, floor, stair, stair_position, trap, trap_position,
                key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
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

    # DRAW TRAP
    if trap_position:
        trap_x = coordinate_X + cell_rect * (trap_position[1] // 2)
        trap_y = coordinate_Y + cell_rect * (trap_position[0] // 2)
        trap.draw(screen, trap_x, trap_y)

    # DRAW KEY
    if key_position:
        key_x = coordinate_X + cell_rect * (key_position[1] // 2)
        key_y = coordinate_Y + cell_rect * (key_position[0] // 2)
        key.draw(screen, key_x, key_y)

    # DRAW EXPLORER
    if explorer["coordinates"]:
        explorer["sprite_sheet"].draw(screen, explorer["coordinates"][0], explorer["coordinates"][1], explorer["cellIndex"], explorer["direction"])

    # DRAW MUMMY WHITE
    if mummy_white:
        for i in range(len(mummy_white)):
            mummy_white[i]["sprite_sheet"].draw(screen, mummy_white[i]["coordinates"][0], mummy_white[i]["coordinates"][1],
                                                mummy_white[i]["cellIndex"], mummy_white[i]["direction"])

    # DRAW MUMMY RED
    if mummy_red:
        for i in range(len(mummy_red)):
            mummy_red[i]["sprite_sheet"].draw(screen, mummy_red[i]["coordinates"][0], mummy_red[i]["coordinates"][1],
                                                mummy_red[i]["cellIndex"], mummy_red[i]["direction"])

    # DRAW SCORPION WHITE
    if scorpion_white:
        for i in range(len(scorpion_white)):
            scorpion_white[i]["sprite_sheet"].draw(screen, scorpion_white[i]["coordinates"][0], scorpion_white[i]["coordinates"][1],
                                                scorpion_white[i]["cellIndex"], scorpion_white[i]["direction"])

    # DRAW SCORPION RED
    if scorpion_red:
        for i in range(len(scorpion_red)):
            scorpion_red[i]["sprite_sheet"].draw(screen, scorpion_red[i]["coordinates"][0], scorpion_red[i]["coordinates"][1],
                                                scorpion_red[i]["cellIndex"], scorpion_red[i]["direction"])

    # DRAW GATE
    if gate:
        gate_x = coordinate_X + cell_rect * (gate["gate_position"][1] // 2)
        gate_y = coordinate_Y + cell_rect * (gate["gate_position"][0] // 2)
        if maze_size == 6 or maze_size == 8:
            gate_x -= 6
            gate_y -= 12
        elif maze_size == 10:
            gate_x -= 3
            gate_y -= 9
        gate_sheet.draw(screen, gate_x, gate_y, gate["cellIndex"])

    # DRAW WALL
    # Horizontal Wall
    for i in range(2, len(input_maze)-1, 2):
        for j in range(1, len(input_maze[i]), 2):
            if input_maze[i][j] == "%":
                wall_x = coordinate_X + cell_rect * (j // 2)
                wall_y = coordinate_Y + cell_rect * (i // 2)
                if maze_size == 6 or maze_size == 8:
                    wall_x -= 6
                    wall_y -= 12
                if maze_size == 10:
                    wall_x -= 3
                    wall_y -= 9
                wall.draw_up_wall(screen, wall_x, wall_y)
                
    # Vertical Wall
    for j in range(2, len(input_maze)-1, 2):
        for i in range(1, len(input_maze[j]), 2):
            if input_maze[i][j] == "%":
                wall_x = coordinate_X + cell_rect * (j // 2)
                wall_y = coordinate_Y + cell_rect * (i // 2)
                if maze_size == 6 or maze_size == 8:
                    wall_x -= 6
                    wall_y -= 12
                elif maze_size == 10:
                    wall_x -= 3
                    wall_y -= 9
                if (input_maze[i+1][j+1] == "%"):
                    wall.draw_right_wall(screen, wall_x, wall_y)
                    redraw_x = coordinate_X + cell_rect * ((j+1) // 2)
                    redraw_y = coordinate_Y + cell_rect * ((i+1) // 2)
                    if maze_size == 6 or maze_size == 8:
                        redraw_x -= 6
                        redraw_y -= 12
                    if maze_size == 10:
                        redraw_x -= 3
                        redraw_y -= 9
                    if (i + 1 < maze_size * 2 and j + 1 < maze_size * 2):
                        wall.draw_up_wall_no_shadow(screen, redraw_x, redraw_y)
                else:
                    wall.draw_left_wall(screen, wall_x, wall_y)

def gate_animation(screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    for i in range(8):
        if gate["isClosed"]:
            gate["cellIndex"] = -(i+1)
        else:
            gate["cellIndex"] = i
        draw_screen(screen, game.maze, game.maze_size, game.cell_rect, backdrop, floor, stair, game.stair_position,
                    trap, game.trap_position, key, game.key_position, gate_sheet, gate, wall, explorer, mummy_white, 
                    mummy_red, scorpion_white, scorpion_red)
        pygame.time.delay(70)
        pygame.display.update()

def determine_moving_direction(past_position, new_position):
    if past_position[0] == new_position[0] + 2:  # Move UP
        return "UP"
    if past_position[0] == new_position[0] - 2:  # Move Down
        return "DOWN"
    if past_position[1] == new_position[1] + 2:  # Move Left
        return "LEFT"
    if past_position[1] == new_position[1] - 2:  # Move Right
        return "RIGHT"

def enemy_move_animation(mw_past_position, mw_new_position, mr_past_position, mr_new_position, sw_past_position, 
                         sw_new_position, sr_past_position, sr_new_position, screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                         key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    def enemy_check_movement(enemy_past_position, enemy_new_position, enemy):
        check_movement = [False for _ in range(len(enemy_past_position))]
        for i in range(len(enemy_past_position)):
            enemy_start_x = game.coordinate_screen_x + game.cell_rect * (enemy_past_position[i][1] // 2)
            enemy_start_y = game.coordinate_screen_y + game.cell_rect * (enemy_past_position[i][0] // 2)
            if game.maze[enemy_new_position[i][0] - 1][enemy_new_position[i][1]] == "%" or game.maze[enemy_new_position[i][0] - 1][enemy_new_position[i][1]] == "G":
                enemy_start_y += 3
            enemy[i]["coordinates"] = ([enemy_start_x, enemy_start_y])
            if enemy_past_position[i][0] != enemy_new_position[i][0] or enemy_past_position[i][1] != enemy_new_position[i][1]:
                check_movement[i] = True
            if check_movement[i]:
                enemy[i]["direction"] = determine_moving_direction(enemy_past_position[i], enemy_new_position[i])
        return check_movement
    
    # Mummy White
    mw_check_movement = enemy_check_movement(mw_past_position, mw_new_position, mummy_white)
    # Mummy Red
    mr_check_movement = enemy_check_movement(mr_past_position, mr_new_position, mummy_red)
    # Scorpion White
    sw_check_movement = enemy_check_movement(sw_past_position, sw_new_position, scorpion_white)
    # Scorpion Red
    sr_check_movement = enemy_check_movement(sr_past_position, sr_new_position, scorpion_red)
    
    step_stride = game.cell_rect // 5
    def update_enemy_animation(enemy, check_movement, i):
        for j in range(len(enemy)):
            if i < 5:
                if enemy[j]["direction"] == "UP" and check_movement[j]:
                    enemy[j]["coordinates"][1] -= step_stride
                if enemy[j]["direction"] == "DOWN" and check_movement[j]:
                    enemy[j]["coordinates"][1] += step_stride
                if enemy[j]["direction"] == "LEFT" and check_movement[j]:
                    enemy[j]["coordinates"][0] -= step_stride
                if enemy[j]["direction"] == "RIGHT" and check_movement[j]:
                    enemy[j]["coordinates"][0] += step_stride
            if check_movement[j]:
                enemy[j]["cellIndex"] = i % 5
        
    for i in range(6):
        update_enemy_animation(mummy_white, mw_check_movement, i)
        update_enemy_animation(mummy_red, mr_check_movement, i)
        update_enemy_animation(scorpion_white, sw_check_movement, i)
        update_enemy_animation(scorpion_red, sr_check_movement, i)

        draw_screen(screen, game.maze, game.maze_size, game.cell_rect, backdrop, floor, stair, game.stair_position,
                    trap, game.trap_position, key, game.key_position, gate_sheet, gate, wall, explorer, mummy_white, 
                    mummy_red, scorpion_white, scorpion_red)
        pygame.time.delay(70)
        pygame.display.update()