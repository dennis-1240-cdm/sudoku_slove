import math, random

class grid:
    def __init__(self) -> None:
        self.matrix = [[0 for x in range(9)] for y in range(9)]
        self.user = [[0 for x in range(9)] for y in range(9)]
        self.K = 50

    def reset_board(self):
        self.matrix = [[0 for x in range(9)] for y in range(9)]
        self.user = [[0 for x in range(9)] for y in range(9)]

    def show(self):
        for i in self.matrix:
            print(*i, end="\n")

    def show_user(self):
        for i in self.user:
            print(*i, end="\n")

    def find_empty_location(self, l):
        for row in range(9):
            for col in range(9):
                if self.matrix[row][col] == 0:
                    l[0] = row
                    l[1] = col
                    return True
        return False

    def used_in_row(self, row, num):
        for i in range(9):
            if self.matrix[row][i] == num:
                return True
        return False

    def used_in_col(self, col, num):
        for i in range(9):
            if self.matrix[i][col] == num:
                return True
        return False

    def used_in_box(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if self.matrix[i + row][j + col] == num:
                    return True
        return False

    def check_location_is_safe(self, row, col, num):
        is_safe = (not self.used_in_row(row, num) and
                    not self.used_in_col(col, num) and
                    not self.used_in_box(row - row % 3, col - col % 3, num))
        return is_safe

    def fillValues(self):
        self.fillDiagonal()
        self.fillRemaining(0, int(9**(1/2)))
        

        # Xóa các ô để tạo Sudoku
        self.removeKDigits()

    def fillDiagonal(self):
      for i in range(0, 9, int(9**(1/2))):
          self.fillBox(i, i)

    def fillRemaining(self, i, j):
      if i == 9 - 1 and j == 9:
          return True

      if j == 9:
          i += 1
          j = 0

      if self.matrix[i][j] != 0:
          return self.fillRemaining(i, j + 1)

      for num in range(1, 10):
          if self.check_location_is_safe(i, j, num):
              self.matrix[i][j] = num
              if self.fillRemaining(i, j + 1):
                  return True
              self.matrix[i][j] = 0
      return False


    def fillBox(self, row, col):
      num = 0
      for i in range(int(9**(1/2))):
          for j in range(int(9**(1/2))):
              while True:
                  num = self.randomGenerator(9)
                  if not self.used_in_box(row, col, num):
                      break
              self.matrix[row + i][col + j] = num

    def removeKDigits(self):
        count = self.K

        while (count != 0):
            i = self.randomGenerator(9) - 1
            j = self.randomGenerator(9) - 1
            if (self.matrix[i][j] != 0):
                count -= 1
                self.user[i][j] = self.matrix[i][j]  # Bản sao để người chơi điền
                self.matrix[i][j] = 0

    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)

    def solve_sudoku(self):
      l = [0, 0]
      if not self.find_empty_location(l):
          print("Sudoku solved successfully!")
          return True

      row = l[0]
      col = l[1]

      for num in range(1, 10):
        #   print(f"Trying {num} at ({row}, {col})")
          if self.check_location_is_safe(row, col, num):
              self.matrix[row][col] = num
            #   print(f"Placed {num} at ({row}, {col})")
              if self.solve_sudoku():
                  return True
            #   print(f"Backtracking from {num} at ({row}, {col})")
              self.matrix[row][col] = 0

      return False
