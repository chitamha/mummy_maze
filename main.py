import pygame
import os
import fixbug
import graphics
import characters

class GameState:
    def __init__(self, file_name):
        self.screen_size_x = 494
        self.screen_size_y = 480
        self.maze_rect = 360
        self.coordinate_screen_x = 67
        self.coordinate_screen_y = 80
        self.get_input_maze(file_name)
        self.get_input_object(file_name)
        self.gate = dict()
        if (self.gate_position):
            self.gate = {
                "gate_position": self.gate_position,
                "isClosed": True,
                "cellIndex": 0
            }

        # Set initial direction
        if (self.explorer_position[1] // 2 <= self.maze_size // 2):
            self.explorer_direction = "RIGHT"
        else:
            self.explorer_direction = "LEFT"
        
        self.mummy_white_direction = []
        self.mummy_red_direction = []
        self.scorpion_white_direction = []
        self.scorpion_red_direction = []
        if (self.mummy_white_position):
            for i in range(len(self.mummy_white_position)):
                self.mummy_white_direction.append("DOWN")
        if (self.mummy_red_position):
            for i in range(len(self.mummy_red_position)):
                self.mummy_red_direction.append("DOWN")
        if (self.scorpion_white_position):
            for i in range(len(self.scorpion_white_position)):
                self.scorpion_white_direction.append("DOWN")
        if (self.scorpion_red_position):
            for i in range(len(self.scorpion_red_position)):
                self.scorpion_red_direction.append("DOWN") 

    def get_input_maze(self, name):
        self.maze = []
        self.stair_position = ()
        self.gate_position = ()
        self.key_position = ()
        self.trap_position = ()
        with open(os.path.join(maze_path, name), "r") as file:
            for line in file:
                row = []
                for char in line:
                    if (char != "\n"): row.append(char)
                self.maze.append(row)

        self.maze_size = len(self.maze) // 2
        self.cell_rect = self.maze_rect // self.maze_size

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == "G"):
                    self.gate_position = (i, j)
                if (self.maze[i][j] == "K"):
                    self.key_position = (i, j)
                if (self.maze[i][j] == "T"):
                    self.trap_position = (i, j)
                if (self.maze[i][j] == "S"):
                    self.stair_position = (i, j)
            
    def get_input_object(self, name):
        self.mummy_white_position = []
        self.mummy_red_position = []
        self.scorpion_white_position = []
        self.scorpion_red_position = []
        with open(os.path.join(agents_path, name), "r") as file:
            for line in file:
                x = line.split()
                if (x[0] == "E"):
                    self.explorer_position = [int(x[1]), int(x[2])]
                if (x[0] == "MW"):
                    self.mummy_white_position.append([int(x[1]), int(x[2])])
                if (x[0] == "MR"):
                    self.mummy_red_position.append([int(x[1]), int(x[2])])
                if (x[0] == "SW"):
                    self.scorpion_white_position.append([int(x[1]), int(x[2])])
                if (x[0] == "SR"):
                    self.scorpion_red_position.append([int(x[1]), int(x[2])])
    
def load_image_path(size):
    image_path = os.path.join(project_path, "image")
    backdrop_path = os.path.join(image_path, "backdrop.png")
    filename_floor = "floor" + str(size) + ".jpg"
    filename_wall = "walls" + str(size) + ".png"
    filename_key = "key" + str(size) + ".png"
    filename_gate = "gate" + str(size) + ".png"
    filename_trap = "trap" + str(size) + ".png"
    filename_stair = "stairs" + str(size) + ".png"
    filename_explorer = "explorer" + str(size) + ".png"
    filename_mummy_white = "mummy_white" + str(size) + ".png"
    filename_mummy_red = "redmummy" + str(size) + ".png"
    filename_scorpion_white = "white_scorpion" + str(size) + ".png"
    filename_scorpion_red = "red_scorpion" + str(size) + ".png"
    filename_white_fight = "whitefight" + str(size) + ".png"
    filename_red_fight = "redfight" + str(size) + ".png"
    floor_path = os.path.join(image_path, filename_floor)
    wall_path = os.path.join(image_path, filename_wall)
    key_path = os.path.join(image_path, filename_key)
    gate_path = os.path.join(image_path, filename_gate)
    trap_path = os.path.join(image_path, filename_trap)
    stair_path = os.path.join(image_path, filename_stair)
    explorer_path = os.path.join(image_path, filename_explorer)
    mummy_white_path = os.path.join(image_path, filename_mummy_white)
    mummy_red_path = os.path.join(image_path, filename_mummy_red)
    scorpion_white_path = os.path.join(image_path, filename_scorpion_white)
    scorpion_red_path = os.path.join(image_path, filename_scorpion_red)
    white_fight_path = os.path.join(image_path, filename_white_fight)
    red_fight_path = os.path.join(image_path, filename_red_fight)
    return backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path, explorer_path, \
        mummy_white_path, mummy_red_path, scorpion_white_path, scorpion_red_path, white_fight_path, red_fight_path

def cal_coordinates(game, position_x, position_y):
    coordinate_x = game.coordinate_screen_x + game.cell_rect * (position_y // 2)
    coordinate_y = game.coordinate_screen_y + game.cell_rect * (position_x // 2)
    if game.maze[position_x - 1][position_y] == "%" or game.maze[position_x - 1][position_y] == "G":
        coordinate_y += 3
    return [coordinate_x, coordinate_y]

def character_same_place_with_key(character, render, screen, game, backdrop, floor, stair, stair_position, trap, trap_position, key, key_position, 
                                  gate, gate_sheet, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red):
    if (key_position):
        if (key_position[0] == character.get_x() and key_position[1] == character.get_y()):
            if (gate["isClosed"] == True):
                gate["isClosed"] = False
            else:
                gate["isClosed"] = True
            if (render):
                graphics.gate_animation(screen, game, backdrop, floor, stair, stair_position, trap, trap_position, key, key_position, 
                                        gate_sheet, gate, wall, explorer, mummy_white, mummy_red, scorpion_white, scorpion_red)
            if (gate["isClosed"] == True):
                gate["cellIndex"] = 0
            else:
                gate["cellIndex"] = -1
    return gate

def update_same_character(list_character, list_sprite_sheet_character,
                          enemy_past_position, enemy_new_position):
    i = 0
    while (i < len(list_character)):
        j = 0
        while (j < len(list_character)):
            if (i != j and list_character[i].check_same_position(list_character[j])):
                del list_character[j]
                del list_sprite_sheet_character[j]
                del enemy_past_position[j]
                del enemy_past_position[j]
            else: j += 1
        i += 1
    return list_character, list_sprite_sheet_character

def update_diff_character(list_strong_character, list_weak_character, list_sprite_sheet_weak_character,
                          enemy_past_position, enemy_new_position):
    i = 0
    while (i < len(list_strong_character)):
        j = 0 
        while (j < len(list_weak_character)):
            if (list_strong_character[i].check_same_position(list_weak_character[j])):
                del list_weak_character[j]
                del list_sprite_sheet_weak_character[j]
                del enemy_past_position[j]
                del enemy_new_position[j]
            else: j += 1
        i += 1
    return list_weak_character, list_sprite_sheet_weak_character

def update_all_lists_character(mummy_white_character, list_mummy_white, mw_past_position, mw_new_position,
                               mummy_red_character, list_mummy_red, mr_past_position, mr_new_position,
                               scorpion_white_character, list_scorpion_white, sw_past_position, sw_new_position,
                               scorpion_red_character, list_scorpion_red, sr_past_position, sr_new_position
                               ):
    # Delete mummy white have same position
    mummy_white_character, list_mummy_white = update_same_character(mummy_white_character, list_mummy_white, mw_past_position, mw_new_position)
    # Delte same mummy red have same position
    mummy_red_character, list_mummy_red = update_same_character(mummy_red_character, list_mummy_red, mr_past_position, mr_new_position)
    # Delete same scorpion white have same position
    scorpion_white_character, list_scorpion_white = update_same_character(scorpion_white_character, list_scorpion_white, sw_past_position, sw_new_position)
    # Delete same scorpion white have same position
    scorpion_red_character, list_scorpion_red = update_same_character(scorpion_red_character, list_scorpion_red, sr_past_position, sr_new_position)

    # Delete mummy red, scropion white, scorpion red if mummy white have the same position
    if mummy_red_character:
        mummy_red_character, list_mummy_red = update_diff_character(mummy_white_character, mummy_red_character,
                                                                    list_mummy_red, mr_past_position, mr_new_position)
    if scorpion_white_character:
        scorpion_white_character, list_scorpion_white = update_diff_character(mummy_white_character,
                                                                            scorpion_white_character,
                                                                            list_scorpion_white, sw_past_position, sw_new_position)
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_diff_character(mummy_white_character,
                                                                        scorpion_red_character,
                                                                        list_scorpion_red, sr_past_position, sr_new_position)
    # Delete scropion white, scorpion red if mummy red have the same position
    if scorpion_white_character:
        scorpion_white_character, list_scorpion_white = update_diff_character(mummy_red_character,
                                                                            scorpion_white_character,
                                                                            list_scorpion_white, sw_past_position, sw_new_position)
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_diff_character(mummy_red_character,
                                                                        scorpion_red_character,
                                                                        list_scorpion_red, sr_past_position, sr_new_position)
    # Delete scorpion red if scorpion white have the same position
    if scorpion_red_character:
        scorpion_red_character, list_scorpion_red = update_diff_character(scorpion_white_character,
                                                                        scorpion_red_character,
                                                                        list_scorpion_red, sr_past_position, sr_new_position)

def check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
                             scorpion_red_character, trap_position):
    if (trap_position):
        if (explorer_character.get_x() == trap_position[0] and explorer_character.get_y() == trap_position[1]):
            return True
    
    if (mummy_white_character):
        for i in range(len(mummy_white_character)):
            if (explorer_character.get_x() == mummy_white_character[i].get_x() and explorer_character.get_y() == mummy_white_character[i].get_y()):
                return True
            
    if (mummy_red_character):
        for i in range(len(mummy_red_character)):
            if (explorer_character.get_x() == mummy_red_character[i].get_x() and explorer_character.get_y() == mummy_red_character[i].get_y()):
                return True
            
    if (scorpion_white_character):
        for i in range(len(scorpion_white_character)):
            if (explorer_character.get_x() == scorpion_white_character[i].get_x() and explorer_character.get_y() == scorpion_white_character[i].get_y()):
                return True
    
    if (scorpion_red_character):
        for i in range(len(scorpion_red_character)):
            if (explorer_character.get_x() == scorpion_red_character[i].get_x() and explorer_character.get_y() == scorpion_red_character[i].get_y()):
                return True
    
    return False

def enemy_move_one_step(enemy_character, move_type, render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red):
    past_position = []
    new_position = []

    for i in range(len(enemy_character)):
        past_position.append([enemy_character[i].get_x(), enemy_character[i].get_y()])
        if move_type == "white":
            enemy_character[i] = enemy_character[i].white_move(game.maze, game.gate, explorer_character)
        else:
            enemy_character[i] = enemy_character[i].red_move(game.maze, game.gate, explorer_character)
        new_position.append([enemy_character[i].get_x(), enemy_character[i].get_y()])
    
    for i in range(len(enemy_character)):
        game.gate = character_same_place_with_key(enemy_character[i], render, screen, game, backdrop, floor, stair, game.stair_position, trap, game.trap_position,
                                                key, game.key_position, game.gate, gate, wall, explorer, list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
    
    return past_position, new_position
    

def update_enemy_position(render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red):
    game.gate = character_same_place_with_key(explorer_character, render, screen, game, backdrop, floor, stair, game.stair_position, trap, game.trap_position,
                                            key, game.key_position, game.gate, gate, wall, explorer, list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
    
    if (check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
                             scorpion_red_character, game.trap_position)):
        return True
    
    mw_past_position, mw_new_position = [], []
    mr_past_position, mr_new_position = [], []
    sw_past_position, sw_new_position = [], []
    sr_past_position, sr_new_position = [], []

    # Mummy White di chuyển bước 1
    mw_past_position, mw_new_position = enemy_move_one_step(mummy_white_character, "white", render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)
    # Mummy Red di chuyển bước 1
    mr_past_position, mr_new_position = enemy_move_one_step(mummy_red_character, "red", render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)
    # Scorpion White di chuyển bước 1
    sw_past_position, sw_new_position = enemy_move_one_step(scorpion_white_character, "white", render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)
    # Scorpion Red di chuyển bước 1
    sr_past_position, sr_new_position = enemy_move_one_step(scorpion_red_character, "red", render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)
    
    if render:
        graphics.enemy_move_animation(mw_past_position, mw_new_position, mr_past_position, mr_new_position,
                                    sw_past_position, sw_new_position, sr_past_position, sr_new_position,
                                    screen, game, backdrop, floor, stair, game.stair_position, trap, game.trap_position, key, game.key_position, 
                                    gate, game.gate, wall, explorer, list_mummy_white, list_mummy_red, list_scorpion_white,
                                    list_scorpion_red)
        
    if (check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
                            scorpion_red_character, game.trap_position)):
        return True
    
    update_all_lists_character(mummy_white_character, list_mummy_white, mw_past_position, mw_new_position,
                               mummy_red_character, list_mummy_red, mr_past_position, mr_new_position,
                               scorpion_white_character, list_scorpion_white, sw_past_position, sw_new_position,
                               scorpion_red_character, list_scorpion_red, sr_past_position, sr_new_position
                               )
    
    sw_past_position = sw_new_position.copy()
    sr_past_position = sr_new_position.copy()

    # Mummy White di chuyển bước 2
    mw_past_position, mw_new_position = enemy_move_one_step(mummy_white_character, "white", render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)
    # Mummy Red di chuyển bước 2
    mr_past_position, mr_new_position = enemy_move_one_step(mummy_red_character, "red", render, screen, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)

    if render:
        graphics.enemy_move_animation(mw_past_position, mw_new_position, mr_past_position, mr_new_position,
                                    sw_past_position, sw_new_position, sr_past_position, sr_new_position,
                                    screen, game, backdrop, floor, stair, game.stair_position, trap, game.trap_position, key, game.key_position, 
                                    gate, game.gate, wall, explorer, list_mummy_white, list_mummy_red, list_scorpion_white,
                                    list_scorpion_red)
        
    if (check_explorer_is_killed(explorer_character, mummy_white_character, mummy_red_character, scorpion_white_character,
                            scorpion_red_character, game.trap_position)):
        return True
    
    update_all_lists_character(mummy_white_character, list_mummy_white, mw_past_position, mw_new_position,
                               mummy_red_character, list_mummy_red, mr_past_position, mr_new_position,
                               scorpion_white_character, list_scorpion_white, sw_past_position, sw_new_position,
                               scorpion_red_character, list_scorpion_red, sr_past_position, sr_new_position
                               )
    
    if render:
        graphics.draw_screen(screen, game.maze, game.maze_size, game.cell_rect, backdrop, floor, stair, game.stair_position,
                             trap, game.trap_position, key, game.key_position, gate, game.gate, wall, explorer, list_mummy_white, 
                             list_mummy_red, list_scorpion_white, list_scorpion_red)
        pygame.display.update()

    if game.maze[explorer_character.get_x() - 1][explorer_character.get_y()] == "S" or \
        game.maze[explorer_character.get_x() + 1][explorer_character.get_y()] == "S" or \
        game.maze[explorer_character.get_x()][explorer_character.get_y() - 1] == "S" or \
        game.maze[explorer_character.get_x()][explorer_character.get_y() + 1] == "S":
        print("=== YOU HAVE ESCAPED MAZE SUCCESSFULLY ===")
        print("=== YOU WIN ===")
        return True
    
def rungame(level, render):
    game = GameState(level)

    backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path, explorer_path, \
    mummy_white_path, mummy_red_path, scorpion_white_path, scorpion_red_path, white_fight_path, \
    red_fight_path = load_image_path(game.maze_size)

    # LOAD IMAGE
    backdrop = pygame.image.load(backdrop_path)
    floor = pygame.image.load(floor_path)
    stair = graphics.stairs_spritesheet(stair_path)
    trap = graphics.trap_spritesheet(trap_path)
    key = graphics.key_spritesheet(key_path)
    gate = graphics.gate_spritesheet(gate_path)
    wall = graphics.wall_spritesheet(wall_path, game.maze_size)
    explorer_sheet = graphics.character_spritesheet(explorer_path)
    mummy_white_sheet = graphics.character_spritesheet(mummy_white_path)
    mummy_red_sheet = graphics.character_spritesheet(mummy_red_path)
    scorpion_white_sheet = graphics.character_spritesheet(scorpion_white_path)
    scorpion_red_sheet = graphics.character_spritesheet(scorpion_red_path)

    # GAME
    explorer = {
        "sprite_sheet": explorer_sheet,
        "coordinates": cal_coordinates(game, game.explorer_position[0], game.explorer_position[1]),
        "direction": game.explorer_direction,
        "cellIndex": 0
    }

    list_mummy_white = []
    for i in range(len(game.mummy_white_position)):
         mummy_white = {
             "sprite_sheet": mummy_white_sheet,
             "coordinates": cal_coordinates(game, game.mummy_white_position[i][0], game.mummy_white_position[i][1]),
             "direction": game.mummy_white_direction[i],
             "cellIndex": 0
         }
         list_mummy_white.append(mummy_white)

    list_mummy_red = []
    for i in range(len(game.mummy_red_position)):
        mummy_red = {
            "sprite_sheet": mummy_red_sheet,
            "coordinates": cal_coordinates(game, game.mummy_red_position[i][0], game.mummy_red_position[i][1]),
            "direction": game.mummy_red_direction[i],
            "cellIndex": 0
        }
        list_mummy_red.append(mummy_red)

    list_scorpion_white = []
    for i in range(len(game.scorpion_white_position)):
        scorpion_white = {
            "sprite_sheet": scorpion_white_sheet,
            "coordinates": cal_coordinates(game, game.scorpion_white_position[i][0], game.scorpion_white_position[i][1]),
            "direction": game.scorpion_white_direction[i],
            "cellIndex": 0
        }
        list_scorpion_white.append(scorpion_white)

    list_scorpion_red = []
    for i in range(len(game.scorpion_red_position)):
        scorpion_red = {
            "sprite_sheet": scorpion_red_sheet,
            "coordinates": cal_coordinates(game, game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]),
            "direction": game.scorpion_red_direction[i],
            "cellIndex": 0
        }
        list_scorpion_red.append(scorpion_red)
        
    if render:
        # Set Screen
        pygame.init()
        window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
        pygame.display.set_caption("Mummy Maze")
        # Set FPS
        FPS = 60
        clock = pygame.time.Clock()
        graphics.draw_screen(window, game.maze, game.maze_size, game.cell_rect, backdrop, floor, stair, game.stair_position,
                             trap, game.trap_position, key, game.key_position, gate, game.gate, wall, explorer, list_mummy_white, 
                             list_mummy_red, list_scorpion_white, list_scorpion_red)
        pygame.display.update()

    explorer_character = characters.Explorer(game.explorer_position[0], game.explorer_position[1])
    mummy_white_character = []
    if game.mummy_white_position:
        for i in range(len(game.mummy_white_position)):
            mummy_white_character.append(characters.mummy_white(game.mummy_white_position[i][0], game.mummy_white_position[i][1]))
    mummy_red_character = []
    if game.mummy_red_position:
        for i in range(len(game.mummy_red_position)):
            mummy_red_character.append(characters.mummy_red(game.mummy_red_position[i][0], game.mummy_red_position[i][1]))
    scorpion_white_character = []
    if game.scorpion_white_position:
        for i in range(len(game.scorpion_white_position)):
            scorpion_white_character.append(characters.scorpion_white(game.scorpion_white_position[i][0], game.scorpion_white_position[i][1]))
    scorpion_red_character = []
    if game.scorpion_red_position:
        for i in range(len(game.scorpion_red_position)):
            scorpion_red_character.append(characters.scorpion_red(game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]))

    # DI CHUYỂN
    running = True
    move_queue = []          # mỗi phần tử: (new_x, new_y, direction)
    is_moving = False        # đang chạy animation Explorer + Mummy
    last_input_time = 0      # thời gian lần nhận input gần nhất (ms)
    INPUT_DELAY = 150        # không nhận input quá dày (< 150ms)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Lấy vị trí hiện tại
                explorer_x = explorer_character.get_x()
                explorer_y = explorer_character.get_y()
                explorer_new_x = explorer_x
                explorer_new_y = explorer_y

                if event.key == pygame.K_UP:
                    explorer_new_x -= 2
                    direction = "UP"
                if event.key == pygame.K_DOWN:
                    explorer_new_x += 2
                    direction = "DOWN"
                if event.key == pygame.K_LEFT:
                    explorer_new_y -= 2
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT:
                    explorer_new_y += 2
                    direction = "RIGHT"

                # Nếu có hướng và vị trí mới khác vị trí cũ
                if (explorer_new_x != explorer_x or explorer_new_y != explorer_y):
                    # Kiểm tra có đi hợp lệ không
                    if explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y,
                                                                  explorer_new_x, explorer_new_y):
                        # CHỈ THÊM VÀO HÀNG ĐỢI
                        move_queue.append((explorer_new_x, explorer_new_y, direction))
                
            # Xử lí click chuột
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                # Chống spam: không nhận click quá nhanh
                now = pygame.time.get_ticks()
                if now - last_input_time < INPUT_DELAY:
                    continue  # bỏ qua click này

                # Lấy tọa độ x, y pixel
                mouse_x, mouse_y = event.pos

                # Lấy vị trí explorer tại thời điểm click
                explorer_x = explorer_character.get_x()
                explorer_y = explorer_character.get_y()

                # 1. Đổi từ pixel sang ô (target_row, target_col) trong matrix
                target_row = (mouse_y - game.coordinate_screen_y) // game.cell_rect
                target_col = (mouse_x - game.coordinate_screen_x) // game.cell_rect

                # 2. Đổi từ matrix (row, col) sang chỉ số trong maze (ASCII)
                explorer_new_x = int(target_row * 2 + 1)
                explorer_new_y = int(target_col * 2 + 1)

                # 3. Chỉ cho click vào ô kề cạnh
                is_neighbor = (
                    (abs(explorer_x - explorer_new_x) == 2 and explorer_y == explorer_new_y) or
                    (abs(explorer_y - explorer_new_y) == 2 and explorer_x == explorer_new_x)
                )

                if is_neighbor and explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y,
                                                                              explorer_new_x, explorer_new_y):
                    # 4. Xác định hướng di chuyển
                    if explorer_new_x == explorer_x - 2:
                        direction = "UP"
                    elif explorer_new_x == explorer_x + 2:
                        direction = "DOWN"
                    elif explorer_new_y == explorer_y - 2:
                        direction = "LEFT"
                    elif explorer_new_y == explorer_y + 2:
                        direction = "RIGHT"
                    else:
                        pass

                    move_queue.append((explorer_new_x, explorer_new_y, direction))
                    last_input_time = now
        # ================== XỬ LÝ HÀNG ĐỢI LỆNH DI CHUYỂN ==================
        if (not is_moving) and move_queue:
            # Lấy lệnh đầu tiên trong queue (FIFO)
            target_x, target_y, direction = move_queue.pop(0)

            # Lấy lại vị trí hiện tại của Explorer
            explorer_x = explorer_character.get_x()
            explorer_y = explorer_character.get_y()

            # Chỉ cho phép di chuyển nếu vẫn kề cạnh + hợp lệ tại thời điểm thực thi
            is_neighbor = (
                (abs(explorer_x - target_x) == 2 and explorer_y == target_y) or
                (abs(explorer_y - target_y) == 2 and explorer_x == target_x)
            )

            if is_neighbor and explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y,
                                                                          target_x, target_y):
                # Set hướng
                explorer["direction"] = direction

                # Bắt đầu animation → khóa input
                is_moving = True
                
                explorer_character.move(target_x, target_y, render, window, game, backdrop, floor, stair, game.stair_position, trap, game.trap_position, \
                                        key, game.key_position, gate, game.gate, wall, explorer, list_mummy_white, \
                                        list_mummy_red, list_scorpion_white, list_scorpion_red)

                # Sau khi người chơi đi xong thì cho quái di chuyển
                isEnd = update_enemy_position(render, window, game, backdrop, floor, stair, trap, key, gate, wall, explorer, explorer_character, mummy_white_character,
                          mummy_red_character, scorpion_white_character, scorpion_red_character, list_mummy_white,
                          list_mummy_red, list_scorpion_white, list_scorpion_red)
                if isEnd:
                    running = False

                # Kết thúc lượt → mở khóa
                is_moving = False
        # Giới hạn FPS để game mượt và ổn định
        clock.tick(FPS)

# Điều kiện này làm cho các câu lệnh bên dưới chỉ chạy từ file gốc này
# Khi import file main cho các file khác if sẽ sai -> Không chạy game
if __name__ == "__main__":
    # Tạo đường dẫn đến thư mục gốc
    project_path = os.getcwd()
    # Tạo đường dẫn đến thư mục map
    map_path = os.path.join(project_path, "map")
    # Tạo đường dẫn đến thư mục agents
    agents_path = os.path.join(map_path, "agents")
    # Tạo đường dẫn đến thư mục maze
    maze_path = os.path.join(map_path, "maze")

    print("===== CHOOSE LEVEL ===== ")
    pre_level = input("INPUT LEVEL 1 - 10 YOU WANT SOLVE: ")
    level = pre_level + ".txt"
    render = True
    rungame(level, render)