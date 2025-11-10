import pygame
import os

import main

class character_spritesheet:
    def __init__(self, image_spritesheet_path):
        # Một character sẽ có 20 frame chứa trong 4 hàng 5 cột
        self.sheet = pygame.image.load(image_spritesheet_path)
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
            self.stairs.append([x * self.cell_w, 0, self.cell_w, self.cell_h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.stairs[cellIndex])

def draw_screen(screen, input_maze, backdrop, floor, maze_size, cell_rect,
                stair, stair_position,
                mummy_white,
                wall,
                explorer):
    # Tọa độ bắt đầu của mê cung đồng bộ với trong file main
    coordinate_X    = 67
    coordinate_Y    = 80

    # Vẽ backdrop và floor đơn giản
    if True:
        # Phải vẽ backdrop trước rồi tới floor để floor đè lên phần đen trong backdrop
        screen.blit(backdrop, (0, 0))
        screen.blit(floor, (coordinate_X, coordinate_Y))

    # Vẽ Stair
    if True:
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

    # Vẽ Explorer
    if explorer["coordinates"]:
        # Các tham số truyền vào đọc hàm draw trong character_spritesheet để hiểu
        explorer["sprite_sheet"].draw(screen, explorer["coordinates"][0],
                                              explorer["coordinates"][1],
                                              explorer["cellIndex"],
                                              explorer["direction"])

    # Vẽ Mummy
    if mummy_white:
        # Tương tự Explorer
        mummy_white["sprite_sheet"].draw(screen, mummy_white["coordinates"][0],
                                                 mummy_white["coordinates"][1],
                                                 mummy_white["cellIndex"],
                                                 mummy_white["direction"])

    # Vẽ tường
    if True:
        # Horizontal Wall (Tường ngang)
        # Hàng chẵn chứa tường ngang
        # Tường nằm giữa 2 ô trống ngang nên ở cột lẻ
        for x in range(2, len(input_maze)-1, 2):
            for y in range(1, len(input_maze[x]), 2):
                if input_maze[x][y] == "%":
                    # Tính tọa độ tương tự hàm Cal_coordinate bên main
                    wall_x = coordinate_X + cell_rect * (y // 2)
                    wall_y = coordinate_Y + cell_rect * (x // 2)
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
                    # Đây chính là trường hợp tường hình chữ L
                    if (input_maze[x+1][y+1] == "%"):
                        wall.draw_right_wall(screen, wall_x, wall_y)
                        # redraw ở đây là vẽ lại phần ngang của chữ L cho nó không thừa
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