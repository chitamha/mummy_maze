import pygame
import os

import graphics

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
        self.maze_rect = 360
        self.screen_size_x = 494
        self.screen_size_y = 480
        self.coordinate_screen_x = 67
        self.coordinate_screen_y = 81
        self.get_input_maze(file_name)
        self.get_input_object(file_name)

        # Set hướng ban đầu cho nhân vật
        # Mặc định người chơi nửa trái bản đồ thì là Right và ngược lại
        if self.explorer_position[1] // 2 <= self.maze_size // 2:
            self.explorer_direction = "RIGHT"
        else:
            self.explorer_direction = "LEFT"
        # Set hướng ban đầu cho Mummy
        # Mặc định mummy ban đầu hướng xuống
        if self.mummy_white_position:
            self.mummy_white_direction = "DOWN"

    def get_input_maze(self, file_name):
        self.maze = []
        self.stair_position = ()
        with open(os.path.join(maze_path, file_name)) as file:
            for line in file:
                row = []
                for chr in line:
                    if chr != '\n': row.append(chr)
                self.maze.append(row)

        self.maze_size = len(self.maze) // 2
        self.cell_rect = self.maze_rect // self.maze_size

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 'S':
                    self.stair_position = (i, j)

    def get_input_object(self, file_name):
        with open(os.path.join(agents_path, file_name)) as file:
            for line in file:
                x = line.split()
                if x[0] == "E":
                    self.explorer_position = [int(x[1]), int(x[2])]
                if x[0] == "MW":
                    self.mummy_white_position = [int(x[1]), int(x[2])]

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
    backdrop_path = os.path.join(image_path, "backdrop.png")
    # Floor
    filename_floor = "floor" + str(size) + ".jpg"
    floor_path = os.path.join(image_path, filename_floor)
    # Wall
    filename_wall = "walls" + str(size) + ".png"
    wall_path = os.path.join(image_path, filename_wall)
    # Stair
    filename_stair = "stairs" + str(size) + ".png"
    stair_path = os.path.join(image_path, filename_stair)
    # Explorer
    filename_explorer = "explorer" + str(size) + ".png"
    explorer_path = os.path.join(image_path, filename_explorer)
    # Mummy_white
    filename_mummy_white = "mummy_white" + str(size) + ".png"
    mummy_white_path = os.path.join(image_path, filename_mummy_white)

    return backdrop_path, floor_path, wall_path, stair_path, explorer_path, mummy_white_path

def rungame(level):
    # Lấy trạng thái game
    game = GameState(level)

    # Load image path
    backdrop_path, floor_path, wall_path, stair_path, explorer_path, mummy_white_path  = load_image_path(game.maze_size)

    # Load image
    backdrop = pygame.image.load(backdrop_path)
    floor = pygame.image.load(floor_path)
    stair = graphics.stairs_spritesheet(stair_path)
    wall = graphics.wall_spritesheet(wall_path, game.maze_size)
    explorer_sheet = graphics.character_spritesheet(explorer_path)
    mummy_white_sheet = graphics.character_spritesheet(mummy_white_path)

    # Object
    explorer = {
        "sprite_sheet": explorer_sheet,
        "coordinates": Cal_coordinates(game, game.explorer_position[0], game.explorer_position[1]),
        "direction": game.explorer_direction,
        "cellIndex": 0
    }
    mummy_white = {
        "sprite_sheet": mummy_white_sheet,
        "coordinates": Cal_coordinates(game, game.mummy_white_position[0], game.mummy_white_position[1]),
        "direction": game.mummy_white_direction,
        "cellIndex": 0
    }

    # Set base
    pygame.init()
    pygame.display.set_caption("Mummy Maze")
    FPS = 60
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
    graphics.draw_screen(window, game.maze, backdrop, floor, game.maze_size, game.cell_rect, stair,
                         game.stair_position,
                         mummy_white,
                         wall,
                         explorer)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Điều kiện này làm cho các câu lệnh bên dưới chỉ chạy từ file gốc này
# Khi import file main cho các file khác if sẽ sai
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