import random

class Constants:    
    EMPTY_SLOT = -1
    O_SLOT = 0
    X_SLOT = 1

    CLEAN_BOARD = [
                   [EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT],
                   [EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT],
                   [EMPTY_SLOT, EMPTY_SLOT ,EMPTY_SLOT]
                ]

    CLEAN_BOARD_TEST = [
                   [X_SLOT, EMPTY_SLOT, EMPTY_SLOT],
                   [X_SLOT, O_SLOT,     EMPTY_SLOT],
                   [O_SLOT, EMPTY_SLOT ,X_SLOT]
                ]    

    DIGIT_BOARD = [
                   [10**0 + 10**3 + 10**6,  10**0 + 10**4,                  10**0 + 10**5 + 10**7],
                   [10**1 + 10**3,          10**1 + 10**4 + 10**6 + 10**7,  10**1 + 10**5],
                   [10**2 + 10**3 + 10**7,  10**2 + 10**4,                  10**2 + 10**5 + 10**6]
                ]

    # Status
    PLAYER_WON = 0
    PC_WON = 1
    TIE = 2
    ERR_GAME_OVER = 3
    ERR_INVALID_MOVE = 4
    ERR_RESTART_ON_FIRST = 5


class State:
    PRE_START = 0
    PLAYER_MOVE = 1 # TODO : change to GAME_RUNS
    GAME_OVER = 2

class GameResult:
    NOT_FINISHED = -1
    PLAYER_WON = 0
    COMPUTER_WON = 1
    TIE = 2

class Difficulty:
    EASY = 30
    HARD = 70
    IMPOSSIBLE = 100
    DIFF_TO_STR = {
        EASY : "easy",
        HARD : "hard",
        IMPOSSIBLE : "impossible"
    }



# Responsible for game logic : legal \ illegal moves, board state, computer move calc etc...
# TODO : maybe change opponent_start to player_start
class TicTacToeEngine:

    def __init__(self):
        self.board = [x[:] for x in Constants.CLEAN_BOARD]
        self.opponent_start = None
        self.state = State.PRE_START
        self.game_res = GameResult.NOT_FINISHED
        self.last_moves = None
        self.difficulty = Difficulty.EASY

    def start(self, opponent_start=False):
        self.opponent_start = opponent_start
        self.state = State.PLAYER_MOVE
        self.last_moves = []

        if not self.opponent_start:
            self.do_self_move()

    def restart(self):
        assert self.opponent_start != None, "Should not be able to restart before game started..."

        self.opponent_start = not self.opponent_start
        self.game_res = GameResult.NOT_FINISHED
        self.state = State.PLAYER_MOVE
        self.board = [x[:] for x in Constants.CLEAN_BOARD]
        self.last_moves = []

        if not self.opponent_start:
            self.do_self_move()

    def do_self_move(self):
        row, col = self.calculate_move()
        self.board[row][col] = Constants.O_SLOT if self.opponent_start else Constants.X_SLOT

        self.last_moves.append([row, col])

        [game_over, game_res] = self.check_game_over()
        if game_over:
            self.state = State.GAME_OVER
            self.game_res = game_res    
        

    def get_available_moves(self):
        available_moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == Constants.EMPTY_SLOT:
                    available_moves.append([row, col])
        
        return available_moves

    def get_random_available_move(self):
        available_moves = self.get_available_moves()
        assert available_moves

        rand_i = random.randint(0, len(available_moves)-1)

        print("Got random move : {}".format(available_moves[rand_i]))
        return available_moves[rand_i]

    def get_perfect_move_helper(self, possible_moves, bot_turn):
        [game_over, game_res] = self.check_game_over()
        if game_over:
            if game_res == GameResult.COMPUTER_WON:
                return 1
            if game_res == GameResult.PLAYER_WON:
                return 0
            if game_res == GameResult.TIE:
                return 0.5
            
        curr_move_x_o_sign = Constants.X_SLOT
        if (bot_turn and self.opponent_start) or (not bot_turn and not self.opponent_start):
            curr_move_x_o_sign = Constants.O_SLOT

        num_of_moves = len(possible_moves)
        curr_min_max = None
        for i in range(num_of_moves):
            move = possible_moves.pop(0)
            self.board[move[0]][move[1]] = curr_move_x_o_sign
            
            ret_eval = self.get_perfect_move_helper(possible_moves, not bot_turn)
            
            self.board[move[0]][move[1]] = Constants.EMPTY_SLOT
            possible_moves.append(move)
            
            curr_min_max = ret_eval if curr_min_max is None else \
                           (min(curr_min_max, ret_eval) if not bot_turn else max(curr_min_max, ret_eval))
        
        return curr_min_max

    def get_perfect_move(self):
        possible_moves = self.get_available_moves()
        assert possible_moves

        num_of_moves = len(possible_moves)
        pre_board = [x[:] for x in self.board]
        
        curr_best_move = None
        curr_best_eval = 0
        for i in range(num_of_moves):
            move = possible_moves.pop(0)
            self.board[move[0]][move[1]] = Constants.O_SLOT if self.opponent_start else Constants.X_SLOT
            
            ret_eval = self.get_perfect_move_helper(possible_moves, False)

            print("{}eval = {}, popped : {}, remaining : {}".format("  " * (9 - num_of_moves), ret_eval, move, possible_moves))
            
            self.board[move[0]][move[1]] = Constants.EMPTY_SLOT
            possible_moves.append(move)            

            if ret_eval >= curr_best_eval:
                curr_best_move = move
                curr_best_eval = ret_eval

        self.board = pre_board

        print("perfect move = {}, eval = {}".format(move, curr_best_eval))

        return curr_best_move


    # Bot move. perfect move is done with probability of self.difficulty/100, otherwise random available move
    def calculate_move(self):
        if random.randint(1, 100) > self.difficulty:
            return self.get_random_available_move()
        return self.get_perfect_move()

    def _check_valid_square(self, row, col):
        return not (                        \
            row >= len(self.board) or       \
            col >= len(self.board[0]) or    \
            row < 0 or                      \
            col < 0 or                      \
            self.board[row][col] != Constants.EMPTY_SLOT \
        )

    def undo_move(self):
        assert self.state != State.GAME_OVER and self.state != State.PRE_START, "Undo should not be allowed in this state. state = {}".format(self.state)
        assert self.last_moves, "No turns to undo, TicTacToeGame should have checked that with has_undo"
        assert len(self.last_moves) > 1, "Has to undo 2 moves ( 1 for player 1 for bot )"

        bot_last_move = self.last_moves.pop()
        player_last_move = self.last_moves.pop()

        self.board[bot_last_move[0]][bot_last_move[1]] = Constants.EMPTY_SLOT
        self.board[player_last_move[0]][player_last_move[1]] = Constants.EMPTY_SLOT
        

    # Return true if move was made, otherwise return false ( if move was illegal )
    def do_player_move(self, row, col):
        assert self.state != State.GAME_OVER, "TicTacToeGame should have prevented a move when game is over"

        if not self._check_valid_square(row, col):
            return False
        
        self.board[row][col] = Constants.X_SLOT if self.opponent_start else Constants.O_SLOT
        self.last_moves.append([row, col])
        
        [game_over, game_res] = self.check_game_over()
        if game_over:
            self.state = State.GAME_OVER
            self.game_res = game_res
            return True

        # Computer immediently makes a move if game is not over, might need to change it if we want to do it seperately
        # for instance in a case where the game wants to send a board after player move and then another board after computer move.
        # Update : Haha, above comment was spot on, almost everyone got confused at first because of that
        # still, because it takes too long to write the message, i dont want to make it any longer
        self.do_self_move()
        return True

    # cool way to check game over and who won : each one of the 8 winning lines is representred by 10**x, 0<=x<=7
    # int sum -> string. if digit 3 in string -> win
    # if game won, return True and game result, otherwise False and None
    def check_game_over(self):
        SLOT_TO_VAL = {
            Constants.EMPTY_SLOT: 0,
            Constants.O_SLOT : 0,
            Constants.X_SLOT : 0,
        }
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                slot = self.board[row][col]
                SLOT_TO_VAL[slot] = SLOT_TO_VAL[slot] + Constants.DIGIT_BOARD[row][col]
        
        if "3" in str(SLOT_TO_VAL[Constants.O_SLOT]):
            game_res = GameResult.COMPUTER_WON if self.opponent_start else GameResult.PLAYER_WON
            return [True, game_res]
        
        if "3" in str(SLOT_TO_VAL[Constants.X_SLOT]):        
            game_res = GameResult.PLAYER_WON if self.opponent_start else GameResult.COMPUTER_WON
            return [True, game_res]

        if SLOT_TO_VAL[Constants.EMPTY_SLOT] == 0:
            game_res = GameResult.TIE
            return [True, game_res]

        return [False, None]

    def set_difficulty(self, diff):
        assert diff <= 100, "difficulty should be less than or equal to 100"
        self.difficulty = diff

    def get_difficulty(self):
        return self.difficulty

    def get_state(self):
        return self.state

    def get_game_result(self):
        return self.game_res

    def is_opponent_started(self):
        return self.opponent_start

    def has_undo(self):
        return self.last_moves is not None and len(self.last_moves) > 1

    def get_board(self):
        return [x[:] for x in self.board]

    


# Responsible for interpreting the moves/commands, responding with proper text, interacting with engine etc...
class TicTacToeGame:

    def __init__(self):
        self.should_quit = False
        self.bot_score = 0     # Player wins
        self.player_score = 0
        self.difficulty = 30
        self.previous_state = None

    def handle_cmd_recv_resp(self, cmd):
        assert self.should_quit != True, "Should not run commands after quitting"

        cmd = cmd.lower()

        if self.engine.get_state() == State.PRE_START:
            return self.handle_pre_start_cmd(cmd)

        if self.engine.get_state() == State.PLAYER_MOVE:
            return self.handle_player_move_cmd(cmd)

        if self.engine.get_state() == State.GAME_OVER:
            return self.handle_game_over_cmd(cmd)

    def handle_pre_start_cmd(self, cmd):
        if cmd == "x":
            self.engine.start(opponent_start=True)
            return self.get_score_status_str() + "Game Started - Your turn\n" + self.board_to_string() + self.get_player_move_state_commands()
        elif cmd == "o":
            self.engine.start(opponent_start=False)
            return self.get_score_status_str() + "Game Started - Bot made move\n" + self.board_to_string() + self.get_player_move_state_commands()
        elif cmd == "quit":
            return self.quit()
        
        cmd = cmd.split(" ")
        if len(cmd) == 2 and cmd[0] == "set-difficulty":
            return self.set_difficulty_and_response(cmd[1]) + self.get_pre_game_state_commands()

        return "Invalid Command, try again :\n " + self.get_pre_game_state_commands()
                

    def handle_player_move_cmd(self, cmd):
        if cmd == "quit":
            return self.quit()      

        elif cmd == "restart":
            self.engine.restart()
            start_info_str = "Bot made a move" if self.engine.is_opponent_started() else "Your turn"
            return self.get_score_status_str() + "Restarted Game " + start_info_str + "\n" + self.board_to_string() + self.get_player_move_state_commands()

        elif cmd == "undo":
            if self.engine.has_undo():
                self.engine.undo_move()
                return self.get_score_status_str() + "Undid last move :\n" + self.board_to_string() + self.get_player_move_state_commands()
            return "You.Can't.Do.That.\n" + self.get_player_move_state_commands()

        cmd = cmd.split(" ")
        if len(cmd) == 2 and cmd[0].isdigit() and cmd[1].isdigit():
            move_completed = self.engine.do_player_move(int(cmd[0])-1, int(cmd[1])-1)
            if move_completed:
                return self.move_completed_update_and_response()

        return self.get_player_move_state_commands() + "Invalid Move (make sure cell is empty and row and col are within boundries), try again :\n" + self.board_to_string() + self.get_player_move_state_commands()
    
    def handle_game_over_cmd(self, cmd):
        if cmd == "restart":
            self.engine.restart()
            start_info_str = "Bot made a move" if self.engine.is_opponent_started() else "Your turn"
            return "Restarted Game " + start_info_str + "\n" + self.board_to_string() + self.get_player_move_state_commands()
        elif cmd == "quit":
            return self.quit()
        
        cmd = cmd.split(" ")
        if len(cmd) == 2 and cmd[0] == "set-difficulty":
            return self.set_difficulty_and_response(cmd[1]) + self.get_game_over_state_commands()

        return "Invalid Command, try again :\n " + self.get_game_over_state_commands() 


    def move_completed_update_and_response(self):
        if self.engine.get_state() == State.PLAYER_MOVE:
            return self.get_score_status_str() + "You and the bot made a move\n" + self.board_to_string() + self.get_player_move_state_commands()

        assert self.engine.get_state() == State.GAME_OVER, "Game has to be over in this case, cant be pre start"
        assert self.engine.get_game_result() != GameResult.NOT_FINISHED, "Result has to be in after game finished"

        if self.engine.get_game_result() == GameResult.PLAYER_WON:
            self.player_score = self.player_score + 1
            return self.get_score_status_str() + "You Won! Congratulations!\n" + self.board_to_string() + self.get_game_over_state_commands()

        if self.engine.get_game_result() == GameResult.COMPUTER_WON:
            self.bot_score = self.bot_score + 1
            return self.get_score_status_str() + "You Lost :( Better luck next time!\n" + self.board_to_string() + self.get_game_over_state_commands()

        if self.engine.get_game_result() == GameResult.TIE:
            self.player_score = self.player_score + 0.5
            self.bot_score = self.bot_score + 0.5
            return self.get_score_status_str() + "It's a tie ! so close...\n" + self.board_to_string() + self.get_game_over_state_commands()

    def set_difficulty_and_response(self, difficulty):
        if difficulty == "easy":
            self.engine.set_difficulty(Difficulty.EASY)
        elif difficulty == "hard":
            self.engine.set_difficulty(Difficulty.HARD)
        elif difficulty == "impossible":
            self.engine.set_difficulty(Difficulty.IMPOSSIBLE)
        else:
            return "Invalid difficulty value : '{}'. Has to be easy/hard/impossible\n".format(difficulty)
    
        return "Set difficulty to '{}'.\n".format(difficulty)

    def start(self):
        self.engine = TicTacToeEngine()
        return self.get_pre_game_state_commands()

    def quit(self):
        self.should_quit = True
        return "Quitting the game..."

    def get_should_quit(self):
        return self.should_quit

    def get_score_status_str(self):
        return "-- You : {}     Bot : {} --\n".format(self.player_score, self.bot_score)

    def get_pre_game_state_commands(self):
        diff_str = Difficulty.DIFF_TO_STR[self.engine.get_difficulty()]
        
        return "What do you want to do ?\n" +\
            "[X] to start as X\n" +\
            "[O] to play as O\n" +\
            "[set-difficulty X] Set difficulty to X [easy/hard/impossible] (curr = {})\n".format(diff_str) +\
            "[quit] to quit the game\n"
        
    def get_player_move_state_commands(self):
        undo_str = "[undo] To undo last move\n" if self.engine.has_undo() else ""
        return "What do you want to do ?\n" +\
            "[<row> <col>] to mark row <row> and column <col> (1<=row,col<=3)\n" +\
            undo_str +\
            "[restart] to start a new game\n" +\
            "[quit] to quit the game\n"

    def get_game_over_state_commands(self):
        diff_str = Difficulty.DIFF_TO_STR[self.engine.get_difficulty()]

        return "What do you want to do ?\n" +\
            "[restart] to start a new game\n" +\
            "[set-difficulty X] Set difficulty to X [easy/hard/impossible] (curr = {})\n".format(diff_str) +\
            "[quit] to quit the game\n"

    def board_to_string(self):
        SLOT_TO_STR = {
            Constants.EMPTY_SLOT: "     ",
            Constants.O_SLOT : "⭕",        # This is for whatapp output
            Constants.X_SLOT : "✖️",        # This is for whatapp output
            #Constants.O_SLOT : "  O  ",     # This is for console testing 
            #Constants.X_SLOT : "  X  ",     # This is for console testing
        }

        board = self.engine.get_board()

        ret_str = ""

        first_row = True
        for row in board:
            # Draw line seperations above non first rows
            if not first_row:
                ret_str = ret_str + "-" * 12 + "\n"

            # Draw the row itself
            first_slot = True
            for slot in row:
                # Draw slot seperations before non first slots
                if not first_slot:
                    ret_str = ret_str + "|"\

                ret_str = ret_str + SLOT_TO_STR[slot]
                first_slot = False
            
            ret_str = ret_str + "\n"
            first_row = False

        return ret_str
