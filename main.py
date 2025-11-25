import pygame
import os

import graphics
import characters

# Trạng thái game
class GameState:
    def __init__(self, file_name):
        """
        Giải thích vì sao có các kích thước bên dưới:
        - maze_rect = 360 vì chúng ta có mê cung 6x6, 8x8, 10x10. 360 đáp ứng chia hết cho 6, 8, 10
        - size_x, size_y tui nghĩ là lấy bất kì hoặc liên quan đến backdrop
        - coor_x tính bằng (size_x - maze_rect) /2
        - coor_y tính bằng (size_y - maze_rect) /2
        """
        self.maze_rect              = 360
        self.screen_size_x          = 494
        self.screen_size_y          = 480
        self.coordinate_screen_x    = 67
        self.coordinate_screen_y    = 80
        self.get_input_maze(file_name)
        self.get_input_object(file_name)
        self.gate                   = dict()
        if self.gate_position:
            self.gate = {
                "gate_position": self.gate_position,
                "isClosed":      True,
                "cellIndex":     0
            }
        # Set hướng ban đầu cho nhân vật
        # Mặc định người chơi nửa trái bản đồ thì là Right và ngược lại
        set_explorer_direction_default = True
        if set_explorer_direction_default:
            if self.explorer_position[1] // 2 <= self.maze_size // 2:
                self.explorer_direction = "RIGHT"
            else:
                self.explorer_direction = "LEFT"

        # Set hướng ban đầu cho các quái
        # Mặc định ban đầu hướng xuống
        set_objects_direction_default = True
        if set_objects_direction_default:
            self.mummy_white_direction      = ["DOWN"]*len(self.mummy_white_position)
            self.mummy_red_direction        = ["DOWN"]*len(self.mummy_red_position)
            self.scorpion_white_direction   = ["DOWN"]*len(self.scorpion_white_position)
            self.scorpion_red_direction     = ["DOWN"]*len(self.scorpion_red_position)

    def get_input_maze(self, file_name):
        # Lấy dữ liệu mê cung ASCII lưu vào maze
        self.maze           = []
        self.stair_position = ()
        self.trap_position  = ()
        self.key_position   = ()
        self.gate_position  = ()
        with open(os.path.join(maze_path, file_name), "r") as file:
            for line in file:
                row = []
                for chr in line:
                    if chr != '\n':
                        row.append(chr)
                self.maze.append(row)

        # Mê cung ASCII vừa biểu diễn đường đi vừa biểu diễn tường nên size nó gấp đôi
        # Ô thứ tự lẻ là tường, ô thứ tự chẵn là đường đi
        self.maze_size = len(self.maze) // 2
        self.cell_rect = self.maze_rect // self.maze_size

        # Tìm vị trí các vật phẩm trong mê cung
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 'S':
                    self.stair_position = (i, j)
                if self.maze[i][j] == 'T':
                    self.trap_position  = (i, j)
                if self.maze[i][j] == 'K':
                    self.key_position   = (i, j)
                if self.maze[i][j] == 'G':
                    self.gate_position  = (i, j)

    def get_input_object(self, file_name):
        # Tìm position ban đầu của người chơi và các quái
        self.mummy_white_position       = []
        self.mummy_red_position         = []
        self.scorpion_white_position    = []
        self.scorpion_red_position      = []
        with open(os.path.join(agents_path, file_name), "r") as file:
            for line in file:
                x = line.split()
                if x[0] == "E":
                    self.explorer_position = [int(x[1]), int(x[2])]
                if x[0] == "MW":
                    self.mummy_white_position.append(
                        [int(x[1]), int(x[2])]
                    )
                if x[0] == "MR":
                    self.mummy_red_position.append(
                        [int(x[1]), int(x[2])]
                    )
                if x[0] == "SW":
                    self.scorpion_white_position.append(
                        [int(x[1]), int(x[2])]
                    )
                if x[0] == "SR":
                    self.scorpion_red_position.append(
                        [int(x[1]), int(x[2])]
                    )

# Tính toán tọa độ pixel từ vị trí trong mê cung
def Cal_coordinates(game, position_x, position_y):
    x = game.coordinate_screen_x + game.cell_rect * (position_y // 2)
    y = game.coordinate_screen_y + game.cell_rect * (position_x // 2)
    # Đẩy nhân vật xuống 3 pixel để phần đầu không bị đè lên tường
    if game.maze[position_x - 1][position_y] == "%":
        y += 3
    return [x, y]

# Tạo đường dẫn đến hình ảnh
def load_image_path(size):
    # Tạo đường dẫn đến thư mục image trong thư mục gốc
    image_path = os.path.join(project_path, "image")
    # Backdrop
    backdrop_path       = os.path.join(image_path, "backdrop.png")
    # Floor
    floor_path          = os.path.join(image_path,  "floor"         + str(size) + ".jpg")
    # Wall
    wall_path           = os.path.join(image_path,  "walls"         + str(size) + ".png")
    # Key
    key_path            = os.path.join(image_path,  "key"           + str(size) + ".png")
    # Gate
    gate_path           = os.path.join(image_path,  "gate"          + str(size) + ".png")
    # Trap
    trap_path           = os.path.join(image_path,  "trap"          + str(size) + ".png")
    # Stair
    stair_path          = os.path.join(image_path,  "stairs"        + str(size) + ".png")
    # Explorer
    explorer_path       = os.path.join(image_path,  "explorer"      + str(size) + ".png")
    # Mummy white
    mummy_white_path    = os.path.join(image_path,  "mummy_white"   + str(size) + ".png")
    # Mummy red
    mummy_red_path      = os.path.join(image_path,  "redmummy"      + str(size) + ".png")
    # Scorpion white
    scorpion_white_path = os.path.join(image_path,  "white_scorpion"+ str(size) + ".png")
    # Scorpion_red
    scorpion_red_path   = os.path.join(image_path,  "red_scorpion"  + str(size) + ".png")
    # White_fight
    white_fight_path    = os.path.join(image_path,  "whitefight"    + str(size) + ".png")
    # Red_fight
    red_fight_path = os.path.join(image_path,       "redfight"      + str(size) + ".png")

    return backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path,\
        explorer_path, mummy_white_path, mummy_red_path,\
        scorpion_white_path, scorpion_red_path,\
        white_fight_path, red_fight_path

def update_gate(character, screen, game, backdrop, floor,
                stair, stair_position, trap, trap_position, key, key_position,
                gate_sheet, gate, wall,
                explorer,
                mummy_white, mummy_red,
                scorpion_white, scorpion_red):
    if key_position and \
        character.get_x() == key_position[0] and \
        character.get_y() == key_position[1]:
        gate["isClosed"] = not gate["isClosed"]
        graphics.gate_animation(screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                                key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red,
                                scorpion_white, scorpion_red)
        if gate["isClosed"]:
            gate["cellIndex"] = 0
        else:
            gate["cellIndex"] = -1
    return gate

def check_explorer_is_killed(explorer_character,
                             mummy_white_character, mummy_red_character,
                             scorpion_white_character, scorpion_red_character,
                             trap_position):
    if trap_position:
        if explorer_character.get_x() == trap_position[0] and \
                explorer_character.get_y() == trap_position[1]:
            return True
    if mummy_white_character:
        for i in range(len(mummy_white_character)):
            if explorer_character.get_x() == mummy_white_character[i].get_x() and \
                    explorer_character.get_y() == mummy_white_character[i].get_y():
                return True
    if mummy_red_character:
        for i in range(len(mummy_red_character)):
            if explorer_character.get_x() == mummy_red_character[i].get_x() and \
                    explorer_character.get_y() == mummy_red_character[i].get_y():
                return True
    if scorpion_white_character:
        for i in range(len(scorpion_white_character)):
            if explorer_character.get_x() == scorpion_white_character[i].get_x() and \
                    explorer_character.get_y() == scorpion_white_character[i].get_y():
                return True
    if scorpion_red_character:
        for i in range(len(scorpion_red_character)):
            if explorer_character.get_x() == scorpion_red_character[i].get_x() and \
                    explorer_character.get_y() == scorpion_red_character[i].get_y():
                return True
    return False

def update_list_same_character(list_character, list_sprite_sheet_character):
    i = 0
    while i < len(list_character):
        j = 0
        while j < len(list_character):
            if j != i and list_character[i].check_same_position(list_character[j]):
                del list_character[j]
                del list_sprite_sheet_character[j]
            else:
                j += 1
        i += 1
    return list_character, list_sprite_sheet_character

def update_list_diff_character(list_strong_character, list_week_character, list_sprite_sheet_week_character):
    for i in range(len(list_strong_character)):
        j = 0
        while j < len(list_week_character):
            if list_strong_character[i].check_same_position(list_week_character[j]):
                del list_week_character[j]
                del list_sprite_sheet_week_character[j]
            else:
                j += 1
    return list_week_character, list_sprite_sheet_week_character

def enemy_white_move(enemy_character, explorer_character,
                     game):
    past_position   = []
    new_position    = []
    for i in range(len(enemy_character)):
        past_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )
        # Cho mummy di chuyển
        enemy_character[i] = enemy_character[i].white_move(game.maze, game.gate, explorer_character)
        # Cập nhật lại vị trí mummy
        new_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )

    return past_position, new_position, enemy_character

def enemy_red_move(enemy_character, explorer_character,
                     game):
    past_position   = []
    new_position    = []
    for i in range(len(enemy_character)):
        past_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )
        # Cho mummy di chuyển
        enemy_character[i] = enemy_character[i].red_move(game.maze, game.gate, explorer_character)
        # Cập nhật lại vị trí mummy
        new_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )

    return past_position, new_position, enemy_character

def update_enemy_position(window, game, backdrop, floor,
                          stair, trap, key, gate, wall,
                          explorer, explorer_character,
                          mummy_white_character, list_mummy_white,
                          mummy_red_character, list_mummy_red,
                          scorpion_white_character, list_scorpion_white,
                          scorpion_red_character, list_scorpion_red):

    game.gate = update_gate(explorer_character, window, game, backdrop, floor,
                            stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                            gate, game.gate, wall,
                            explorer,
                            list_mummy_white, list_mummy_red,
                            list_scorpion_white, list_scorpion_red)

    # Gọi hàm kiểm tra xem mummy có trùng vị trí với người chơi không
    if check_explorer_is_killed(explorer_character,
                                mummy_white_character, mummy_red_character,
                                scorpion_white_character, scorpion_red_character,
                                game.trap_position):
        return False
    # -------------------------------MUMMY WHITE FIRST MOVE-------------------------------
    mw_past_position, mw_new_position, mummy_white_character    = enemy_white_move(mummy_white_character, explorer_character, game)
    for i in range(len(mummy_white_character)):
        game.gate = update_gate(mummy_white_character[i], window, game, backdrop, floor,
                                stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red)

    # -------------------------------MUMMY RED FIRST MOVE---------------------------------
    mr_past_position, mr_new_position, mummy_red_character      = enemy_red_move(mummy_red_character, explorer_character, game)
    for i in range(len(mummy_red_character)):
        game.gate = update_gate(mummy_red_character[i], window, game, backdrop, floor,
                                stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red)

    # -------------------------------SCORPION WHITE FIRST MOVE----------------------------
    sw_past_position, sw_new_position, scorpion_white_character = enemy_white_move(scorpion_white_character, explorer_character, game)
    for i in range(len(scorpion_white_character)):
        game.gate = update_gate(scorpion_white_character[i], window, game, backdrop, floor,
                                stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red)

    # -------------------------------SCORPION RED FIRST MOVE------------------------------
    sr_past_position, sr_new_position, scorpion_red_character   = enemy_red_move(scorpion_red_character, explorer_character, game)
    for i in range(len(scorpion_red_character)):
        game.gate = update_gate(scorpion_red_character[i], window, game, backdrop, floor,
                                stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red)

    # -------------------------------DRAW MOVE ANIMATION----------------------------------
    draw = True
    if draw:
        graphics.enemy_move_animation(mw_past_position, mw_new_position,
                                      mr_past_position, mr_new_position,
                                      sw_past_position, sw_new_position,
                                      sr_past_position, sr_new_position,
                                      window, game, backdrop, floor,
                                      stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                      gate, game.gate, wall,
                                      explorer,
                                      list_mummy_white, list_mummy_red,
                                      list_scorpion_white, list_scorpion_red)

    # Check lại sau bước 1 đã thua chưa
    if check_explorer_is_killed(explorer_character,
                                mummy_white_character, mummy_red_character,
                                scorpion_white_character, scorpion_red_character,
                                game.trap_position):
        return False

    # -------------------------------DELETE ENEMY SAME POSITION---------------------------
    Delete_enemy_same_position = True
    if Delete_enemy_same_position:
        # Xóa các quái cùng loại
        Delete_same_object = True
        if Delete_same_object:
            # Xóa mummy white cùng vị trí
            mummy_white_character, list_mummy_white             = update_list_same_character(
                                                                    mummy_white_character, list_mummy_white
                                                                )
            # Xóa mummy red cùng vị trí
            mummy_red_character, list_mummy_red                 = update_list_same_character(
                                                                    mummy_red_character, list_mummy_red
                                                                )
            # Xóa scorpion white cùng vị trí
            scorpion_white_character, list_scorpion_white       = update_list_same_character(
                                                                    scorpion_white_character,  list_scorpion_white
                                                                )
            # Xóa scorpion red cùng vị trí
            scorpion_red_character, list_scorpion_red           = update_list_same_character(
                                                                    scorpion_red_character, list_scorpion_red
                                                                )

        # Xóa các quái khác loại
        # Thứ tự sức mạnh các quái giảm dần: mummy_white, mummy_red, scorpion_white, scorpion_red
        Delete_diff_object = True
        if Delete_diff_object:
            # Xóa mummy red nếu cùng vị trí với mummy white
            if mummy_red_character:
                mummy_red_character, list_mummy_red             = update_list_diff_character(
                                                                    mummy_white_character, mummy_red_character, list_mummy_red
                                                                )
            # Xóa scorpion white nếu cùng vị trí với mummy white
            if scorpion_white_character:
                scorpion_white_character, list_scorpion_white   = update_list_diff_character(
                                                                    mummy_white_character, scorpion_white_character, list_scorpion_white
                                                                )
            # Xóa scorpion red nếu cùng vị trí với mummy white
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red       = update_list_diff_character(
                                                                    mummy_white_character, scorpion_red_character, list_scorpion_red
                                                                )
            # Xóa scropion white nếu cùng vị trí với mummy red
            if scorpion_white_character:
                scorpion_white_character, list_scorpion_white   = update_list_diff_character(
                                                                    mummy_red_character, scorpion_white_character, list_scorpion_white
                                                                )
            # Xóa scorpion red nếu cùng vị trí với mummy red
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red       = update_list_diff_character(
                                                                    mummy_red_character, scorpion_red_character, list_scorpion_red
                                                                )
            # Xóa scorpion red nếu cùng vị trí với scorpion white
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red       = update_list_diff_character(
                                                                    scorpion_white_character, scorpion_red_character, list_scorpion_red
                                                                )
    sw_past_position = sw_new_position.copy()
    sr_past_position = sr_new_position.copy()

    # -------------------------------MUMMY WHITE SECOND MOVE------------------------------
    mw_past_position, mw_new_position, mummy_white_character    = enemy_white_move(mummy_white_character, explorer_character, game)
    for i in range(len(mummy_white_character)):
        game.gate = update_gate(mummy_white_character[i], window, game, backdrop, floor,
                                stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red)

    # -------------------------------MUMMY RED SECOND MOVE--------------------------------
    mr_past_position, mr_new_position, mummy_red_character      = enemy_red_move(mummy_red_character, explorer_character, game)
    for i in range(len(mummy_red_character)):
        game.gate = update_gate(mummy_red_character[i], window, game, backdrop, floor,
                                stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red)

    # -------------------------------DRAW MOVE ANIMATION----------------------------------
    draw = True
    if draw:
        graphics.enemy_move_animation(mw_past_position, mw_new_position,
                                      mr_past_position, mr_new_position,
                                      sw_past_position, sw_new_position,
                                      sr_past_position, sr_new_position,
                                      window, game, backdrop, floor,
                                      stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                      gate, game.gate, wall,
                                      explorer,
                                      list_mummy_white, list_mummy_red,
                                      list_scorpion_white, list_scorpion_red)

    # Check lại sau bước 2 đã thua chưa
    if check_explorer_is_killed(explorer_character,
                                mummy_white_character, mummy_red_character,
                                scorpion_white_character, scorpion_red_character,
                                game.trap_position):
        return False

    # -------------------------------DELETE ENEMY SAME POSITION---------------------------
    Delete_enemy_same_position = True
    if Delete_enemy_same_position:
        # Xóa các quái cùng loại
        Delete_same_object = True
        if Delete_same_object:
            # Xóa mummy white cùng vị trí
            mummy_white_character, list_mummy_white         = update_list_same_character(
                                                                mummy_white_character, list_mummy_white
                                                            )
            # Xóa mummy red cùng vị trí
            mummy_red_character, list_mummy_red             = update_list_same_character(
                                                                mummy_red_character, list_mummy_red
                                                            )
            # Xóa scorpion white cùng vị trí
            scorpion_white_character, list_scorpion_white   = update_list_same_character(
                                                                scorpion_white_character, list_scorpion_white
                                                            )
            # Xóa scorpion red cùng vị trí
            scorpion_red_character, list_scorpion_red       = update_list_same_character(
                                                                scorpion_red_character, list_scorpion_red
                                                            )

        # Xóa các quái khác loại
        # Thứ tự sức mạnh các quái giảm dần: mummy_white, mummy_red, scorpion_white, scorpion_red
        Delete_diff_object = True
        if Delete_diff_object:
            # Xóa mummy red nếu cùng vị trí với mummy white
            if mummy_red_character:
                mummy_red_character, list_mummy_red             = update_list_diff_character(
                                                                    mummy_white_character, mummy_red_character, list_mummy_red
                                                                )
            # Xóa scorpion white nếu cùng vị trí với mummy white
            if scorpion_white_character:
                scorpion_white_character, list_scorpion_white   = update_list_diff_character(
                                                                    mummy_white_character, scorpion_white_character, list_scorpion_white
                                                                )
            # Xóa scorpion red nếu cùng vị trí với mummy white
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red       = update_list_diff_character(
                                                                    mummy_white_character, scorpion_red_character, list_scorpion_red
                                                                )
            # Xóa scropion white nếu cùng vị trí với mummy red
            if scorpion_white_character:
                scorpion_white_character, list_scorpion_white   = update_list_diff_character(
                                                                    mummy_red_character, scorpion_white_character, list_scorpion_white
                                                                )
            # Xóa scorpion red nếu cùng vị trí với mummy red
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red       = update_list_diff_character(
                                                                    mummy_red_character, scorpion_red_character, list_scorpion_red
                                                                )
            # Xóa scorpion red nếu cùng vị trí với scorpion white
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red = update_list_diff_character(
                                                                    scorpion_white_character, scorpion_red_character, list_scorpion_red
                                                                )
    # Check điều kiện thắng
    # Theo thứ tự 4 dòng bên dưới:
    # 1. Cửa ra nằm bên trên
    # 2. Cửa ra nằm bên dưới
    # 3. Cửa ra nằm bên trái
    # 4. Cửa ra nằm bn phải
    if  game.maze[explorer_character.get_x() - 1][explorer_character.get_y()    ]   == "S"    or \
        game.maze[explorer_character.get_x() + 1][explorer_character.get_y()    ]   == "S"    or \
        game.maze[explorer_character.get_x()    ][explorer_character.get_y() - 1]   == "S"    or \
        game.maze[explorer_character.get_x()    ][explorer_character.get_y() + 1]   == "S":
        print("YOU WIN!")
        return False
    return True

def rungame(level):
    # Lấy trạng thái game
    game = GameState(level)

    # Load image path
    backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path, \
        explorer_path, mummy_white_path, mummy_red_path, scorpion_white_path, scorpion_red_path,\
        white_fight_path, red_fight_path = load_image_path(game.maze_size)

    # Load image
    Load_image = True
    if Load_image:
        backdrop            = pygame.image.load             (backdrop_path)
        floor               = pygame.image.load             (floor_path)
        wall                = graphics.wall_spritesheet     (wall_path, game.maze_size)
        key                 = graphics.key_spritesheet      (key_path)
        gate                = graphics.gate_spritesheet     (gate_path)
        trap                = graphics.trap_spritesheet     (trap_path)
        stair               = graphics.stairs_spritesheet   (stair_path)
        explorer_sheet      = graphics.character_spritesheet(explorer_path)
        mummy_white_sheet   = graphics.character_spritesheet(mummy_white_path)
        mummy_red_sheet     = graphics.character_spritesheet(mummy_red_path)
        scorpion_white_sheet= graphics.character_spritesheet(scorpion_white_path)
        scorpion_red_sheet  = graphics.character_spritesheet(scorpion_red_path)

    # Objects
    # Mỗi object sẽ là một dict tương tự như struct bên C++ chứa 4 thứ
    # 1. sprite_sheet: Một hình ảnh chứa các ô frame trạng thái của object
    # 2. coordinates: Tọa độ hiện tại của object
    # 3. direction: Hướng quay của object (UP, DOWN, RIGHT, LEFT)
    # 4. cellIndex: Vị trí ô frame cần vẽ trong sprite_sheet
    initialize_objects = True
    if initialize_objects:
        explorer = {
            "sprite_sheet"  : explorer_sheet,
            "coordinates"   : Cal_coordinates(game,
                            game.explorer_position[0], game.explorer_position[1]
                            ),
            "direction"     : game.explorer_direction,
            "cellIndex"     : 0
        }

        list_mummy_white = []
        for i in range (len(game.mummy_white_position)):
            mummy_white = {
                "sprite_sheet"  : mummy_white_sheet,
                "coordinates"   : Cal_coordinates(game,
                                game.mummy_white_position[i][0], game.mummy_white_position[i][1]
                                ),
                "direction"     : game.mummy_white_direction[i],
                "cellIndex"     : 0
            }
            list_mummy_white.append(mummy_white)

        list_mummy_red = []
        for i in range(len(game.mummy_red_position)):
            mummy_red = {
                "sprite_sheet"  : mummy_red_sheet,
                "coordinates"   : Cal_coordinates(game,
                                game.mummy_red_position[i][0], game.mummy_red_position[i][1]
                                ),
                "direction"     : game.mummy_red_direction[i],
                "cellIndex"     : 0
            }
            list_mummy_red.append(mummy_red)

        list_scorpion_white = []
        for i in range(len(game.scorpion_white_position)):
            scorpion_white = {
                "sprite_sheet"  : scorpion_white_sheet,
                "coordinates"   : Cal_coordinates(game,
                                game.scorpion_white_position[i][0], game.scorpion_white_position[i][1]
                                ),
                "direction"     : game.scorpion_white_direction[i],
                "cellIndex"     : 0
            }
            list_scorpion_white.append(scorpion_white)

        list_scorpion_red = []
        for i in range(len(game.scorpion_red_position)):
            scorpion_red = {
                "sprite_sheet"  : scorpion_red_sheet,
                "coordinates"   : Cal_coordinates(game,
                                game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]
                                ),
                "direction"     : game.scorpion_red_direction[i],
                "cellIndex"     : 0
            }
            list_scorpion_red.append(scorpion_red)

    # Thiết lập các chỉ số cơ bản
    set_base = True
    if set_base:
        pygame.init()
        pygame.display.set_caption("Mummy Maze")
        FPS = 60
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))

        # Vẽ màn hình hiển thị ban đầu
        graphics.draw_screen(window, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                             stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                             gate, game.gate, wall,
                             explorer,
                             list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
        # Ở trên nó chỉ đẩy lên ô nhớ update để vẽ ra
        pygame.display.update()

    # Tạo các class của objects
    initialize_objects_class = True
    if initialize_objects_class:
        explorer_character      = characters.Explorer(game.explorer_position[0], game.explorer_position[1])
        mummy_white_character   = []
        if game.mummy_white_position:
            for i in range(len(game.mummy_white_position)):
                mummy_white_character.append(
                    characters.mummy_white(game.mummy_white_position[i][0], game.mummy_white_position[i][1]))
        mummy_red_character     = []
        if game.mummy_red_position:
            for i in range(len(game.mummy_red_position)):
                mummy_red_character.append(
                    characters.mummy_red(game.mummy_red_position[i][0], game.mummy_red_position[i][1]))
        scorpion_white_character= []
        if game.scorpion_white_position:
            for i in range(len(game.scorpion_white_position)):
                scorpion_white_character.append(
                    characters.scorpion_white(game.scorpion_white_position[i][0], game.scorpion_white_position[i][1]))
        scorpion_red_character  = []
        if game.scorpion_red_position:
            for i in range(len(game.scorpion_red_position)):
                scorpion_red_character.append(
                    characters.scorpion_red(game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]))

    running = True
    # HÀNG ĐỢI LỆNH DI CHUYỂN
    move_queue = []          # mỗi phần tử chứa: (new_x, new_y, direction)
    is_moving = False        # đang chạy animation Explorer + Mummy
    last_input_time = 0      # thời gian lần nhận input gần nhất (ms)
    INPUT_DELAY = 150        # không nhận input quá dày (< 150ms)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Lấy vị trí hiện tại
                explorer_x      = explorer_character.get_x()
                explorer_y      = explorer_character.get_y()
                explorer_new_x  = explorer_x
                explorer_new_y  = explorer_y

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

                # Nếu vị trí mới khác vị trí cũ
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

                explorer_character.move(target_x, target_y, window, game, backdrop, floor,
                                        stair, game.stair_position,trap, game.trap_position, key, game.key_position,
                                        gate, game.gate, wall,
                                        explorer,
                                        list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)

                # Sau khi người chơi đi xong thì cho quái di chuyển
                running = update_enemy_position(window, game, backdrop, floor,
                                                stair, trap, key, gate, wall,
                                                explorer, explorer_character,
                                                mummy_white_character, list_mummy_white,
                                                mummy_red_character, list_mummy_red,
                                                scorpion_white_character, list_scorpion_white,
                                                scorpion_red_character, list_scorpion_red)

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
    pre_level = input("INPUT LEVEL 1- 10 YOU WANT SOLVE: ")
    level = pre_level + ".txt"
    rungame(level)