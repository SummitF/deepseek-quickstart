import pygame
import sys

# 初始化pygame
pygame.init()

# 游戏常量
BOARD_SIZE = 15  # 15x15的棋盘
GRID_SIZE = 40   # 每个格子的像素大小
PIECE_RADIUS = 18  # 棋子半径
MARGIN = 30      # 棋盘边距
WIDTH = BOARD_SIZE * GRID_SIZE + 2 * MARGIN  # 窗口宽度
HEIGHT = BOARD_SIZE * GRID_SIZE + 2 * MARGIN + 50  # 窗口高度
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (220, 179, 92)  # 棋盘颜色(木质)
LINE_COLOR = (0, 0, 0)        # 棋盘线颜色
BLACK_PIECE = (45, 45, 45)    # 黑棋颜色
WHITE_PIECE = (230, 230, 230) # 白棋颜色
HIGHLIGHT = (255, 0, 0)       # 高亮颜色(获胜连线)

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("五子棋")

# 游戏状态
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # 棋盘状态
current_player = "black"  # 当前玩家(黑棋先行)
game_over = False         # 游戏是否结束
winner = None             # 获胜方
win_line = []             # 获胜连线坐标

# 绘制棋盘
def draw_board():
    # 填充棋盘背景色
    screen.fill(BOARD_COLOR)
    
    # 绘制棋盘网格线
    for i in range(BOARD_SIZE):
        # 横线
        pygame.draw.line(screen, LINE_COLOR, 
                         (MARGIN, MARGIN + i * GRID_SIZE), 
                         (WIDTH - MARGIN, MARGIN + i * GRID_SIZE), 2)
        # 竖线
        pygame.draw.line(screen, LINE_COLOR, 
                         (MARGIN + i * GRID_SIZE, MARGIN), 
                         (MARGIN + i * GRID_SIZE, HEIGHT - MARGIN - 50), 2)
    
    # 绘制坐标标记
    font = pygame.font.SysFont('Arial', 16)
    for i in range(BOARD_SIZE):
        # 横坐标(A-O)
        text = font.render(chr(65 + i), True, BLACK)
        screen.blit(text, (MARGIN + i * GRID_SIZE - 5, HEIGHT - 40))
        # 纵坐标(1-15)
        text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, (10, MARGIN + i * GRID_SIZE - 10))
    
    # 绘制当前玩家提示
    status_text = f"当前: {'黑棋' if current_player == 'black' else '白棋'}"
    if game_over:
        status_text = f"{'黑棋' if winner == 'black' else '白棋'}获胜!"
    text = pygame.font.SysFont('Arial', 24).render(status_text, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 30))

# 绘制棋子
def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == "black":
                pygame.draw.circle(screen, BLACK_PIECE, 
                                  (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE), 
                                  PIECE_RADIUS)
            elif board[row][col] == "white":
                pygame.draw.circle(screen, WHITE_PIECE, 
                                  (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE), 
                                  PIECE_RADIUS)
    
    # 绘制获胜连线
    if win_line:
        start_pos = (MARGIN + win_line[0][1] * GRID_SIZE, MARGIN + win_line[0][0] * GRID_SIZE)
        end_pos = (MARGIN + win_line[-1][1] * GRID_SIZE, MARGIN + win_line[-1][0] * GRID_SIZE)
        pygame.draw.line(screen, HIGHLIGHT, start_pos, end_pos, 4)

# 落子
def place_piece(row, col):
    global current_player, game_over, winner, win_line
    
    # 检查位置是否有效
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE or board[row][col] is not None:
        return False
    
    # 放置棋子
    board[row][col] = current_player
    
    # 检查是否获胜
    if check_win(row, col):
        game_over = True
        winner = current_player
    else:
        # 切换玩家
        current_player = "white" if current_player == "black" else "black"
    
    return True

# 检查是否五子连珠
def check_win(row, col):
    directions = [
        [(0, 1), (0, -1)],   # 水平方向
        [(1, 0), (-1, 0)],    # 垂直方向
        [(1, 1), (-1, -1)],   # 主对角线
        [(1, -1), (-1, 1)]    # 副对角线
    ]
    
    for direction_pair in directions:
        count = 1  # 当前棋子已算1个
        line = [(row, col)]  # 记录连线
        
        for dx, dy in direction_pair:
            x, y = row + dx, col + dy
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == current_player:
                count += 1
                line.append((x, y))
                x += dx
                y += dy
        
        if count >= 5:
            # 找到5个或更多连线
            # 只保留5个连续的棋子坐标用于高亮显示
            if len(line) > 5:
                line = line[:5] if direction_pair[0][0] >= 0 or direction_pair[0][1] >= 0 else line[-5:]
            win_line.extend(line)
            return True
    
    return False

# 重置游戏
def reset_game():
    global board, current_player, game_over, winner, win_line
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "black"
    game_over = False
    winner = None
    win_line = []

# 主游戏循环
def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # 获取鼠标位置并转换为棋盘坐标
                x, y = pygame.mouse.get_pos()
                col = round((x - MARGIN) / GRID_SIZE)
                row = round((y - MARGIN) / GRID_SIZE)
                
                # 尝试落子
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    place_piece(row, col)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 按R键重置游戏
                    reset_game()
        
        # 绘制游戏
        draw_board()
        draw_pieces()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()