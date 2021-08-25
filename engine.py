from stockfish import Stockfish
import os.path


class Engine(Stockfish):
    def __init__(self, path):
        Stockfish.__init__(self, path)


if __name__ == "__main__":
    engine = Engine("Stockfish\\Stockfish_14.exe")

    while True:
        try:
            exec(input(">>> "))

        except Exception as e:
            print(f"[Error]: {e}")
