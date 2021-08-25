import lichess.api
from lichess.format import PGN
import chess.pgn
from engine import *


class GameLoader:
    def convert_to_fen(self):
        list_fen = []
        pgn_file = open("storage.pgn")

        game = chess.pgn.read_game(pgn_file)
        board = game.board()
        list_fen.append(board.fen())

        for move in game.mainline_moves():
            board.push(move)
            list_fen.append(board.fen())

        return list_fen

    def get_next_game(self):
        pgn = next(self.games)

        with open("storage.pgn", "w") as file:
            file.write(pgn)

        return self.convert_to_fen()

    def __init__(self, user):
        self.user = user
        self.user_api = lichess.api.user(user)
        self.games_played = self.user_api["count"]["all"]
        self.games = lichess.api.user_games(user, max=self.games_played, format=PGN)


loader = GameLoader("DrNykterstein")
print(loader.get_next_game())
