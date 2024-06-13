import board
import pygame
import sys


def convert_notation(s):
    letter = s[0]
    next_letter = s[3]
    ascii_value = ord(letter) - 96
    next_ascii_value = ord(next_letter) - 96
    row = int(s[1])
    next_row = int(s[-1])
    return [[row, ascii_value], [next_row, next_ascii_value]]


# Constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")


# Load images (ensure you have images named properly in the assets folder)
def load_images():
    pieces = ['White_Pawn', 'Black_Pawn', 'White_Rook', 'Black_Rook', 'White_Knight', 'Black_Knight',
              'White_Bishop', 'Black_Bishop', 'White_Queen', 'Black_Queen', 'White_King', 'Black_King']
    assets = {}
    for piece in pieces:
        assets[piece] = pygame.transform.scale(
            pygame.image.load(f'images/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
        )
    return assets


images = load_images()


# Draw the chess board
def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# Draw the pieces on the board
def draw_pieces(screen, game_board):
    for row in range(0, BOARD_SIZE+1):
        for col in range(0, BOARD_SIZE+1):
            piece = game_board.get_piece([row, col])
            if piece is not None:
                piece_name = piece.color + '_' + piece.type_name
                x = (col-1) * SQUARE_SIZE
                y = HEIGHT - row * SQUARE_SIZE
                screen.blit(images[piece_name], pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))


def get_board_coords(mouse_pos):
    x, y = mouse_pos
    col = x // SQUARE_SIZE + 1
    row = BOARD_SIZE - (y // SQUARE_SIZE)
    return row, col


def main():
    print("-------------WELCOME TO THE GAME OF CHESS---------------")
    game_board = board.Board()
    game_continues = True
    piece_selected = False
    move = []

    while game_continues:

        screen.fill(pygame.Color("black"))  # Clear the screen with a background color
        draw_board(screen)
        draw_pieces(screen, game_board)
        pygame.display.flip()  # Update the display

        check = game_board.is_in_check(game_board.to_move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece_selected:
                    if selected_piece is not None:
                        next_pos = pygame.mouse.get_pos()
                        next_row, next_col = get_board_coords(next_pos)
                        move.append([next_row, next_col])
                    piece_selected = False
                else:
                    pos = pygame.mouse.get_pos()
                    row, col = get_board_coords(pos)
                    selected_piece = game_board.get_piece([row, col])
                    piece_selected = True
                    move.append([row, col])

        try:
            try_it_boy = move[0][1] + move[1][1]
        except:
            continue

        is_legal = game_board.update_position(move)
        print(move)
        if not is_legal:
            dest = game_board.get_piece(move[1])
            if dest is not None:
                if dest.color == game_board.to_move:
                    move = [move[1]]
                    piece_selected = True
                else:
                    move = []
                    piece_selected = False
            else:
                move = []
                piece_selected = False
            continue

        screen.fill(pygame.Color("black"))  # Clear the screen with a background color
        draw_board(screen)
        draw_pieces(screen, game_board)
        pygame.display.flip()  # Update the display

        game_continues = game_board.check_game_state()

        if not game_continues:
            if game_board.checkmated:
                print("game has ended, checkmate!")
            elif game_board.stalemate:
                print("game has ended, stalemate!")
            pygame.quit()
            sys.exit()

    print("thank you for playing!")


if __name__ == '__main__':
    main()