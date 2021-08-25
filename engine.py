from stockfish import Stockfish


class Engine(Stockfish):
    def __init__(self, path, depth=15):
        Stockfish.__init__(self, path)

        self.set_depth(depth)

    def get_worst_moves(self):
        top_moves = self.get_top_moves(141)

        if len(top_moves) == 0:
            raise AttributeError("Invalid position")

        elif len(top_moves) == 1:
            return {"status": -1}

        else:
            return {"status": 1, "worst": top_moves[-1], "second-worst": top_moves[-2]}


if __name__ == "__main__":
    engine = Engine("Stockfish\\Stockfish_14.exe")

    COMMANDS = {"get worst": lambda: print(engine.get_worst_moves()),
                "visual": lambda: print(engine.get_board_visual()),
                "position startpos": engine.set_position,
                "get best": lambda: print(engine.get_best_move()),
                "fen": lambda: print(engine.get_fen_position())}

    SETTER = {"depth": lambda depth: engine.set_depth(int(depth)),
              "fen": lambda fen: engine.set_fen_position(fen), }

    while True:
        try:
            command = input(">>> ")

            if command.split()[0] == "set":
                if command.split(" ")[1].split(":")[0] in SETTER:
                    SETTER[command.split()[1].split(":")[0]](command.split(":")[1])
                    print("Value:", command.split(":")[1])

                else:
                    print("[Error]: This setter does not exist")

            elif command in COMMANDS:
                COMMANDS[command]()

            else:
                exec(command)

        except Exception as e:
            print(f"[Error]: {e}")