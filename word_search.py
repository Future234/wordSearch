import pygame
import sys
import random
import string
import time
import threading
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

width = 600
height = 600

rows = 10
cols = 10

FPS = 60
game_paused = False

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Search Word")

font = pygame.font.SysFont("timesnewroman",25)
 
size = 500

# CONSTANT COLORS
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
GREY = (128,128,128)

colors = [BLUE,GREEN,BLACK]
letters = string.ascii_uppercase

class Spot:
    def __init__(self,row,col,size,text):
        self.row = row
        self.col = col
        self.color = WHITE
        self.size = size
        self.x = self.col * self.size
        self.y = self.row * self.size
        self.text = text
        self.current_text = " "
        self.txt = ' '
        
    def change_color(self,newColor):
        self.color = newColor

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.size,self.size))
        self.current_text = font.render(self.text,True,RED)
        self.txt = self.text
        text_rect = self.current_text.get_rect()
        text_rect.center = (self.x + (self.size // 2), self.y + (self.size // 2))
        win.blit(self.current_text,text_rect)
    
    def get_current_color(self):
        return self.color
    
    def get_current_text(self):
        return self.txt

class Button:
    def __init__(self,x,y,width,height,text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        text = font.render(self.text,True,BLUE)
        text_rect = text.get_rect()
        text_rect.center = (self.x + (self.width // 2),self.y + (self.height // 2))
        pygame.draw.rect(win,RED,self.rect)

        pos = pygame.mouse.get_pos()

        global letter_grid
        global game_paused
        global Grid

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:

                for i in range(len(words)):
                    list_of_digits.append([])
                    for j in range(len(words[i])):
                        list_of_digits[i].append(words[i][j])

                letter_grid = create_word_search(words,rows,cols)
                show_board(letter_grid)
                Grid = make_grid(letter_grid,rows,size)

                for i in list_of_dict:
                    print(i)
    
                for i in list_of_digits:
                    print(i)

                game_paused = True

        win.blit(text,text_rect)

def make_grid(letters,rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,letters[j][i])
            grid[i].append(spot)
    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,BLACK,(0,i * gap),(width,i * gap))
        for j in range(rows):
            pygame.draw.line(win,BLACK,(j * gap,0),(j * gap,width))

def draw(win,grid,rows,width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    
    for i in range(len(words)):
        text_surface = font.render(words[i],True,BLACK)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (i * (width / len(words)), 550)
        win.blit(text_surface,text_rect)

    pygame.display.update()

# Draw Screen That Get Input
def draw_input_screen(win,user_text,input_rect):
    playButton = Button(300,300,150,50,"Play")
    playButton.draw(win)
    pygame.draw.rect(win,RED,input_rect,2)
    text_surface = font.render(user_text,True,WHITE)
    win.blit(text_surface,(input_rect.x,input_rect.y))

def get_pos(pos,rows,width):
    x,y = pos
    gap = width // rows

    row = y // gap
    col = x // gap

    return row,col

list_of_dict = list()
word_dict = dict()
list_of_list_pos = list()

def place_word(board,word):
    global word_count
    placed = False
    while not placed:
        list_of_pos = list()
        orientation = random.randint(0,4)
        _orientation = "Vertical" if orientation == 0 else "Horizontal" if orientation == 1 else "Diagonal top-left to bottom right" if orientation == 2 else "Diagonal bottom-left to top-right"
        if orientation == 0: # Vertical
            row = random.randint(0,len(board) - 1)    
            col = random.randint(0,len(board) - len(word))
            
            space_available = all(board[row][c] == " " or
                                  board[row][c] == word[i]
                                  for i,c in enumerate(range(col,col + len(word))))
            if space_available:
                for i,c in enumerate(range(col,col + len(word))):
                    board[row][c] = word[i]
                    list_of_pos.append((c,row))

                word_dict = dict(wordN = word, typeofOrientation = _orientation)
                placed = True
                list_of_dict.append(word_dict)
                list_of_list_pos.append(list_of_pos)

        elif orientation == 1:  # Horizontal
            row = random.randint(0, len(board)-len(word))
            col = random.randint(0, len(board)-1)

            space_available = all(board[r][col] == " " or 
                board[r][col] == word[i] 
                  for i, r in enumerate(range(row, row+len(word))))
            
            if space_available:
                for i, r in enumerate(range(row, row+len(word))):
                    board[r][col] = word[i]
                    list_of_pos.append((col,r))



                word_dict = dict(wordN =  word, typeofOrientation = _orientation)
                placed = True
                list_of_dict.append(word_dict)
                list_of_list_pos.append(list_of_pos)

        elif orientation == 2:  # Diagonal top-left to bottom right
            row = random.randint(0, len(board)-len(word))
            col = random.randint(0, len(board)-len(word))

            space_available = all(board[r][c] == " " or 
                board[r][c] == word[i] 
                  for i, (r, c) in enumerate(zip(range(row, row+len(word)), 
                                      range(col, col+len(word)))))
            if space_available:
                for i, (r, c) in enumerate(zip(range(row, row+len(word)), 
                                      range(col, col+len(word)))):
                    board[r][c] = word[i]
                    list_of_pos.append((c,r))

                word_dict = dict(wordN =  word, typeofOrientation = _orientation)
                placed = True
                list_of_dict.append(word_dict)
                list_of_list_pos.append(list_of_pos)

        elif orientation == 3:  # Diagonal bottom-left to top-right
            row = random.randint(len(word) - 1, len(board) - 1)
            col = random.randint(0, len(board) - len(word))

            space_available = all(board[r][c] == " " or 
                board[r][c] == word[i] 
                  for i, (r, c) in enumerate(zip(range(row, row-len(word), -1),
                                     range(col, col+len(word)))))
            if space_available:
                for i, (r, c) in enumerate(zip(range(row, row-len(word), -1), 
                      range(col, col+len(word)))):
                    board[r][c] = word[i]
                    list_of_pos.append((c,r))

                word_dict = dict(wordN =  word, typeofOrientation = _orientation)
                placed = True
                list_of_dict.append(word_dict)
                list_of_list_pos.append(list_of_pos)

def fill_empty(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == " ":
                board[row][col] = random.choice(letters)


# Can be Deleted
def show_board(board):
    #print ("\n".join(map(lambda row: " ".join(row),letter_grid)))
    for row in range(len(board)):
        # print("|".join(row))
        for col in range(len(board[0])):
            print((board[col][row]),end='|')
        print('\n')

def generate_empty_board(rows,cols):
    #board = [[" " for _ in range(rows)] for _ in range(cols)]

    board = []
    for row in range(rows):
        board.append([])
        for col in range(cols):
            board[row].append(" ")

    return board
    
def create_word_search(words,rows,cols):
  
    board = generate_empty_board(rows,cols)

    for word in words:
        place_word(board,word)
  
    fill_empty(board)

    print(list_of_list_pos)

    return board

def get_words():
    words = []
    valid = True
    while valid:
        con = input("Enter Name: ")
        if con.lower() == "q":
            valid = False
            break
        words.append(con.upper())
    return words

checker = list()
current_checker_pos = list()
words = list()
list_of_digits = list()

def draw_horizontal_line(win,start_point,end_point):
    pygame.draw.line(win,RED,start_point,end_point)

def check_input(input):
    checking = False
    for i in range(len(list_of_digits)):
        checking = False
        if len(input) != len(list_of_digits[i]):
            continue

        for j in range(len(input)):
            
            if input[j] == list_of_digits[i][j]:
                if list_of_list_pos[i][j] == current_checker_pos[j]:
                    checking = True
                else:
                    checking = False
                    break
            else:
                checking = False
                break

        if checking == True:

            words.remove(words[i])
            list_of_digits.remove(list_of_digits[i])
            list_of_list_pos.remove(list_of_list_pos[i])
            input.clear()
            return checking

    input.clear()
    return checking    

def clear_selected_spot():
    for i in range(len(current_checker_pos)):
        row,col = current_checker_pos[i]
        spot = Grid[row][col]
        spot.change_color(WHITE)
        # spot.draw(win)

class Trie:
    def __init__(self,is_end=False):
        self.children = {}
        self.is_end = is_end
    
    def insert(self,s):
        node = self

        for ch in s:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True
    
    def build(self,words):

        for word in words:
            self.insert(word)
        return self
    
    def search(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node if node.is_end else None

    def delete(self, s):
        def rec(node, s, i):
            if i == len(s):
                node.is_end = False
                return len(node.children) == 0
            else:
                next_deletion = rec(node.children[s[i]], s, i+1)
                if next_deletion:
                    del node.children[s[i]]
                return next_deletion and not node.is_end and len(node.children) == 0
        if self.search(s):
            rec(self, s, 0)

def check(grid, trie, i, j, i_diff, j_diff, moves):
    single = []
    n, m = len(grid), len(grid[0])
    node = trie
    start_i, start_j = i, j
    substring = ''
    while 0 <= i < n and 0 <= j < m and grid[i][j] in node.children:
        substring += grid[i][j]
        node = node.children[grid[i][j]]
        single.append((j,i))
        if node.is_end:
            moves.append(single)
            trie.delete(substring)
            break
        i += i_diff
        j += j_diff

def solve(grid, words):
    moves = []
    trie = Trie().build(words)
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] in trie.children:
                for i_diff, j_diff in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    check(grid, trie, i, j, i_diff, j_diff, moves)
    return moves

def main():
    user_text = ''
    input_rect = pygame.Rect(200,200,200,32)
    run = True
    ai_moves = []
    counter = 0
    # words = get_words()

    def draw_ai_moves(ai_moves, colors):
        delay = 0.5 
        if len(ai_moves) == len(words):
            for i in range(len(words)):
                if len(ai_moves[i]) > 0:
                    for j in range(len(ai_moves[i])):
                        spot = Grid[ai_moves[i][j][0]][ai_moves[i][j][1]]
                        spot.change_color(colors[i])
                        spot.draw(win)
                        pygame.display.update()
                        clock.tick(FPS)
                        time.sleep(delay)
        else:
            print("No words found by the AI.")

    while run:
        if game_paused == False:
            win.fill(BLACK)
            draw_input_screen(win,user_text,input_rect)
        else:
            win.fill(WHITE)
            draw(win,Grid,rows,size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if event.key == pygame.K_RETURN and len(user_text) > 0:
                        words.append(user_text.upper())
                        user_text = ''
                        print(words)
                    else:
                        if len(user_text) <= rows and event.key != pygame.K_RETURN:
                            if len(words) < len(colors):
                                user_text += event.unicode

                if event.key == pygame.K_f:
                    ai_moves = solve(letter_grid,words)
                    print(ai_moves)
                    # draw ai moves
                    thread = threading.Thread(target=draw_ai_moves, args=(ai_moves, colors))
                    thread.start()

            if event.type == pygame.MOUSEBUTTONUP: # Left Mouse Button
                pos = pygame.mouse.get_pos()
                row,col = get_pos(pos,rows,size)
                # print(f'Row: {row} , Col: {col}')
                if row <= (rows - 1) and col <= (rows - 1):
                    spot = Grid[row][col]
                    spot.change_color(colors[counter])
                    checker.append(spot.get_current_text())
                    current_checker_pos.append(get_pos(pos,rows,size))
                    # print(spot.get_current_text())
                else:
                    print("Frankenstein")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(checker)
                    print(current_checker_pos)
                    # print(current_checker_pos)
                    isTrue = check_input(checker)
                    if isTrue:
                        counter += 1
                        current_checker_pos.clear()
                    else:
                        clear_selected_spot()
                        current_checker_pos.clear()

                    if counter == len(words):
                        pass
                        # pygame.quit()
                        # sys.exit()
                    print(isTrue)
                    
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

