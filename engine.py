from stockfish import Stockfish


class Engine(Stockfish):
    def __init__(self, path="Stockfish\\Stockfish_14.exe", depth=15):
        Stockfish.__init__(self, path)

        self.set_depth(depth)

    def get_worst_moves(self) -> dict:
        top_moves = self.get_top_moves(141)

        if len(top_moves) == 0:
            raise AttributeError("Invalid position")

        elif len(top_moves) == 1:
            return {"status": -1}

        else:
            return {"status": 1, "worst": top_moves[-1], "second-worst": top_moves[-2]}

    def get_worst_difference(self, worst_moves=None) -> dict:
        if worst_moves is None:
            worst_moves = self.get_worst_moves()

        if worst_moves["status"] == 1:
            if worst_moves["worst"]["Mate"] is None:
                assert worst_moves["second-worst"]["Mate"] is None
                return {"status": 1,
                        "cp": abs(worst_moves["second-worst"]["Centipawn"] - worst_moves["worst"]["Centipawn"]),
                        "mate": None}

            else:
                if worst_moves["second-worst"]["Mate"] is None:
                    return {"status": 1, "cp": None, "mate": True}

                else:
                    return {"status": 1, "cp": None, "mate": False}

        else:
            return {"status": -1, "cp": None, "mate": None}

    def get_difference_significant(self, worst_moves=None) -> bool:
        worst_difference = self.get_worst_difference(worst_moves)

        if worst_difference["status"] == -1:
            return False

        if worst_difference["cp"]:
            return worst_difference["cp"] > 200

        return worst_difference["mate"]


if __name__ == "__main__":
    engine = Engine("Stockfish\\Stockfish_14.exe")

    COMMANDS = {"get worst": lambda: print(engine.get_worst_moves()),
                "get worst difference": lambda: print(engine.get_worst_difference()),
                "get significant": lambda: print(engine.get_difference_significant()),
                "visual": lambda: print(engine.get_board_visual()),
                "position startpos": engine.set_position,
                "get best": lambda: print(engine.get_best_move()),
                "fen": lambda: print(engine.get_fen_position()),
                "exit": exit}

    SETTER = {"depth": lambda depth: engine.set_depth(int(depth)),
              "fen": lambda fen: engine.set_fen_position(fen), }

    while True:
        try:
            command = input(">>> ")

            if command.split()[0] == "set":
                if command.split(" ")[1].split(":")[0] in SETTER:
                    SETTER[command.split()[1].split(":")[0]](command.split(":")[1])

                else:
                    print("[Error]: This setter does not exist")

            elif command in COMMANDS:
                COMMANDS[command]()

            else:
                try:
                    res = eval(command)
                    if res is not None:
                        print(f"\033[93m{res}\033[0m")

                except SyntaxError:
                    exec(command)

        except Exception as e:
            print(f"[Error]: {e}")
