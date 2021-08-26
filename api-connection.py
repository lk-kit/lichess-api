from lichess.format import PGN
from engine import *
from datetime import datetime
import chess.pgn
import lichess.api
from time import time

ENDLINE = "\033[0m"
PERCENTAGE = "\033[93m"
PURPLE = "\033[95m"

first = 12
second = 20
time_first = [0, 0]
time_second = [0, 0]


class GameLoader:
    def get_next_game(self):
        global time_first, time_second

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
            print(f"[Move {move + 1}/{len(list_fen)}]: ", end="")
            engine.set_fen_position(list_fen[move])
            engine.set_depth(first)

            begin = time()
            worst_moves = engine.get_worst_moves()
            time_first[0] += time() - begin
            time_first[1] += 1

            significant = engine.get_difference_significant(worst_moves)

            if not significant:
                print(f"Unsuccessful (Depth: {first})")

            else:
                print(f"{PURPLE}Successful{ENDLINE} (Depth: {first}) \t", end="")
                engine.set_depth(second)
                engine.set_fen_position(list_fen[move])

                begin = time()
                worst_moves = engine.get_worst_moves()
                time_second[0] += time() - begin
                time_second[1] += 1

                significant = engine.get_difference_significant(worst_moves)

                if not significant:
                    print(f"Unsuccessful (Depth: {second})")

                else:
                    print(f"{PURPLE}Successful{ENDLINE} (Depth: {second})")
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
            print("\n\n==========================================================================")
            print(f"Searching in Game #{i + 1}\t\t (Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")
            print("==========================================================================\n\n")
            counter += self.get_next_game()

        print("\n\n\n==========================================================================")
        print(f"Finished\t\t (Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")
        print("==========================================================================\n")
        print(f"Hits: {PERCENTAGE}{counter}{ENDLINE}")
        print(f"Games searched: {PERCENTAGE}{end - start}{ENDLINE}")
        try:
            print(f"Average time on first search: {PERCENTAGE}{time_first[0] / time_first[1]}{ENDLINE} seconds")
            print(f"Average time on second search: {PERCENTAGE}{time_first[0] / time_first[1]}{ENDLINE} seconds")

        except ZeroDivisionError:
            print(f"Average time on first search: {PERCENTAGE}{0}{ENDLINE} seconds")
            print(f"Average time on second search: {PERCENTAGE}{0}{ENDLINE} seconds")

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
