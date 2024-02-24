import pygame

pygame.init()
width = 1000
height = 900
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Two-Player Chess Game')
font = pygame.font.Font('freesansbold.ttf', 20)
Mediumfont = pygame.font.Font('freesansbold.ttf', 40)
Bigfont = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# defining pieces

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_white_pieces = []
captured_black_pieces = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

#Pieces image rendering

BlackQueen = pygame.image.load('Chess images/black queen.png')
BlackQueen = pygame.transform.scale(BlackQueen, (80, 80))
black_queen_small = pygame.transform.scale(BlackQueen, (45, 45))
BlackKing = pygame.image.load('Chess images/black king.png')
BlackKing = pygame.transform.scale(BlackKing, (80, 80))
black_king_small = pygame.transform.scale(BlackKing, (45, 45))
BlackRook = pygame.image.load('Chess images/black rook.png')
BlackRook = pygame.transform.scale(BlackRook, (80, 80))
black_rook_small = pygame.transform.scale(BlackRook, (45, 45))
BlackBishop = pygame.image.load('Chess images/black bishop.png')
BlackBishop = pygame.transform.scale(BlackBishop, (80, 80))
black_bishop_small = pygame.transform.scale(BlackBishop, (45, 45))
BlackKnight = pygame.image.load('Chess images/black knight.png')
BlackKnight = pygame.transform.scale(BlackKnight, (80, 80))
black_knight_small = pygame.transform.scale(BlackKnight, (45, 45))
BlackPawn = pygame.image.load('Chess images/black pawn.png')
BlackPawn = pygame.transform.scale(BlackPawn, (65, 65))
black_pawn_small = pygame.transform.scale(BlackPawn, (45, 45))
WhiteQueen = pygame.image.load('Chess images/white queen.png')
WhiteQueen = pygame.transform.scale(WhiteQueen, (80, 80))
white_queen_small = pygame.transform.scale(WhiteQueen, (45, 45))
WhiteKing = pygame.image.load('Chess images/white king.png')
WhiteKing = pygame.transform.scale(WhiteKing, (80, 80))
white_king_small = pygame.transform.scale(WhiteKing, (45, 45))
WhiteRook = pygame.image.load('Chess images/white rook.png')
WhiteRook = pygame.transform.scale(WhiteRook, (80, 80))
white_rook_small = pygame.transform.scale(WhiteRook, (45, 45))
WhiteBishop = pygame.image.load('Chess images/white bishop.png')
WhiteBishop = pygame.transform.scale(WhiteBishop, (80, 80))
white_bishop_small = pygame.transform.scale(WhiteBishop, (45, 45))
WhiteKnight = pygame.image.load('Chess images/white knight.png')
WhiteKnight = pygame.transform.scale(WhiteKnight, (80, 80))
white_knight_small = pygame.transform.scale(WhiteKnight, (45, 45))
WhitePawn = pygame.image.load('Chess images/white pawn.png')
WhitePawn = pygame.transform.scale(WhitePawn, (65, 65))
white_pawn_small = pygame.transform.scale(WhitePawn, (45, 45))
WhiteImages = [WhitePawn, WhiteQueen, WhiteKing, WhiteKnight, WhiteRook, WhiteBishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
BlackImages = [BlackPawn, BlackQueen, BlackKing, BlackKnight, BlackRook, BlackBishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
counter = 0
winner = ''
game_over = False


# display
def board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, width, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, width, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, height], 5)
        text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(Bigfont.render(text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(Mediumfont.render('FORFEIT', True, 'black'), (810, 830))


# enter the pieces on to the board
def pieces_position():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(WhitePawn, (white_location[i][0] * 100 + 22, white_location[i][1] * 100 + 30))
        else:
            screen.blit(WhiteImages[index], (white_location[i][0] * 100 + 10, white_location[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_location[i][0] * 100 + 1, white_location[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(BlackPawn, (black_location[i][0] * 100 + 22, black_location[i][1] * 100 + 30))
        else:
            screen.blit(BlackImages[index], (black_location[i][0] * 100 + 10, black_location[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_location[i][0] * 100 + 1, black_location[i][1] * 100 + 1,
                                                  100, 100], 2)


# function to check all pieces valid on the given position
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# checks valid move for king
def check_king(position, colour):
    moves_list = []
    if colour == 'white':
        EnemiesList = black_location
        FriendList = white_location
    else:
        FriendList = black_location
        EnemiesList = white_location
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in FriendList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check valid move for queen
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check valid move for bishop
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, colour):
    moves_list = []
    if colour == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_location and \
                (position[0], position[1] + 1) not in black_location and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_location and \
                (position[0], position[1] + 2) not in black_location and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_location:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_location:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_location and \
                (position[0], position[1] - 1) not in black_location and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_location and \
                (position[0], position[1] - 2) not in black_location and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_location:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_location:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, colour):
    moves_list = []
    if colour == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# display valid moves on screen
def display_valid(moves):
    if turn_step < 2:
        colour = 'red'
    else:
        colour = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


# display captured pieces on side of screen
def display_captured():
    for i in range(len(captured_white_pieces)):
        captured_piece = captured_white_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_black_pieces)):
        captured_piece = captured_black_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


# display a colored square around king if in check
def display_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_location[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_location[king_index][0] * 100 + 1,
                                                              white_location[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_location[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_location[king_index][0] * 100 + 1,
                                                               black_location[king_index][1] * 100 + 1, 100, 100], 5)


def display_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


#Game Logic
black_options = check_options(black_pieces, black_location, 'black')
white_options = check_options(white_pieces, white_location, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    board()
    pieces_position()
    display_captured()
    display_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        display_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_location:
                    selection = white_location.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_location[selection] = click_coords
                    if click_coords in black_location:
                        black_piece = black_location.index(click_coords)
                        captured_white_pieces.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_location.pop(black_piece)
                    black_options = check_options(black_pieces, black_location, 'black')
                    white_options = check_options(white_pieces, white_location, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_location:
                    selection = black_location.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_location[selection] = click_coords
                    if click_coords in white_location:
                        white_piece = white_location.index(click_coords)
                        captured_black_pieces.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_location.pop(white_piece)
                    black_options = check_options(black_pieces, black_location, 'black')
                    white_options = check_options(white_pieces, white_location, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_white_pieces = []
                captured_black_pieces = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_location, 'black')
                white_options = check_options(white_pieces, white_location, 'white')

    if winner != '':
        game_over = True
        display_game_over()

    pygame.display.flip()
pygame.quit()