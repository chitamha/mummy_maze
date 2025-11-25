import pygame
import os

import main

class character_spritesheet:
    def __init__(self, image_spritesheet_path):
        # Một character sẽ có 20 frame chứa trong 4 hàng 5 cột
        self.sheet      = pygame.image.load(image_spritesheet_path)
        self.rows       = 4
        self.cols       = 5
        self.totalCell  = self.rows * self.cols

        # Tính toán chiều rộng, cao của mỗi ô frame phục vụ cho việc trích xuất
        self.rect           = self.sheet.get_rect()
        w = self.cellWidth  = self.rect.width / self.cols
        h = self.cellHeight = self.rect.height / self.rows

        # Lần lượt thêm các frame vào list theo thứ tự sau:
        # 0 1 2 3 4
        # 5 .......
        # ......18 19
        self.cells = list()
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells.append([x * w, y * h, w, h])

    def draw(self, surface, x, y, cellIndex, direction):
        """
        Image chứa theo logic sau:
        - Hàng thứ 1 chứa 5 frame object quay lên trên      UP
        - Hàng thứ 2 chứa 5 frame object quay bên phải      RIGHT
        - Hàng thứ 3 chứa 5 frame object quay xuống dưới    DOWN
        - Hàng thứ 4 chứa 5 frame object quay bên trái      LEFT
        """
        if direction == "UP":
            pass
        if direction == "RIGHT":
            cellIndex += 5
        if direction == "DOWN":
            cellIndex += 10
        if direction == "LEFT":
            cellIndex += 15
        # Vẽ ô thứ cellIndex trong sprite_sheet từ tọa độ (x, y) lên surface
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class wall_spritesheet:
    def __init__(self, image_spritesheet_path, maze_size):
        self.sheet      = pygame.image.load(image_spritesheet_path)
        self.left_wall  = []
        self.right_wall = []
        self.up_wall    = []
        # Mỗi bộ 4 thông số bên dưới ý nghĩa là: x, y, width, height
        # Cắt từ ảnh bắt đầu từ tọa độ (x, y) cắt ngang width và xuống height
        # Anh tính sẵn cho mình lấy sử dụng là được
        if maze_size == 6:
            self.left_wall          = [0,  0, 12, 78]
            self.right_wall         = [84, 0, 12, 78]
            self.up_wall            = [12, 0, 72, 18]
            self.up_wall_no_shadow  = [12, 0, 66, 18]
        elif maze_size == 8:
            self.left_wall          = [0,  0, 12, 63]
            self.right_wall         = [69, 0, 12, 63]
            self.up_wall            = [12, 0, 57, 18]
            self.up_wall_no_shadow  = [12, 0, 51, 18]
        elif maze_size == 10:
            self.left_wall          = [0,  0, 8,  48]
            self.right_wall         = [52, 0, 8,  48]
            self.up_wall            = [8,  0, 44, 12]
            self.up_wall_no_shadow  = [8,  0, 38, 12]

    # Lệnh surface.blit(source, (x, y), area) có nghĩa:
    # Vẽ lên bề mặt surface ở tọa độ (x, y) một area của source ảnh
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
        self.sheet  = pygame.image.load(image_spritesheet_path)
        self.rect   = self.sheet.get_rect()
        self.cell   = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class gate_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet  = pygame.image.load(image_spritesheet_path)
        self.rect   = self.sheet.get_rect()
        # Số frame trong sheet gate là 8 trên cùng một hàng
        number_gate_sheet = 8
        # Tính toán chiều rộng chiều cao của frame để phục vụ cho việc trích xuất
        w = self.rect.width / number_gate_sheet
        h = self.rect.height
        self.cells  = []
        for x in range(number_gate_sheet):
            self.cells.append([x * w, 0, w, h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class trap_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet  = pygame.image.load(image_spritesheet_path)
        self.rect   = self.sheet.get_rect()
        self.cell   = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class stairs_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet  = pygame.image.load(image_spritesheet_path)
        self.rect   = self.sheet.get_rect()

        # Tính toán chiều rộng, cao của mỗi ô frame phục vụ cho việc trích xuất
        self.cell_w = self.rect.width // 4
        self.cell_h = self.rect.height

        # Lần lượt thêm các frame vào list theo thứ tự sau: 0 1 2 3
        self.stairs = []
        for x in range(4):
            self.stairs.append(
                [x * self.cell_w, 0, self.cell_w, self.cell_h]
            )

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.stairs[cellIndex])

def draw_screen(screen, input_maze, backdrop, floor, maze_size, cell_rect,
                stair, stair_position, trap, trap_position, key, key_position,
                gate_sheet, gate, wall,
                explorer,
                mummy_white, mummy_red, scorpion_white, scorpion_red):
    # Tọa độ bắt đầu của mê cung đồng bộ với trong file main
    coordinate_X    = 67
    coordinate_Y    = 80

    # Vẽ backdrop và floor đơn giản
    draw_backdrop_and_floor = True
    if draw_backdrop_and_floor:
        # Phải vẽ backdrop trước rồi tới floor để floor đè lên phần đen trong backdrop
        screen.blit(backdrop, (0, 0))
        screen.blit(floor, (coordinate_X, coordinate_Y))

    # Vẽ Stair
    draw_stair = True
    if draw_stair:
        # Tính xem stair nằm trong ô nào trong mê cung
        stair_px = stair_position[1] // 2
        stair_py = stair_position[0] // 2
        # Từ đó biến thành tọa độ pixel
        stair_x = coordinate_X + cell_rect * (stair_px)
        stair_y = coordinate_Y + cell_rect * (stair_py)
        # stair_index = (0, 1, 2, 3) lần lượt ứng với trạng thái (UP, RIGHT, DOWN, LEFT)
        # Các trường hợp bên dưới tưởng tượng để xét nó nằm ở cạnh nào trong mê cung hình vuông

        # STAIR IS UP
        stair_index = 0
        # STAIR IS RIGHT
        if  stair_px == maze_size:
            stair_index = 1
        # STAIR IS DOWN
        elif stair_py == maze_size:
            stair_index = 2
        # STAIR IS LEFT
        elif stair_px == 0:
            stair_index = 3

        # Nếu là UP chỉnh sửa một chút
        # Dịch cầu thang lên trên stair.cell_h pixel
        # Nếu không thì cầu thang bị đè lên mê cung
        if (stair_index == 0):
            stair_y = coordinate_Y - stair.cell_h
        # Nếu là Left cũng sửa một chút
        # Dịch cầu thang sang trái stair.cell_w
        if (stair_index == 3):
            stair_x = coordinate_X - stair.cell_w

        stair.draw(screen, stair_x, stair_y, stair_index)

    # Vẽ Trap
    if trap_position:
        trap_x = coordinate_X + cell_rect * (trap_position[1] // 2)
        trap_y = coordinate_Y + cell_rect * (trap_position[0] // 2)
        trap.draw(screen, trap_x, trap_y)

    # Vẽ Key
    if key_position:
        key_x = coordinate_X + cell_rect * (key_position[1] // 2)
        key_y = coordinate_Y + cell_rect * (key_position[0] // 2)
        key.draw(screen, key_x, key_y)

    # Vẽ gate
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

    # Vẽ Explorer
    if explorer["coordinates"]:
        # Các tham số truyền vào đọc hàm draw trong character_spritesheet để hiểu
        explorer["sprite_sheet"].draw(screen, explorer["coordinates"][0],
                                              explorer["coordinates"][1],
                                              explorer["cellIndex"],
                                              explorer["direction"])

    # Vẽ Mummy White
    if mummy_white:
        for i in range(len(mummy_white)):
            mummy_white[i]["sprite_sheet"].draw(screen,
                                                mummy_white[i]["coordinates"][0],
                                                mummy_white[i]["coordinates"][1],
                                                mummy_white[i]["cellIndex"],
                                                mummy_white[i]["direction"])

    # Vẽ Mummy Red
    if mummy_red:
        for i in range(len(mummy_red)):
            mummy_red[i]["sprite_sheet"].draw(screen,
                                              mummy_red[i]["coordinates"][0],
                                              mummy_red[i]["coordinates"][1],
                                              mummy_red[i]["cellIndex"],
                                              mummy_red[i]["direction"])

    # Vẽ Scorpion white
    if scorpion_white:
        for i in range(len(scorpion_white)):
            scorpion_white[i]["sprite_sheet"].draw(screen,
                                                   scorpion_white[i]["coordinates"][0],
                                                   scorpion_white[i]["coordinates"][1],
                                                   scorpion_white[i]["cellIndex"],
                                                   scorpion_white[i]["direction"])

    # Vẽ Scorpion red
    if scorpion_red:
        for i in range(len(scorpion_red)):
            scorpion_red[i]["sprite_sheet"].draw(screen,
                                                 scorpion_red[i]["coordinates"][0],
                                                 scorpion_red[i]["coordinates"][1],
                                                 scorpion_red[i]["cellIndex"],
                                                 scorpion_red[i]["direction"])

    # Vẽ tường
    draw_wall = True
    if draw_wall:
        # Horizontal Wall (Tường ngang)
        # Hàng chẵn chứa tường ngang
        # Tường nằm giữa 2 ô trống ngang nên ở cột lẻ
        for i in range(2, len(input_maze)-1, 2):
            for j in range(1, len(input_maze[i]), 2):
                if input_maze[i][j] == "%":
                    # Tính tọa độ tương tự hàm Cal_coordinate bên main
                    wall_x = coordinate_X + cell_rect * (j // 2)
                    wall_y = coordinate_Y + cell_rect * (i // 2)
                    # Trừ lại cho nó không bị lệch
                    # Anh test sẵn mình sử dụng thôi
                    if maze_size == 6 or maze_size == 8:
                        wall_x -= 6
                        wall_y -= 12
                    if maze_size == 10:
                        wall_x -= 3
                        wall_y -= 9
                    wall.draw_up_wall(screen, wall_x, wall_y)
        # Vertical Wall (Tường dọc)
        # Cột chẵn chứa tường dọc
        # Tường nằm giữa 2 ô trống dọc nên ở hàng lẻ
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
                    # Trường hợp mà tường tạo góc vuông thì sài right_wall bởi nó ngắn nó mới khớp
                    # Đây chính là trường hợp tường hình chữ L
                    if (input_maze[i+1][j+1] == "%"):
                        wall.draw_right_wall(screen, wall_x, wall_y)
                        # redraw ở đây là vẽ lại phần ngang của chữ L cho nó không thừa
                        redraw_x = coordinate_X + cell_rect * ((j+1) // 2)
                        redraw_y = coordinate_Y + cell_rect * ((i+1) // 2)
                        if maze_size == 6 or maze_size == 8:
                            redraw_x -= 6
                            redraw_y -= 12
                        if maze_size == 10:
                            redraw_x -= 3
                            redraw_y -= 9
                        # Vẽ lại tường ngang không bóng đổ
                        if (i + 1 < maze_size * 2 and j + 1 < maze_size * 2):
                            wall.draw_up_wall_no_shadow(screen, redraw_x, redraw_y)
                    else:
                        wall.draw_left_wall(screen, wall_x, wall_y)

def gate_animation(screen, game, backdrop, floor,
                   stair, stair_position, trap, trap_position, key, key_position,
                   gate_sheet, gate, wall,
                   explorer,
                   mummy_white, mummy_red,
                   scorpion_white, scorpion_red):
    if gate["isClosed"]:
        for i in range(8):
            gate["cellIndex"] = -(i+1)
            draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                        stair, stair_position, trap, trap_position, key, key_position,
                        gate_sheet, gate, wall,
                        explorer,
                        mummy_white, mummy_red,
                        scorpion_white, scorpion_red)
            pygame.time.delay(100)
            pygame.display.update()
    else:
        for i in range(8):
            gate["cellIndex"] = i
            draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                        stair, stair_position, trap, trap_position, key, key_position,
                        gate_sheet, gate, wall,
                        explorer,
                        mummy_white, mummy_red,
                        scorpion_white, scorpion_red)
            pygame.time.delay(100)
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

def enemy_move_animation(mw_past_position, mw_new_position,
                         mr_past_position, mr_new_position,
                         sw_past_position, sw_new_position,
                         sr_past_position, sr_new_position,
                         screen, game, backdrop, floor,
                         stair, stair_position, trap, trap_position, key, key_position,
                         gate_sheet, gate, wall,
                         explorer,
                         mummy_white, mummy_red,
                         scorpion_white, scorpion_red):
    def determine_coor_and_direction(past_position, new_position,
                                    check_movement, enemy):
        start_coordinate = []
        for i in range(len(past_position)):
            start_x = game.coordinate_screen_x + game.cell_rect * (past_position[i][1] // 2)
            start_y = game.coordinate_screen_y + game.cell_rect * (past_position[i][0] // 2)
            if game.maze[new_position[i][0] - 1][new_position[i][1]] == "%" or \
               game.maze[new_position[i][0] - 1][new_position[i][1]] == "G":
                start_y += 3
            start_coordinate.append([start_x, start_y])
            if past_position[i][0] != new_position[i][0] or \
               past_position[i][1] != new_position[i][1]:
                check_movement[i] = True
            if check_movement[i]:
                enemy[i]["direction"] = determine_moving_direction(past_position[i], new_position[i])
        for i in range(len(enemy)):
            enemy[i]["coordinates"] = start_coordinate[i]
        return check_movement, enemy

    mw_check_movement = [False] * len(mw_past_position)
    mr_check_movement = [False] * len(mr_past_position)
    sw_check_movement = [False] * len(sw_past_position)
    sr_check_movement = [False] * len(sr_past_position)

    # Mummy white
    mw_check_movement, mummy_white      = determine_coor_and_direction(mw_past_position, mw_new_position,
                                                                        mw_check_movement, mummy_white)
    # Mummy red
    mr_check_movement, mummy_red        = determine_coor_and_direction(mr_past_position, mr_new_position,
                                                                        mr_check_movement, mummy_red)
    # Scorpion white
    sw_check_movement, scorpion_white   = determine_coor_and_direction(sw_past_position, sw_new_position,
                                                                        sw_check_movement, scorpion_white)
    # Scorpion Red
    sr_check_movement, scorpion_red     = determine_coor_and_direction(sr_past_position, sr_new_position,
                                                                        sr_check_movement, scorpion_red)

    step_stride = game.cell_rect // 5

    for i in range(6):
        for j in range(len(mummy_white)):
            if i < 5:
                if mummy_white[j]["direction"] == "UP"      and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][1] -= step_stride
                if mummy_white[j]["direction"] == "DOWN"    and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][1] += step_stride
                if mummy_white[j]["direction"] == "LEFT"    and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][0] -= step_stride
                if mummy_white[j]["direction"] == "RIGHT"   and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][0] += step_stride
            if mw_check_movement[j]:
                mummy_white[j]["cellIndex"] = i % 5

        for j in range(len(mummy_red)):
            if i < 5:
                if mummy_red[j]["direction"] == "UP"        and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][1] -= step_stride
                if mummy_red[j]["direction"] == "DOWN"      and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][1] += step_stride
                if mummy_red[j]["direction"] == "LEFT"      and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][0] -= step_stride
                if mummy_red[j]["direction"] == "RIGHT"     and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][0] += step_stride
            if mr_check_movement[j]:
                mummy_red[j]["cellIndex"] = i % 5

        for j in range(len(scorpion_white)):
            if i < 5:
                if scorpion_white[j]["direction"] == "UP"   and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][1] -= step_stride
                if scorpion_white[j]["direction"] == "DOWN" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][1] += step_stride
                if scorpion_white[j]["direction"] == "LEFT" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][0] -= step_stride
                if scorpion_white[j]["direction"] == "RIGHT"and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][0] += step_stride
            if sw_check_movement[j]:
                scorpion_white[j]["cellIndex"] = i % 5

        for j in range(len(scorpion_red)):
            if i < 5:
                if scorpion_red[j]["direction"] == "UP"     and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][1] -= step_stride
                if scorpion_red[j]["direction"] == "DOWN"   and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][1] += step_stride
                if scorpion_red[j]["direction"] == "LEFT"   and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][0] -= step_stride
                if scorpion_red[j]["direction"] == "RIGHT"  and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][0] += step_stride
            if sr_check_movement[j]:
                scorpion_red[j]["cellIndex"] = i % 5

        draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    explorer,
                    mummy_white, mummy_red,
                    scorpion_white, scorpion_red)
        pygame.time.delay(100)
        pygame.display.update()