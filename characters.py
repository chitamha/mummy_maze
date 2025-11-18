import pygame

import graphics

class character():
    def  __init__(self, x, y):
        self.x = x
        self.y = y

    def check_same_position(self, character):
        return (character.x == self.x) and (character.y == self.y)

    def eligible_character_move(self, maze, x, y, new_x, new_y):
        # Vượt ra ngoài mê cung thì False
        if new_x < 1 or new_x > len(maze) or new_y < 1 or new_y > len(maze):
            return False
        # Check xem các trường hợp đi có đụng tường không
        # Move Down
        if new_x == x + 2:
            if maze[x+1][y] == "%":
                return False
        # Move Up
        if new_x == x - 2:
            if maze[x-1][y] == "%":
                return False
        # Move Right
        if new_y == y + 2:
            if maze[x][y+1] == "%":
                return False
        # Move Left
        if new_y == y - 2:
            if maze[x][y-1] == "%":
                return False
        return True

    def move_animation(self, x, y, screen, game,
                       backdrop, floor, stair, stair_position, wall,
                       explorer, mummy_white):
        raise NotImplementedError("This is base class method")

    def move(self, new_x, new_y, screen, game,
             backdrop, floor, stair, stair_position,wall,
             explorer, mummy_white):
        self.move_animation(new_x, new_y, screen, game,
                            backdrop, floor, stair, stair_position, wall,
                            explorer, mummy_white)
        self.x = new_x
        self.y = new_y

    def move_xy(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

class Explorer(character):
    def move_animation(self, x, y, screen, game,
                       backdrop, floor, stair, stair_position, wall,
                       explorer, mummy_white):
        # Tính toán tọa độ pixel của nhân vật
        explorer_start_x = game.coordinate_screen_x + game.cell_rect * (self.y // 2)
        explorer_start_y = game.coordinate_screen_y + game.cell_rect * (self.x // 2)
        # Nếu bên trên là tường dịch nhân vật xuống 3 pixel để đầu không đụng tường
        if x > 0 and game.maze[x - 1][y] == "%":
            explorer_start_y += 3
        explorer["coordinates"] = [explorer_start_x, explorer_start_y]
        # Tính toán khoảng cách pixel của mỗi bước đi
        step_stride = game.cell_rect // 5
        coordinates = list(explorer["coordinates"])
        for i in range(6):
            # 5 Bước đầu là di chuyển
            # Bước thứ 6 là đến nơi
            if i < 5:
                if explorer["direction"] == "UP":
                    coordinates[1] -= step_stride
                if explorer["direction"] == "DOWN":
                    coordinates[1] += step_stride
                if explorer["direction"] == "LEFT":
                    coordinates[0] -= step_stride
                if explorer["direction"] == "RIGHT":
                    coordinates[0] += step_stride
            explorer["coordinates"] = list(coordinates)
            explorer["cellIndex"] = i % 5
            graphics.draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                                 stair, stair_position, wall,
                                 explorer, mummy_white)
            pygame.time.delay(100)
            pygame.display.update()

class enemy(character):
    def __init__(self, x, y):
        self.attempt = 0
        self.step_count = 0
        super().__init__(x, y)

    def move_Vertical(self, maze, explorer):
        # Nếu đã đi đủ 2 bước thì ngưng
        if self.step_count == 2:
            return self
        new_x = self.get_x() + 2 * sign(explorer.get_x() - self.get_x())
        new_y = self.get_y()
        if self.eligible_character_move(maze, self.get_x(), self.get_y(), new_x, new_y):
            self.move_xy(new_x, new_y)
            self.step_count += 1
            if self.step_count == 2:
                return self
        else:
            self.attempt += 1
        return self

    def move_Horizontal(self, maze, explorer):
        # Nếu đã đi đủ 2 bước thì ngưng
        if self.step_count == 2:
            return self
        new_x = self.get_x()
        new_y = self.get_y() + 2 * sign(explorer.get_y() - self.get_y())
        if self.eligible_character_move(maze, self.get_x(), self.get_y(), new_x, new_y):
            self.move_xy(new_x, new_y)
            self.step_count += 1
            if self.step_count == 2:
                return self
        else:
            self.attempt += 1
        return self

    def set_attempt(self, attempt):
        self.attempt = attempt
    def get_attempt(self):
        return self.attempt
    def set_step_count(self, step_count):
        self.step_count = step_count
    def get_step_count(self):
        return self.step_count

class mummy_white(enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

    def white_move(self, maze, explorer):
        # Nếu vị trí mummy trùng với explorer thì kết thúc luôn
        if self.check_same_position(explorer):
            return self
        else:
            # step_count: Số bước thử thành công
            # attempt: Số lần thử
            self.set_step_count(0)
            self.set_attempt(0)
            # Giới hạn số lần thử là 5 để tránh lặp vô tận
            while self.get_attempt() < 5 and self.get_step_count() < 1:
                # Ưu tiên đuổi theo hàng ngang
                while self.get_y() != explorer.get_y():
                    self = self.move_Horizontal(maze, explorer)
                    if self.get_step_count() >= 1:
                        return self
                    if self.get_attempt() > 4:
                        break
                if self.check_same_position(explorer):
                    return self
                # Sau đó đi ngang không được mới đuổi theo hàng dọc
                self = self.move_Vertical(maze, explorer)
                if (self.check_same_position(explorer) or self.get_step_count() >= 1):
                    return self
            return self

def sign(x):
    if x == 0:
        return 0
    else:
        return x // abs(x)