import os
import sys
import cfg
import pygame
import random
import pickle

def isgameover(board, size):
    ncells = size * size
    for i in range(ncells - 1):
        if board[i] != i:
            return False
    return True

def moveL(board, bci, ncols):
    if bci % ncols == ncols - 1:  # If blank cell is at the rightmost column, can't move left
        return bci
    board[bci + 1], board[bci] = board[bci], board[bci + 1]
    play_move_sound()
    return bci + 1

def moveR(board, bci, ncols):
    if bci % ncols == 0:  # If blank cell is at the leftmost column, can't move right
        return bci
    board[bci - 1], board[bci] = board[bci], board[bci - 1]
    play_move_sound()
    return bci - 1

def moveD(board, bci, ncols):
    if bci < ncols:  # If blank cell is in the topmost row, can't move down
        return bci
    board[bci - ncols], board[bci] = board[bci], board[bci - ncols]
    play_move_sound()
    return bci - ncols

def moveU(board, bci, nrows, ncols):
    if bci >= ncols * (nrows - 1):  # If blank cell is in the bottommost row, can't move up
        return bci
    board[bci + ncols], board[bci] = board[bci], board[bci + ncols]
    play_move_sound()
    return bci + ncols

def creatboard(nrows, ncols, ncells):
    board = list(range(ncells))
    bci = ncells - 1

    for _ in range(cfg.RANDOM):
        direction = random.randint(0, 3)
        if direction == 0:
            bci = moveL(board, bci, ncols)
        elif direction == 1:
            bci = moveR(board, bci, ncols)
        elif direction == 2:
            bci = moveU(board, bci, nrows, ncols)
        elif direction == 3:
            bci = moveD(board, bci, ncols)
    return board, bci

def Getimagepaths(rootdir):
    imagenames = os.listdir(rootdir)
    return os.path.join(rootdir, random.choice(imagenames))

def save_game(board, bci):
    with open('saved_game.pkl', 'wb') as f:
        pickle.dump((board, bci), f)

def load_game():
    with open('saved_game.pkl', 'rb') as f:
        return pickle.load(f)

def play_move_sound():
    move_sound = pygame.mixer.Sound(cfg.move_sound)
    move_sound.play()

def play_win_sound():
    pygame.mixer.music.load(cfg.win_sound)
    pygame.mixer.music.play()

def play_bg_music():
    pygame.mixer.music.load(cfg.bgm)
    pygame.mixer.music.play(-1)  # Loop the background music

def save_high_score(time):
    with open('high_scores.txt', 'a') as f:
        f.write(f'{time}\n')

def showendinterface(screen, width, height):
    screen.fill(cfg.background)
    font = pygame.font.Font(cfg.font, width // 15)
    title = font.render('Good job you won!', True, (233, 150, 122))
    rect = title.get_rect()
    rect.midtop = (width / 2, height / 2.5)
    screen.blit(title, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()

def showstartinterface(screen, width, height):
    screen.fill(cfg.background)
    tfont = pygame.font.Font(cfg.font, width // 4)
    cfont = pygame.font.Font(cfg.font, width // 20)
    title = tfont.render('Puzzle', True, cfg.RED)
    content1 = cfont.render('Press H, M or L to choose your puzzle', True, cfg.BLUE)
    content2 = cfont.render('H-5x5 L-4x4 M-3x3', True, cfg.BLUE)
    content3 = cfont.render('Press S to save game, L to load game', True, cfg.BLUE)
    trect = title.get_rect()
    trect.midtop = (width / 2, height / 10)
    crect1 = content1.get_rect()
    crect1.midtop = (width / 2, height / 2.2)
    crect2 = content2.get_rect()
    crect2.midtop = (width / 2, height / 1.8)
    crect3 = content3.get_rect()
    crect3.midtop = (width / 2, height / 1.6)
    screen.blit(title, trect)
    screen.blit(content1, crect1)
    screen.blit(content2, crect2)
    screen.blit(content3, crect3)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == ord('h'):
                    return 5
                elif event.key == ord('l'):
                    return 4
                elif event.key == ord('m'):
                    return 3
            pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    play_bg_music()
    game_img_used = pygame.image.load(Getimagepaths(cfg.pic_root_dir))
    game_img_used = pygame.transform.scale(game_img_used, cfg.screensize)
    game_img_used_rect = game_img_used.get_rect()
    screen = pygame.display.set_mode(cfg.screensize)
    pygame.display.set_caption('POKEMON')
    size = showstartinterface(screen, game_img_used_rect.width, game_img_used_rect.height)
    nrows, ncols = size, size
    ncells = nrows * ncols
    cell_width = game_img_used_rect.width // ncols
    cell_height = game_img_used_rect.height // nrows
    while True:
        game_board, bci = creatboard(nrows, ncols, ncells)
        if not isgameover(game_board, size):
            break
    is_running = True
    start_time = pygame.time.get_ticks()

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    bci = moveL(game_board, bci, ncols)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    bci = moveU(game_board, bci, nrows, ncols)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    bci = moveD(game_board, bci, ncols)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    bci = moveR(game_board, bci, ncols)
                elif event.key == pygame.K_s:
                    save_game(game_board, bci)
                elif event.key == pygame.K_l:
                    game_board, bci = load_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                cell_x, cell_y = x // cell_width, y // cell_height
                idx = cell_x + cell_y * ncols
                if idx == bci - 1:
                    bci = moveR(game_board, bci, ncols)
                elif idx == bci + 1:
                    bci = moveL(game_board, bci, ncols)
                elif idx == bci + ncols:
                    bci = moveU(game_board, bci, nrows, ncols)
                elif idx == bci - ncols:
                    bci = moveD(game_board, bci, ncols)

        if isgameover(game_board, size):
            game_board[bci] = ncells - 1
            is_running = False
            end_time = pygame.time.get_ticks()
            time_taken = (end_time - start_time) / 1000  # time in seconds
            save_high_score(time_taken)
            play_win_sound()
            showendinterface(screen, game_img_used_rect.width, game_img_used_rect.height)

        screen.fill(cfg.background)
        for i in range(ncells):
            if game_board[i] == -1:
                continue
            cell_x = i % ncols
            cell_y = i // ncols
            rect = pygame.Rect(cell_x * cell_width, cell_y * cell_height, cell_width, cell_height)
            img_area = pygame.Rect((game_board[i] % ncols) * cell_width, (game_board[i] // ncols) * cell_height, cell_width, cell_height)
            screen.blit(game_img_used, rect, img_area)

        for i in range(ncols + 1):
            pygame.draw.line(screen, cfg.BLACK, (i * cell_width, 0), (i * cell_width, game_img_used_rect.height))
        for i in range(nrows + 1):
            pygame.draw.line(screen, cfg.BLACK, (0, i * cell_height), (game_img_used_rect.width, i * cell_height))

        pygame.display.update()
        clock.tick(cfg.FPS)

if __name__ == '__main__':
    main()
