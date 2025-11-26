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
        self.maze_rect = 360
        self.screen_size_x = 494
        self.screen_size_y = 480
        self.coordinate_screen_x = 67
        self.coordinate_screen_y = 8000
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
        # Lấy dữ liệu mê cung ASCII lưu vào maze
        self.maze = []
        with open(os.path.join(maze_path, file_name)) as file:
            for line in file:
                row = []
                for chr in line:
                    if chr != '\n': row.append(chr)
                self.maze.append(row)

        # Mê cung ASCII vừa biểu diễn đường đi vừa biểu diễn tường nên size nó gấp đôi
        self.maze_size = len(self.maze) // 2
        self.cell_rect = self.maze_rect // self.maze_size

        # Tìm vị trí Stair trong mê cung
        self.stair_position = ()
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 'S':
                    self.stair_position = (i, j)

    def get_input_object(self, file_name):
        # Tìm position ban đầu của người chơi và mummy
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

def check_explorer_is_killed(explorer_character, mummy_white_character):
    if mummy_white_character:
        if explorer_character.get_x() == mummy_white_character.get_x() and explorer_character.get_y() == mummy_white_character.get_y():
            return True
    return False

def update_enemy_position(window, game,
                          backdrop, floor, stair, wall,
                          explorer, explorer_character,
                          mummy_white_character, mummy_white):
    # Gọi hàm kiểm tra xem mummy có trùng vị trí với người chơi không
    if check_explorer_is_killed(explorer_character, mummy_white_character):
        return False
    # -------------------------------MUMMY WHITE FIRST MOVE-------------------------------
    mw_move = True
    if mw_move:
        # Vị trí cũ của mummy
        mw_past_position = [mummy_white_character.get_x(), mummy_white_character.get_y()]
        # Cho mummy di chuyển
        mummy_white_character = mummy_white_character.white_move(game.maze, explorer_character)
        # Cập nhật lại vị trí mummy
        mw_new_position = [mummy_white_character.get_x(), mummy_white_character.get_y()]

    # Vẽ quái vật
    draw = True
    if draw:
        graphics.enemy_move_animation(mw_past_position, mw_new_position,
                                      window, game,
                                      backdrop, floor, stair, game.stair_position, wall,
                                      explorer, mummy_white)

    # Check lại sau bước 1 đã thua chưa
    if check_explorer_is_killed(explorer_character, mummy_white_character):
        return False

    # -------------------------------MUMMY WHITE SECOND MOVE-------------------------------
    mw_move = True
    if mw_move:
        # Vị trí cũ của mummy
        mw_past_position = [mummy_white_character.get_x(), mummy_white_character.get_y()]
        # Cho mummy di chuyển
        mummy_white_character = mummy_white_character.white_move(game.maze, explorer_character)
        # Cập nhật lại vị trí mummy
        mw_new_position = [mummy_white_character.get_x(), mummy_white_character.get_y()]

    # Vẽ quái vật
    draw = True
    if draw:
        graphics.enemy_move_animation(mw_past_position, mw_new_position,
                                      window, game,
                                      backdrop, floor, stair, game.stair_position, wall,
                                      explorer, mummy_white)

    # Check lại sau bước 1 đã thua chưa
    if check_explorer_is_killed(explorer_character, mummy_white_character):
        return False

    # Check điều kiện thắng
    # Theo thứ tự 4 dòng bên dưới:
    # 1. Cửa ra nằm bên trên
    # 2. Cửa ra nằm bên dưới
    # 3. Cửa ra nằm bên trái
    # 4. Cửa ra nằm bn phải
    if game.maze[explorer_character.get_x() - 1][explorer_character.get_y()] == "S" or \
            game.maze[explorer_character.get_x() + 1][explorer_character.get_y()] == "S" or \
            game.maze[explorer_character.get_x()][explorer_character.get_y() - 1] == "S" or \
            game.maze[explorer_character.get_x()][explorer_character.get_y() + 1] == "S":
        print("YOU WIN!")
        return False
    return True

def rungame(level):
    # Lấy trạng thái game
    game = GameState(level)

    # Load image path
    backdrop_path, floor_path, wall_path, stair_path, explorer_path, mummy_white_path  = load_image_path(game.maze_size)

    # Load image
    Load_image = True
    if Load_image:
        backdrop = pygame.image.load(backdrop_path)
        floor = pygame.image.load(floor_path)
        stair = graphics.stairs_spritesheet(stair_path)
        wall = graphics.wall_spritesheet(wall_path, game.maze_size)
        explorer_sheet = graphics.character_spritesheet(explorer_path)
        mummy_white_sheet = graphics.character_spritesheet(mummy_white_path)

    # Objects
    # Mỗi object sẽ là một dict tương tự như struct bên C++ chứa 4 thứ
    # 1. sprite_sheet: Một hình ảnh chứa các ô frame trạng thái của object
    # 2. coordinates: Tọa độ hiện tại của object
    # 3. direction: Hướng quay của object (UP, DOWN, RIGHT, LEFT)
    # 4. cellIndex: Vị trí ô frame cần vẽ trong sprite_sheet
    initialize_objects = True
    if initialize_objects:
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
                             stair, game.stair_position, wall,
                             explorer, mummy_white)
        # Ở trên nó chỉ đẩy lên ô nhớ update để vẽ ra
        pygame.display.update()

    # Tạo biến explorer_charater là một class Explorer bên file characters.py
    # mummy_white_character tương tự
    explorer_character = characters.Explorer(game.explorer_position[0], game.explorer_position[1])
    mummy_white_character = characters.mummy_white(game.mummy_white_position[0], game.mummy_white_position[1])

    running = True
    # HÀNG ĐỢI LỆNH DI CHUYỂN
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
                direction = None

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
                if event.key == pygame.K_SPACE:
                    direction = None  # không làm gì

                # Nếu có hướng và vị trí mới khác vị trí cũ
                if direction is not None and (explorer_new_x != explorer_x or explorer_new_y != explorer_y):
                    # Kiểm tra có đi hợp lệ không
                    if explorer_character.eligible_character_move(game.maze, explorer_x, explorer_y,
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

                if is_neighbor and explorer_character.eligible_character_move(game.maze, explorer_x, explorer_y,
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
                        direction = None

                    if direction is not None:
                        # Thêm lệnh vào hàng đợi
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

            if is_neighbor and explorer_character.eligible_character_move(game.maze, explorer_x, explorer_y,
                                                                          target_x, target_y):
                # Set hướng
                explorer["direction"] = direction

                # Bắt đầu animation → khóa input
                is_moving = True

                explorer_character.move(target_x, target_y, window, game,
                                        backdrop, floor, stair, game.stair_position, wall,
                                        explorer, mummy_white)

                # Sau khi người chơi đi xong thì cho quái di chuyển
                running = update_enemy_position(window, game,
                                                backdrop, floor, stair, wall,
                                                explorer, explorer_character,
                                                mummy_white_character, mummy_white)

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