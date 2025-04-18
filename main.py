import pygame
import sys
from pygame.locals import *
from grid import * 
from tkinter import Button
from healthbar import *

pygame.init()

SHOOT_SOUND = pygame.mixer.Sound('sounds/Melstroy_blyat.mp3')
SHOOT_SOUND.set_volume(0.2)


WIDTH, HEIGHT = 540, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Healthbar
health_bar = HealthBar(20, 560, 500, 25, 100)
# Colors
SHADOW_COLOR = (0, 0, 0, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Fonts
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Create a grid object
sudoku_grid = grid()

# Selected cell and grid size
selected = (0, 0)
grid_size = WIDTH // 9

# Game state
menu = 1  # Start with menu screen
wrong_attempts = 0  # Biến đếm số lần nhập sai

def draw_grid():
  for i in range(10):
    if i % 3 == 0:
      pygame.draw.line(screen, BLACK, (i * grid_size, 0), (i * grid_size, WIDTH), 4)
      pygame.draw.line(screen, BLACK, (0, i * grid_size), (WIDTH, i * grid_size), 4)
    else:
      pygame.draw.line(screen, GREY, (i * grid_size, 0), (i * grid_size, WIDTH), 2)
      pygame.draw.line(screen, GREY, (0, i * grid_size), (WIDTH, i * grid_size), 2)

def draw_numbers(player=False):
  for i in range(9):
    for j in range(9):
      if sudoku_grid.matrix[i][j] != 0 and not player:
        text = font.render(str(sudoku_grid.matrix[i][j]), True, BLACK)
        screen.blit(text, (j * grid_size + 20, i * grid_size + 10))
      elif player and sudoku_grid.user[i][j]:
        text = font.render(str(sudoku_grid.user[i][j]), True, BLACK)
        screen.blit(text, (j * grid_size + 20, i * grid_size + 10))

def draw_selected():
    if selected:
        row, col = selected
        pygame.draw.rect(screen, BLUE, (col * grid_size, row * grid_size, grid_size, grid_size), 4)

def handle_click(pos):
    global selected
    x, y = pos
    if x < WIDTH and y < WIDTH:
        selected = (y // grid_size, x // grid_size)

def handle_input(key, player=False):
    global selected, health_bar, wrong_attempts, menu
    if selected:
        row, col = selected
        if player:
          if key in range(K_1, K_9 + 1):
            user_input = key - K_0
            sudoku_grid.user[row][col] = user_input
            
            if user_input != sudoku_grid.matrix[row][col]:
              # Giảm máu và tăng đếm số lần sai
              health_bar.update(20)  # Trừ 20 điểm máu mỗi khi nhập sai
              wrong_attempts += 1
              SHOOT_SOUND.play()

              # Kiểm tra nếu sai 5 lần hoặc thanh máu hết
              if wrong_attempts >= 5 or health_bar.hp <= 0:
                  menu = 4  # Chuyển sang màn hình Game Over
            else:
              # Nếu nhập đúng, hiển thị số nhập đúng bằng màu đen
              num_text = font.render(str(user_input), True, BLACK)
              screen.blit(num_text, (col * grid_size + 10, row * grid_size + 10))
              if sudoku_grid.matrix == sudoku_grid.user: menu = 5
            pygame.display.flip()
          elif key == K_DELETE or key == K_BACKSPACE:
            sudoku_grid.user[row][col] = 0
        elif not player:
          if key in range(K_1, K_9 + 1):
            user_input = key - K_0
            sudoku_grid.matrix[row][col] = user_input
            num_text = font.render(str(user_input), True, BLACK)
            screen.blit(num_text, (col * grid_size + 10, row * grid_size + 10))
            pygame.display.flip()
          elif key == K_DELETE or key == K_BACKSPACE:
            sudoku_grid.matrix[row][col] = 0


def generate_valid_sudoku():
    global health_bar, wrong_attempts
    sudoku_grid.reset_board()
    sudoku_grid.fillValues()
    health_bar.hp = 100  # Reset lại máu về 100 khi bắt đầu trò chơi mới
    wrong_attempts = 0  # Reset số lần nhập sai


# Font setup
small_font = pygame.font.Font(None, 36)  # Adjust font size as needed

def draw_button(text, x, y, width, height, color, shadow=True):
    if shadow:
        shadow_rect = pygame.Rect(x + 4, y + 4, width, height)
        pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=12)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=12)
    text_surface = small_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def draw_start_button():
  return draw_button("START", WIDTH - 150, HEIGHT - 50, 140, 40, GREEN)

def draw_clear_button():
  return draw_button("CLEAR", 10, HEIGHT - 50, 140, 40, GREEN)

def draw_back_button():
  return draw_button("BACK", 200, HEIGHT - 50, 140, 40, GREEN)

def draw_solve_button():
  return draw_button("SOLVE", WIDTH - 150, HEIGHT - 50, 140, 40, GREEN)

def draw_menu():
  screen.fill(WHITE)
  title = font.render("Sudoku Menu", True, BLACK)
  screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))
  play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
  pygame.draw.rect(screen, BLUE, play_button)
  play_text = small_font.render("Play Sudoku", True, WHITE)
  screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - 40))
  solver_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
  pygame.draw.rect(screen, GREEN, solver_button)
  generate_text = small_font.render("Sudoku Solver", True, WHITE)
  screen.blit(generate_text, (WIDTH // 2 - generate_text.get_width() // 2, HEIGHT // 2 + 60))
  return solver_button, play_button
####
def draw_game_over():
  screen.fill(WHITE)
  title = font.render("GAME OVER!", True, RED)
  screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

  reset_button = draw_button("AGAIN", WIDTH // 2 - 70, HEIGHT // 2, 140, 50, GREEN)
  return reset_button

def draw_victory():
  screen.fill(WHITE)
  title = font.render("CONGRATULATIONS!", True, RED)
  screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

  victory = draw_button("AGAIN", WIDTH // 2 - 70, HEIGHT // 2, 140, 50, GREEN)
  return victory

def main():
  global selected, menu, wrong_attempts, health_bar
  running = True
  health_bar.hp = 100
  wrong_attempts = 0

  while running:
    
    if menu == 1:
      solver_button, play_button = draw_menu()
      sudoku_grid.reset_board()

    elif menu == 2:
      screen.fill(WHITE)
      draw_grid()
      draw_numbers()
      draw_selected()
      clear_button = draw_clear_button()
      back_button = draw_back_button()
      solve_button = draw_solve_button()

    elif menu == 3:
      screen.fill(WHITE)
      draw_grid()
      draw_numbers(player=True)
      draw_selected()
      health_bar.draw(screen)
      clear_button = draw_clear_button()
      back_button = draw_back_button()
      start_button = draw_start_button()

      # Vẽ lại thanh máu trong mỗi vòng lặp để cập nhật chính xác
      health_bar.draw(screen)
      

    elif menu == 4:
      reset_button = draw_game_over()
    
    else:
      victory_button = draw_victory()

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

      if menu == 1:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          if solver_button.collidepoint(event.pos):
            menu = 2
          elif play_button.collidepoint(event.pos):
            menu = 3
            generate_valid_sudoku()  # Bắt đầu trò chơi mới và reset lại máu
      elif menu == 3:
        if event.type == MOUSEBUTTONDOWN:
          if clear_button.collidepoint(event.pos):
              sudoku_grid.reset_board()
          elif start_button.collidepoint(event.pos):
              generate_valid_sudoku()  # Reset lại máu khi nhấn "START"
          elif back_button.collidepoint(event.pos):
              menu = 1
          else:
              handle_click(event.pos)
        if event.type == KEYDOWN:
            handle_input(event.key, player=True)
      elif menu == 2:
        if event.type == MOUSEBUTTONDOWN:
            if clear_button.collidepoint(event.pos):
                sudoku_grid.reset_board()
            elif solve_button.collidepoint(event.pos):
              sudoku_grid.solve_sudoku()
            elif back_button.collidepoint(event.pos):
                menu = 1
            else:
                handle_click(event.pos)
        if event.type == KEYDOWN:
            handle_input(event.key, player=False)
      elif menu == 4:  # Màn hình Game Over
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          if reset_button.collidepoint(event.pos):
            generate_valid_sudoku()  # Bắt đầu lại trò chơi mới
            menu = 3  # Quay trở lại màn hình chơi
      else:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          if victory_button.collidepoint(event.pos):
            generate_valid_sudoku()  # Bắt đầu lại trò chơi mới
            menu = 3  # Quay trở lại màn hình chơi

    pygame.display.update()

if __name__ == "__main__":
  main()
