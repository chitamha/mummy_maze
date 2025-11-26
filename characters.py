import pygame
import graphics
import collections


def sign(x):
    if x == 0:
        return 0
    else:
        return int(x // abs(x))

class character():
    def __init__(self, x, y):
        self.x = x # Vị trí hàng (Row)
        self.y = y # Vị trí cột (Column)

    def check_same_position(self, character):
        return (character.x == self.x) and (character.y == self.y)

    def eligible_character_move(self, maze, x, y, new_x, new_y):
        
        # 1. Vượt ra ngoài mê cung (Len(maze) là số hàng, Len(maze[0]) là số cột)
        # Tọa độ ASCII là số lẻ (1, 3, 5, ...), tối đa là len(maze)-2
        if new_x < 1 or new_x >= len(maze) - 1 or new_y < 1 or new_y >= len(maze[0]) - 1:
            return False
            
        # 2. Kiểm tra có đụng tường không (Tường nằm ở ô giữa)
        
        # Đi XUỐNG (Tăng x)
        if new_x == x + 2 and maze[x+1][y] == "%":
            return False
        # Đi LÊN (Giảm x)
        if new_x == x - 2 and maze[x-1][y] == "%":
            return False
        # Đi PHẢI (Tăng y)
        if new_y == y + 2 and maze[x][y+1] == "%":
            return False
        # Đi TRÁI (Giảm y)
        if new_y == y - 2 and maze[x][y-1] == "%":
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
        
        # Thêm logic căn chỉnh 3px từ Cal_coordinates
        if x > 0 and game.maze[x - 1][y] == "%":
            explorer_start_y += 3
            
        explorer["coordinates"] = [explorer_start_x, explorer_start_y]
        
        # Tính toán khoảng cách pixel của mỗi bước đi
        step_stride = game.cell_rect // 5
        coordinates = list(explorer["coordinates"])
        
        # Animation chạy 6 frame
        for i in range(6):
            # 5 Bước đầu là di chuyển
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
            pygame.time.delay(100) # Giảm delay để animation mượt hơn
            pygame.display.update()


class enemy(character):
    def __init__(self, x, y):
        super().__init__(x, y)

    # --- Phương thức Di chuyển Tham lam (Thực hiện và Cập nhật 1 bước) ---
    def move_Vertical(self, maze, explorer):
        new_x = self.get_x() + 2 * sign(explorer.get_x() - self.get_x())
        new_y = self.get_y()
        
        if self.eligible_character_move(maze, self.get_x(), self.get_y(), new_x, new_y):
            self.move_xy(new_x, new_y)
            return True # Di chuyển thành công
        else:
            return False # Không di chuyển được

    def move_Horizontal(self, maze, explorer):
        new_x = self.get_x()
        new_y = self.get_y() + 2 * sign(explorer.get_y() - self.get_y())
        
        if self.eligible_character_move(maze, self.get_x(), self.get_y(), new_x, new_y):
            self.move_xy(new_x, new_y)
            return True # Di chuyển thành công
        else:
            return False # Không di chuyển được
    
    # --- BFS (Giữ nguyên) ---
    def bfs_shortest_path(self, maze, target_x, target_y):
        start_x, start_y = self.x, self.y 
        
        queue = collections.deque([(start_x, start_y, [])]) 
        visited = set([(start_x, start_y)])
        
        # Các hướng đi có thể (bước 2 ô)
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)] 
        
        while queue:
            current_x, current_y, path = queue.popleft()
            
            if current_x == target_x and current_y == target_y:
                return path[0] if path else None 
            
            for dx, dy in directions:
                new_x = current_x + dx
                new_y = current_y + dy
                
                if self.eligible_character_move(maze, current_x, current_y, new_x, new_y):
                    if (new_x, new_y) not in visited:
                        visited.add((new_x, new_y))
                        new_path = path + [(new_x, new_y)]
                        queue.append((new_x, new_y, new_path))
                        
        return None 

class mummy_white(enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.current_strategy = "BFS" 

    def set_move_strategy(self, strategy_name):
        self.current_strategy = strategy_name.upper()
    
    # Hàm này tính toán VÀ thực hiện CHỈ 1 bước di chuyển
    def white_move(self, maze, explorer):
        if self.check_same_position(explorer):
            return self
        
        target_x, target_y = explorer.get_x(), explorer.get_y()
        next_step = None # (x, y) của bước tiếp theo

        if self.current_strategy == "BFS":
            next_step = self.bfs_shortest_path(maze, target_x, target_y)
            
            # Cập nhật vị trí sau BFS
            if next_step is not None:
                next_x, next_y = next_step
                self.move_xy(next_x, next_y)
        
        elif self.current_strategy == "GREEDY":
            
            moved = False
            
            # 1. Thử đi Ngang (Horizontal)
            if self.get_y() != explorer.get_y():
                # Hàm move_Horizontal tự cập nhật vị trí nếu đi thành công
                if self.move_Horizontal(maze, explorer):
                    moved = True
            
            # 2. Nếu chưa đi được, thử đi Dọc (Vertical)
            if not moved and self.get_x() != explorer.get_x():
                self.move_Vertical(maze, explorer)
                
        return self