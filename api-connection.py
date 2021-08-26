import lichess.api
from lichess.format import PGN
import chess.pgn
from engine import *


class GameLoader:
    def get_next_game(self):
        pgn = next(self.games)

        with open("storage.pgn", "w") as file:
            file.write(pgn)

        pgn_file = open("storage.pgn")
        game = chess.pgn.read_game(pgn_file)
        board = game.board()
        url = game.headers["Site"]
        list_fen = [board.fen()]

        for move in game.mainline_moves():
            board.push(move)
            list_fen.append(board.fen())

        for move in range(len(list_fen)):
            print(f"Move {move}: ", end="")
            engine.set_fen_position(list_fen[move])
            value = engine.get_difference_significant()
            print("100%")

    def search_games(self, start, end):
        for i in range(start, end):
            print()
            print()
            print("===================================================")
            print(f"Game #{i + 1} is being searched")
            print("===================================================")
            print()
            print()
            self.get_next_game()

    def __init__(self, user):
        self.user = user
        self.user_api = lichess.api.user(user)
        self.games_played = self.user_api["count"]["all"]

        print(f"{self.games_played} games are loading: ", end="")
        self.games = lichess.api.user_games(user, max=self.games_played, format=PGN)
        print("100%")


engine = Engine()
loader = GameLoader("drnykterstein")
loader.search_games(0, 9)
