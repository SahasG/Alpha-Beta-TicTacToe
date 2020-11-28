import random
import copy

class TicTacToePlayer:
    """ An object representation for an AI game player for the game TicTacToe.
    """
    board = [[' ' for j in range(3)] for i in range(3)]
    pieces = ['x', 'o']

    def __init__(self):
        """ Initializes a TicTacToePlayer object by randomly selecting x or o as its
        piece.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
    
    def succ(self, state):
        successors = []
        for row in range(3):
            for col in range(3):
                if(state[row][col] == ' '):
                    temp_successor = copy.deepcopy(state)
                    temp_successor[row][col] = self.my_piece
                    successors.append(temp_successor)
        return successors
    
    def Max_Value(self, state, depth, alpha, beta):
        if(self.game_value(state) == 1):
            return self.game_value(state) + (1 - (depth/3))
        if(self.game_value(state) == -1):
            return self.game_value(state) - (1 - (depth/3))
        else:
            if(depth == 1):
                return self.heuristic_game_value(state)
            else:
                for s in self.succ(state):
                    alpha = max(alpha, self.Min_Value(s, depth+1, alpha, beta))
                    if(alpha>=beta):
                        return beta
            return alpha
        
    def Min_Value(self, state, depth, alpha, beta):
        if(self.game_value(state) == 1):
            return self.game_value(state) + (1 - (depth/3))
        if(self.game_value(state) == -1):
            return self.game_value(state) - (1 - (depth/3))
        else:
            if(depth == 1):
                return self.heuristic_game_value(state)
            else:
                for s in self.succ(state):
                    beta = min(beta, self.Max_Value(s, depth+1, alpha, beta))
                    if(alpha>=beta):
                        return beta
            return beta
    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. Whenever
        this function is called, it is A.I's turn.

        Args:
            state (list of lists): Takes in the current board state in order to figure out the optimal successor

        Return:
            move (list): a list of move tuples such that its format is (row, col)
                where the (row, col) tuple is the location to place a piece.

        """

        
        move = []
        
        #Usage of Minimax ALgorithm
        max_alpha = float('-inf')
        best_move = []
        successors = self.succ(state)
        for s in successors:
            curr_alpha = self.Max_Value(s, 0, float('-inf'), float('inf'))
            if(curr_alpha > max_alpha):
                max_alpha = curr_alpha
                best_move = s
                    
        for row in range(3):
            for col in range(3):
                if(best_move[row][col] == self.my_piece):
                    if(state[row][col] != self.my_piece):
                        move.insert(0, (row, col))
                            
           
        return move

    
    
    
    
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.

        Args:
            move (list): a list of move tuples such that its format is (row, col)
                where the (row, col) tuple is the location to place a piece.
        """
        
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is (row, col)
                where the (row, col) tuple is the location to place a piece.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('x' or 'o') to place on the board
        """
        
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game or a generated successor state.

        Returns:
            int: 1 if this A.I wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            if row[0] != ' ' and row[0] == row[1] == row[2]:
                    return 1 if row[0]==self.my_piece else -1

        # check vertical wins
        for col in range(3):
            if state[0][col] != ' ' and state[0][col] == state[1][col] == state[2][col]:
                    return 1 if state[0][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2]:
                    return 1 if state[0][0] == self.my_piece else -1
        
        # TODO: check / diagonal wins
        if state[2][0] != ' ' and state[2][0] == state[1][1] == state[0][2]:
                    return 1 if state[2][0] == self.my_piece else -1
        
        return 0 # no winner yet
    
    def heuristic_game_value(self, state):
        game_theoretic_val = self.game_value(state)
        if(game_theoretic_val == 0):
            total = 0.0
            for row in state:
                if row[0] != ' ' and row[0] == row[1]:
                    return 0.3 if row[0]==self.my_piece else -0.3
                elif row[1] != ' ' and row[1] == row[2]:
                    return 0.3 if row[1]==self.my_piece else -0.3
                elif row[0] != ' ' and row[0] == row[2]:
                    return 0.3 if row[0]==self.my_piece else -0.3
            
            for col in range(3):
                if state[0][col] != ' ' and state[0][col] == state[1][col]:
                    return 0.3 if state[0][col]==self.my_piece else -0.3
                elif state[1][col] != ' ' and state[1][col] == state[2][col]:
                    return 0.3 if state[1][col]==self.my_piece else -0.3
                elif state[0][col] != ' ' and state[0][col] == state[2][col]:
                    return 0.3 if state[0][col]==self.my_piece else -0.3
                
            if state[0][0] != ' ' and state[0][0] == state[1][1]:
                    return 0.3 if state[0][0] == self.my_piece else -0.3
            elif state[1][1] != ' ' and state[1][1] == state[2][2]:
                    return 0.3 if state[1][1] == self.my_piece else -0.3
            elif state[0][0] != ' ' and state[0][0] == state[2][2]:
                    return 0.3 if state[0][0] == self.my_piece else -0.3
            
            if state[2][0] != ' ' and state[2][0] == state[1][1]:
                    return 0.3 if state[2][0] == self.my_piece else -0.3
            elif state[1][1] != ' ' and state[1][1] == state[0][2]:
                    return 0.3 if state[1][1] == self.my_piece else -0.3
            elif state[2][0] != ' ' and state[2][0] == state[0][2]:
                    return 0.3 if state[2][0] == self.my_piece else -0.3
                
            if(total >= 1):
                total = 0.99
            elif(total <= (-1)):
                total = -0.99
            return total
        else:
            return game_theoretic_val
            

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    ai = TicTacToePlayer()
    piece_count = 0
    turn = 0

    while piece_count < 9 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "012":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                    
                except Exception as e:
                    print(e)

        piece_count += 1
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    elif ai.game_value(ai.board) == -1:
        print("You win! Game over.")
    else:
        print("Tie! Game over.")


if __name__ == "__main__":
    main()

