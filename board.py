import copy
import piece_classes


class Board:
    def __init__(self):
        self.pieces = []
        self.legal_moves = []
        self.to_move = "White"
        self.checkmated = False
        self.stalemate = False
        self.past_move = [[1, 1], [1, 1]]

        Ra1 = piece_classes.Rook([1, 1], "White", self)
        Nb1 = piece_classes.Knight([1, 2], "White", self)
        Bc1 = piece_classes.Bishop([1, 3], "White", self)
        Qd1 = piece_classes.Queen([1, 4], "White", self)
        Ke1 = piece_classes.King([1, 5], "White", self)
        Bf1 = piece_classes.Bishop([1, 6], "White", self)
        Ng1 = piece_classes.Knight([1, 7], "White", self)
        Rh1 = piece_classes.Rook([1, 8], "White", self)
        self.pieces.append([None] * 10)
        self.pieces.append([None, Ra1, Nb1, Bc1, Qd1, Ke1, Bf1, Ng1, Rh1, None])

        pawn_line = []
        for i in range(10):
            if i == 0 or i == 9:
                pawn_line.append(None)
            else:
                pawn = piece_classes.Pawn([2, i], "White", self)
                pawn_line.append(pawn)
        self.pieces.append(pawn_line)

        for i in range(4):
            empty_line = [None] * 10
            self.pieces.append(empty_line)

        pawn_line = []
        for i in range(10):
            if i == 0 or i == 9:
                pawn_line.append(None)
            else:
                pawn = piece_classes.Pawn([7, i], "Black", self)
                pawn_line.append(pawn)
        self.pieces.append(pawn_line)

        Ra8 = piece_classes.Rook([8, 1], "Black", self)
        Nb8 = piece_classes.Knight([8, 2], "Black", self)
        Bc8 = piece_classes.Bishop([8, 3], "Black", self)
        Qd8 = piece_classes.Queen([8, 4], "Black", self)
        Ke8 = piece_classes.King([8, 5], "Black", self)
        Bf8 = piece_classes.Bishop([8, 6], "Black", self)
        Ng8 = piece_classes.Knight([8, 7], "Black", self)
        Rh8 = piece_classes.Rook([8, 8], "Black", self)
        self.pieces.append([None, Ra8, Nb8, Bc8, Qd8, Ke8, Bf8, Ng8, Rh8, None])

        self.pieces.append([None] * 10)

    def delete_piece(self, position):
        for row in self.pieces:
            for piece in row:
                if piece is not None:
                    if piece.position == position:
                        self.pieces[position[0]][position[1]] = None

    def move_piece(self, position, next_position):
        for row in self.pieces:
            for piece in row:
                if piece is not None:
                    if piece.position == position:
                        piece.position = next_position
                        self.pieces[position[0]][position[1]] = None
                        self.pieces[next_position[0]][next_position[1]] = piece

    # need to add castle, en-passant, promote
    def make_move(self, move):
        self.past_move = move

        piece = self.get_piece(move[0])
        if piece is not None:
            if piece.type_name == "King":
                if move == [[1, 5], [1, 7]]:
                    self.move_piece([1, 8], [1, 6])
                    self.move_piece([1, 5], [1, 7])
                    return
                if move == [[1, 5], [1, 3]]:
                    self.move_piece([1, 1], [1, 4])
                    self.move_piece([1, 5], [1, 3])
                    return
                if move == [[8, 5], [8, 7]]:
                    self.move_piece([8, 8], [8, 6])
                    self.move_piece([8, 5], [8, 7])
                    return
                if move == [[8, 5], [8, 3]]:
                    self.move_piece([8, 1], [8, 4])
                    self.move_piece([8, 5], [8, 3])
                    return
            elif piece.type_name == "Pawn":
                if move[1][0] == 8 or move[1][0] == 1:
                    # piece_name = input() I can add options
                    new_piece = piece_classes.Queen(move[1], piece.color, self)
                    self.pieces[move[1][0]][move[1][1]] = new_piece
                    self.delete_piece(move[0])
                    return

                if self.get_piece(move[1]) is None:
                    offset = move[1][1] - move[0][1]
                    self.move_piece(move[0], move[1])
                    self.delete_piece([move[0][0], move[0][1] + offset])
                    return

        moving_piece = self.get_piece(move[0])
        moving_piece.has_moved = True

        if self.to_move == "White":
            opposite_color = "Black"
        else:
            opposite_color = "White"

        if self.get_square(move[1]) == opposite_color:
            self.delete_piece(move[1])
        self.move_piece(move[0], move[1])

    def get_piece(self, position):
        return self.pieces[position[0]][position[1]]

    def get_square(self, position):
        piece = self.get_piece(position)
        if piece is None:
            if (position[0] == 0 or position[0] == 9) or (position[1] == 0 or position[1] == 9):
                return "Bound"
            else:
                return "Empty"
        else:
            return piece.color

    def is_in_check(self, color):
        king_position = [1, 1]
        for row in self.pieces:
            for piece in row:
                if piece is not None:
                    if piece.type_name == "King" and piece.color == color:
                        king_position = piece.position

        if self.is_threatened(king_position, color):
            return True
        else:
            return False

    def is_threatened(self, position, color):
        possible_position = position
        if color == "White":
            opposite_color = "Black"
        elif color == "Black":
            opposite_color = "White"
        else:
            opposite_color = "Unexpected Behaviour"

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1] + 1]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Bishop" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1] - 1]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Bishop" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1] - 1]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Bishop" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1] + 1]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Bishop" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1]]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Rook" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1]]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Rook" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0], possible_position[1] + 1]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Rook" or piece.type_name == "Queen":
                    return True

        possible_position = position

        while self.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0], possible_position[1] - 1]
            if self.get_square(possible_position) == color:
                break
            elif self.get_square(possible_position) == opposite_color:
                piece = self.get_piece(possible_position)
                if piece.type_name == "Rook" or piece.type_name == "Queen":
                    return True

        possible_squares = []
        if position[1] < 7:
            possible_squares.append([position[0] + 1, position[1] + 2])
            possible_squares.append([position[0] - 1, position[1] + 2])
        if position[1] > 2:
            possible_squares.append([position[0] - 1, position[1] - 2])
            possible_squares.append([position[0] + 1, position[1] - 2])
        if position[0] < 7:
            possible_squares.append([position[0] + 2, position[1] + 1])
            possible_squares.append([position[0] + 2, position[1] - 1])
        if position[0] > 2:
            possible_squares.append([position[0] - 2, position[1] - 1])
            possible_squares.append([position[0] - 2, position[1] + 1])

        if position[0] == 1:
            if [position[0] - 1, position[1] + 2] in possible_squares:
                possible_squares.remove([position[0] - 1, position[1] + 2])
            if [position[0] - 1, position[1] - 2] in possible_squares:
                possible_squares.remove([position[0] - 1, position[1] - 2])

        if position[1] == 1:
            if [position[0] - 2, position[1] - 1] in possible_squares:
                possible_squares.remove([position[0] - 2, position[1] - 1])
            if [position[0] + 2, position[1] - 1] in possible_squares:
                possible_squares.remove([position[0] + 2, position[1] - 1])

        if position[0] == 8:
            if [position[0] + 1, position[1] + 2] in possible_squares:
                possible_squares.remove([position[0] + 1, position[1] + 2])
            if [position[0] + 1, position[1] - 2] in possible_squares:
                possible_squares.remove([position[0] + 1, position[1] - 2])

        if position[1] == 8:
            if [position[0] - 2, position[1] + 1] in possible_squares:
                possible_squares.remove([position[0] - 2, position[1] + 1])
            if [position[0] + 2, position[1] + 1] in possible_squares:
                possible_squares.remove([position[0] + 2, position[1] + 1])

        for square in possible_squares:
            piece = self.get_piece(square)
            if piece is not None:
                if piece.type_name == "Knight" and piece.color == opposite_color:
                    return True

        piece = self.get_piece(position)
        if piece is not None:
            if piece.color == "White":
                right_diagonal = self.get_piece([position[0]+1, position[1]+1])
                left_diagonal = self.get_piece([position[0]+1, position[1]-1])
                if right_diagonal is not None:
                    if right_diagonal.type_name == "Pawn" and right_diagonal.color == "Black":
                        return True
                if left_diagonal is not None:
                    if left_diagonal.type_name == "Pawn" and left_diagonal.color == "Black":
                        return True
            if piece.color == "Black":
                right_diagonal = self.get_piece([position[0]-1, position[1]-1])
                left_diagonal = self.get_piece([position[0]-1, position[1]+1])
                if right_diagonal is not None:
                    if right_diagonal.type_name == "Pawn" and right_diagonal.color == "White":
                        return True
                if left_diagonal is not None:
                    if left_diagonal.type_name == "Pawn" and left_diagonal.color == "White":
                        return True

        return False

    def list_legal_moves(self, color):
        for row in self.pieces:
            legal_moves_line = []
            for piece in row:
                legal_moves_cell = []
                if piece is not None:
                    if piece.color == color:
                        for possible_move in piece.possible_moves:
                            try_board = copy.deepcopy(self)
                            try_board.make_move([piece.position, possible_move])
                            if not try_board.is_in_check(color):
                                legal_moves_cell.append(possible_move)

                legal_moves_line.append(legal_moves_cell)

            self.legal_moves.append(legal_moves_line)

    def update_position(self, move):
        # lists legal moves for each piece
        for row in self.pieces:
            for piece in row:
                if piece is not None:
                    piece.list_possible_moves()
        self.list_legal_moves(self.to_move)

        piece_legal_moves = self.legal_moves[move[0][0]][move[0][1]]
        if move[1] not in piece_legal_moves:
            print("not a legal move")
            self.legal_moves = []
            return False
        else:
            self.make_move(move)
            for row in self.pieces:
                for piece in row:
                    if piece is not None:
                        piece.possible_moves = []
            self.legal_moves = []
            return True

    def check_game_state(self):
        # checks if game has ended

        if self.to_move == "White":
            opposite_color = "Black"
        else:
            opposite_color = "White"

        # lists legal moves for each piece
        for row in self.pieces:
            for piece in row:
                if piece is not None:
                    piece.list_possible_moves()
        self.list_legal_moves(opposite_color)

        legal_moves_num = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if self.pieces[i][j] is not None:
                    if self.get_square([i, j]) == opposite_color:
                        legal_moves_num += len(self.legal_moves[i][j])

        if legal_moves_num == 0 and self.is_in_check(opposite_color):
            self.checkmated = True
        elif legal_moves_num == 0 and not self.is_in_check(opposite_color):
            self.stalemate = True

        if self.stalemate or self.checkmated:
            print("game ended")
            return False
        else:
            if self.to_move == "White":
                self.to_move = "Black"
            else:
                self.to_move = "White"

            for row in self.pieces:
                for piece in row:
                    if piece is not None:
                        piece.possible_moves = []
            self.legal_moves = []
            return True

    def print_board(self):
        for i in range(1, 9):
            line = ""
            for j in range(1, 9):
                piece = self.get_piece([i, j])
                if piece is not None:
                    line += piece.type_name[0]
                else:
                    line += "-"
            print(line)