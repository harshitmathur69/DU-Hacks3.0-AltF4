import pygame

pygame.init()
width = 1000
height = 900
Display = pygame.display.set_mode([width, height])
pygame.display.set_caption('Two-Player Chess Game')
font = pygame.font.Font('freesansbold.ttf', 20)
Mediumfont = pygame.font.Font('freesansbold.ttf', 40)
Bigfont = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# defining pieces

WhitePieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
WhiteLocation = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                 (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
BlackPieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
BlackLocation = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                 (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_white_pieces = []
captured_black_pieces = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
Turn = 0
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
PieceList = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
counter = 0
winner = ''
game_over = False


# display
def board():
    for i in range(32):
        columns = i % 4
        rows = i // 4
        if rows % 2 == 0:
            pygame.draw.rect(Display, 'light gray', [600 - (columns * 200), rows * 100, 100, 100])
        else:
            pygame.draw.rect(Display, 'light gray', [700 - (columns * 200), rows * 100, 100, 100])
        pygame.draw.rect(Display, 'gray', [0, 800, width, 100])
        pygame.draw.rect(Display, 'gold', [0, 800, width, 100], 5)
        pygame.draw.rect(Display, 'gold', [800, 0, 200, height], 5)
        text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        Display.blit(Bigfont.render(text[Turn], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(Display, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(Display, 'black', (100 * i, 0), (100 * i, 800), 2)
        Display.blit(Mediumfont.render('FORFEIT', True, 'black'), (810, 830))


# enter the pieces on to the board
def PiecesPosition():
    for i in range(len(WhitePieces)):
        index = PieceList.index(WhitePieces[i])
        if WhitePieces[i] == 'pawn':
            Display.blit(WhitePawn, (WhiteLocation[i][0] * 100 + 22, WhiteLocation[i][1] * 100 + 30))
        else:
            Display.blit(WhiteImages[index], (WhiteLocation[i][0] * 100 + 10, WhiteLocation[i][1] * 100 + 10))
        if Turn < 2:
            if selection == i:
                pygame.draw.rect(Display, 'red', [WhiteLocation[i][0] * 100 + 1, WhiteLocation[i][1] * 100 + 1,
                                                  100, 100], 2)

    for i in range(len(BlackPieces)):
        index = PieceList.index(BlackPieces[i])
        if BlackPieces[i] == 'pawn':
            Display.blit(BlackPawn, (BlackLocation[i][0] * 100 + 22, BlackLocation[i][1] * 100 + 30))
        else:
            Display.blit(BlackImages[index], (BlackLocation[i][0] * 100 + 10, BlackLocation[i][1] * 100 + 10))
        if Turn >= 2:
            if selection == i:
                pygame.draw.rect(Display, 'blue', [BlackLocation[i][0] * 100 + 1, BlackLocation[i][1] * 100 + 1,
                                                   100, 100], 2)


# function to check all pieces valid on the given position
def CheckMoves(pieces, locations, turn):
    MoveList = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            MoveList = PawnMoves(location, turn)
        elif piece == 'rook':
            MoveList = RookMoves(location, turn)
        elif piece == 'knight':
            MoveList = KnightMoves(location, turn)
        elif piece == 'bishop':
            MoveList = BishopMoves(location, turn)
        elif piece == 'queen':
            MoveList = QueenMoves(location, turn)
        elif piece == 'king':
            MoveList = KingMoves(location, turn)
        all_moves_list.append(MoveList)
    return all_moves_list


# checks valid move for king
def KingMoves(position, colour):
    MoveList = []
    if colour == 'white':
        EnemiesList = BlackLocation
        FriendList = WhiteLocation
    else:
        FriendList = BlackLocation
        EnemiesList = WhiteLocation
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in FriendList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            MoveList.append(target)
    return MoveList


# check valid move for queen
def QueenMoves(position, color):
    MoveList = BishopMoves(position, color)
    second_list = RookMoves(position, color)
    for i in range(len(second_list)):
        MoveList.append(second_list[i])
    return MoveList


# check valid move for bishop
def BishopMoves(position, color):
    MoveList = []
    if color == 'white':
        enemies_list = BlackLocation
        friends_list = WhiteLocation
    else:
        friends_list = BlackLocation
        enemies_list = WhiteLocation
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
                MoveList.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return MoveList


# check rook moves
def RookMoves(position, colour):
    MoveList = []
    if colour == 'white':
        EnimiesList = BlackLocation
        FriendList = WhiteLocation
    else:
        FriendList = BlackLocation
        EnimiesList = WhiteLocation
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
            if (position[0] + (chain * x), position[1] + (chain * y)) not in FriendList and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                MoveList.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in EnimiesList:
                    path = False
                chain += 1
            else:
                path = False
    return MoveList


# check valid pawn moves
def PawnMoves(position, colour):
    MoveList = []
    if colour == 'white':
        if (position[0], position[1] + 1) not in WhiteLocation and \
                (position[0], position[1] + 1) not in BlackLocation and position[1] < 7:
            MoveList.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in WhiteLocation and \
                (position[0], position[1] + 2) not in BlackLocation and position[1] == 1:
            MoveList.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in BlackLocation:
            MoveList.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in BlackLocation:
            MoveList.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in WhiteLocation and \
                (position[0], position[1] - 1) not in BlackLocation and position[1] > 0:
            MoveList.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in WhiteLocation and \
                (position[0], position[1] - 2) not in BlackLocation and position[1] == 6:
            MoveList.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in WhiteLocation:
            MoveList.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in WhiteLocation:
            MoveList.append((position[0] - 1, position[1] - 1))
    return MoveList


# check valid knight moves
def KnightMoves(position, colour):
    MoveList = []
    if colour == 'white':
        enemies_list = BlackLocation
        friends_list = WhiteLocation
    else:
        friends_list = BlackLocation
        enemies_list = WhiteLocation
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            MoveList.append(target)
    return MoveList


# check for valid moves for selected piece
def ValidMoves():
    if Turn < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# display valid moves on screen
def DisplayValidMoves(moves):
    if Turn < 2:
        colour = 'red'
    else:
        colour = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(Display, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


# display captured pieces on side of screen
def DisplayCapturedPiece():
    for i in range(len(captured_white_pieces)):
        captured_piece = captured_white_pieces[i]
        index = PieceList.index(captured_piece)
        Display.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_black_pieces)):
        captured_piece = captured_black_pieces[i]
        index = PieceList.index(captured_piece)
        Display.blit(small_white_images[index], (925, 5 + 50 * i))


# display a colored square around king if in check
def DisplayCheck():
    if Turn < 2:
        if 'king' in WhitePieces:
            king_index = WhitePieces.index('king')
            king_location = WhiteLocation[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(Display, 'dark red', [WhiteLocation[king_index][0] * 100 + 1,
                                                               WhiteLocation[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in BlackPieces:
            king_index = BlackPieces.index('king')
            king_location = BlackLocation[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(Display, 'dark blue', [BlackLocation[king_index][0] * 100 + 1,
                                                                BlackLocation[king_index][1] * 100 + 1, 100, 100], 5)


def GameOver():
    pygame.draw.rect(Display, 'black', [200, 200, 400, 70])
    Display.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    Display.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


#Game Logic
black_options = CheckMoves(BlackPieces, BlackLocation, 'black')
white_options = CheckMoves(WhitePieces, WhiteLocation, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    Display.fill('dark gray')
    board()
    PiecesPosition()
    DisplayCapturedPiece()
    DisplayCheck()
    if selection != 100:
        valid_moves = ValidMoves()
        DisplayValidMoves(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if Turn <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in WhiteLocation:
                    selection = WhiteLocation.index(click_coords)
                    if Turn == 0:
                        Turn = 1
                if click_coords in valid_moves and selection != 100:
                    WhiteLocation[selection] = click_coords
                    if click_coords in BlackLocation:
                        black_piece = BlackLocation.index(click_coords)
                        captured_white_pieces.append(BlackPieces[black_piece])
                        if BlackPieces[black_piece] == 'king':
                            winner = 'white'
                        BlackPieces.pop(black_piece)
                        BlackLocation.pop(black_piece)
                    black_options = CheckMoves(BlackPieces, BlackLocation, 'black')
                    white_options = CheckMoves(WhitePieces, WhiteLocation, 'white')
                    Turn = 2
                    selection = 100
                    valid_moves = []
            if Turn > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in BlackLocation:
                    selection = BlackLocation.index(click_coords)
                    if Turn == 2:
                        Turn = 3
                if click_coords in valid_moves and selection != 100:
                    BlackLocation[selection] = click_coords
                    if click_coords in WhiteLocation:
                        white_piece = WhiteLocation.index(click_coords)
                        captured_black_pieces.append(WhitePieces[white_piece])
                        if WhitePieces[white_piece] == 'king':
                            winner = 'black'
                        WhitePieces.pop(white_piece)
                        WhiteLocation.pop(white_piece)
                    black_options = CheckMoves(BlackPieces, BlackLocation, 'black')
                    white_options = CheckMoves(WhitePieces, WhiteLocation, 'white')
                    Turn = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                WhitePieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                WhiteLocation = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                 (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                BlackPieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                BlackLocation = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                 (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_white_pieces = []
                captured_black_pieces = []
                Turn = 0
                selection = 100
                valid_moves = []
                black_options = CheckMoves(BlackPieces, BlackLocation, 'black')
                white_options = CheckMoves(WhitePieces, WhiteLocation, 'white')

    if winner != '':
        game_over = True
        GameOver()

    pygame.display.flip()
pygame.quit()