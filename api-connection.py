from lichess.format import PGN
from engine import *
from datetime import datetime
import chess.pgn
import lichess.api

ENDLINE = "\033[0m"
PERCENTAGE = "\033[93m"
PURPLE = "\033[95m"


class GameLoader:
    def get_next_game(self):
        counter = 0
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
            print(f"[Move {move}]: ", end="")
            engine.set_fen_position(list_fen[move])
            engine.set_depth(15)
            worst_moves = engine.get_worst_moves()
            significant = engine.get_difference_significant(worst_moves)

            if not significant:
                print("Unsuccessful (Depth: 15)")

            else:
                print(f"{PURPLE}Successful{ENDLINE} (Depth: 15) \t", end="")
                engine.set_depth(20)
                engine.set_fen_position(list_fen[move])
                worst_moves = engine.get_worst_moves()
                significant = engine.get_difference_significant(worst_moves)

                if not significant:
                    print("Unsuccessful (Depth: 20)")

                else:
                    print(f"{PURPLE}Successful{ENDLINE} (Depth: 20)")
                    counter += 1

                    with open("result.txt") as file:
                        zeilen = file.read()

                    with open("result.txt", "w") as file:
                        file.write(zeilen)
                        file.write(f"{move};{url};{list_fen[move]};{worst_moves}\n")

        return counter

    def search_games(self, start, end):
        counter = 0

        for i in range(start, end):
            print()
            print()
            print("==========================================================================")
            print(f"Searching in Game #{i + 1}\t\t (Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")
            print("==========================================================================")
            print()
            print()
            counter += self.get_next_game()

        print(f"\nFinished with {PERCENTAGE}{counter}{ENDLINE} hits")

    def __init__(self, user):
        self.user = user
        self.user_api = lichess.api.user(user)
        self.games_played = self.user_api["count"]["all"]

        print(f"{self.games_played} games are loading: \t", end="")
        self.games = lichess.api.user_games(user, max=self.games_played, format=PGN)
        print(PERCENTAGE + "100%" + ENDLINE)


print("Connecting to Stockfish: \t", end="")
engine = Engine()
print(PERCENTAGE + "100%" + ENDLINE)
loader = GameLoader("drnykterstein")
loader.search_games(0, 1)
