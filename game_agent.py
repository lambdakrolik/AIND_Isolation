"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import isolation.isolation


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """


    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        bestmove = (0,0)
        bestmovevalue = float("-inf")

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if len(legal_moves) == 0:
            bestmove = (-1, -1)
            return bestmove

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            current_depth = 1
            depth_limit = float("inf")
            if self.iterative is False:
                depth_limit = 1

            while current_depth <= depth_limit:
                if self.method is 'minimax':
                    print("Iterative deepening: depth ", current_depth)
                    (bestmovevalue, bestmove) = self.minimax(game, current_depth, True)
                elif self.method is 'alphabeta':
                    (bestmovevalue, bestmove) = self.alphabeta(game, current_depth, True)
                current_depth = current_depth + 1
            pass

        except Timeout:
            # Handle any actions required at timeout, if necessary
            print("Best Move IN TIMEOUT ", bestmove)
            return bestmove
            pass

        # Return the best move from the last completed search iteration
        print ("Best Move ", bestmove)
        return bestmove

    def mingame(self, game, depth_limit, current_level):
        if self.time_left() < self.TIMER_THRESHOLD:
            print("MINGAME timed out at depth ", current_level)
            raise Timeout()

        movesavailable = game.get_legal_moves()
        leadingmovevalue = float("inf")
        print("MOVES AT MINGAME", movesavailable, "CURRENT LEVEL ", current_level, " FOR DEPTH ", depth_limit)
        if (depth_limit - current_level) > 0:
            for m in movesavailable:
                # Evaluate each move for its value
                move_board = game.forecast_move(m)
                board_score = self.maxgame(move_board, depth_limit, current_level + 1)
                if board_score < leadingmovevalue:
                    leadingmovevalue = board_score
        else:
            for m in movesavailable:
                if self.time_left() < self.TIMER_THRESHOLD:
                    print("MAXGAME timed out at depth ", current_level)
                    raise Timeout()
                current_score = self.score(game, game.inactive_player)
                if current_score < leadingmovevalue:
                    leadingmovevalue = current_score
        print("New best move from min: ", leadingmovevalue)
        return leadingmovevalue

    def maxgame(self, game, depth_limit, current_level):
        if self.time_left() < self.TIMER_THRESHOLD:
            print("MAXGAME timed out at depth ", current_level)
            raise Timeout()

        movesavailable = game.get_legal_moves()
        leadingmovevalue = float("-inf")
        print("MOVES AT MAXGAME", movesavailable, "ITER REMAINING ", current_level)
        if (depth_limit - current_level) > 0:
            for m in movesavailable:
                # Evaluate each move for its value
                move_board = game.forecast_move(m)
                board_score = self.mingame(move_board, depth_limit, current_level + 1)
                if board_score > leadingmovevalue:
                    leadingmovevalue = board_score
        else:
            for m in movesavailable:
                if self.time_left() < self.TIMER_THRESHOLD:
                    print("MAXGAME timed out at depth ", current_level)
                    raise Timeout()
                current_score = self.score(game, game.active_player)
                if current_score > leadingmovevalue:
                    leadingmovevalue = current_score

        print("New best move from max: ", leadingmovevalue)
        return leadingmovevalue

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            print("MINIMAX timed out at depth ", depth)
            raise Timeout()

        #Find all available legal moves
        movesavailable=game.get_legal_moves()
        leadingmove = (-1, -1)
        leadingmovevalue = float("-inf")

        #print("MOVES ", movesavailable, " at depth ", depth)

        #If we need to go beyond one, call the minmax recursion
        if depth == 1:
            for m in movesavailable:
                move_board = game.forecast_move(m)
                if self.score(move_board, game.active_player) > leadingmovevalue:
                    leadingmovevalue = self.score(move_board, game.active_player)
                    leadingmove = m
        else:
            for m in movesavailable:
                move_board = game.forecast_move(m)
                board_score = self.mingame(move_board, depth, 1)
                if board_score > leadingmovevalue:
                    leadingmove = m
                    leadingmovevalue = board_score

        print ("BEST MOVE IS ", leadingmove, " WITH VALUE ", leadingmovevalue)
        return leadingmovevalue, leadingmove


    def alphabeta_mingame(self, game, depth_limit, current_level, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        movesavailable = game.get_legal_moves()
        leadingmovevalue = float("inf")
        leadingmove = (-1, -1)
        if (depth_limit - current_level) > 0:
            for m in movesavailable:
                # Evaluate each move for its value
                move_board = game.forecast_move(m)
                move_x, board_score = self.alphabeta_maxgame(move_board, depth_limit, current_level + 1, alpha, beta)
                if board_score < leadingmovevalue:
                    leadingmovevalue = board_score
                    leadingmove = m
                if leadingmovevalue <= alpha:
                    return m, leadingmovevalue
                if leadingmovevalue < beta:
                    beta = leadingmovevalue
        else:
            for m in movesavailable:
                if self.score(game, game.inactive_player) < leadingmovevalue:
                    leadingmovevalue = self.score(game, game.inactive_player)
                    leadingmove = m
        return leadingmove, leadingmovevalue

    def alphabeta_maxgame(self, game, depth_limit, current_level, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        movesavailable = game.get_legal_moves()
        leadingmovevalue = float("-inf")
        leadingmove = (-1, -1)
        if (depth_limit - current_level) > 0:
            for m in movesavailable:
                # Evaluate each move for its value
                move_board = game.forecast_move(m)
                move_x, board_score = self.alphabeta_mingame(move_board, depth_limit, current_level + 1, alpha, beta)
                if board_score > leadingmovevalue:
                    leadingmovevalue = board_score
                    leadingmove = m
                if leadingmovevalue >= beta:
                        return m, leadingmovevalue
                if leadingmovevalue > alpha:
                    alpha = leadingmovevalue
        else:
            for m in movesavailable:
                if self.score(game, game.active_player) > leadingmovevalue:
                    leadingmove = m
                    leadingmovevalue = self.score(game, game.active_player)

        return leadingmove, leadingmovevalue

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        #Find all available legal moves
        movesavailable=game.get_legal_moves()
        leadingmove = (-1, -1)
        leadingmovevalue = float("-inf")

        #If we need to go beyond one, call the minmax recursion
        if depth == 1:
            for m in movesavailable:
                move_board = game.forecast_move(m)
                if self.score(move_board, game.active_player) > leadingmovevalue:
                    leadingmovevalue = self.score(move_board, game.active_player)
                    leadingmove = m
        else:
            leadingmove, leadingmovevalue = self.alphabeta_maxgame(game, depth, 0, float("-inf"), float("inf"))

        return leadingmovevalue, leadingmove