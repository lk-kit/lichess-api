from stockfish import Stockfish


class Engine(Stockfish):
    def __init__(self, path, depth=10):
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

    while True:
        try:
            command = input(">>> ")

            exec(input(">>> "))

        except Exception as e:
            print(f"[Error]: {e}")
