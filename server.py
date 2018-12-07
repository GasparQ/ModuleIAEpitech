import sys
from game import OperaGame
from threading import Thread
import getopt


class Server:
    def __init__(self, server_id: int):
        """
        Create a server with id as parameter
        :param server_id:
        """
        self.server_id = server_id
        self.game = None

    def start(self, batches: int) -> None:
        """
        Start a game server for N batches
        :param batches: Number of batches
        """
        game = OperaGame(self.server_id)
        port = game.init_server()
        thread = Thread(target=game.run, args=(batches,))
        thread.start()
        print("PORT:" + str(port))
        thread.join()
        print("END SERVER")


def parse_args(argv: []) -> (int, int):
    """
    Parse command arguments
    -b Number of batches
    -i server id
    :param argv: list of arguments
    :return: (batches, index)
    """
    my_opts, args = getopt.getopt(argv[1:], "b:i:")

    batches = 1
    index = 0
    for o, a in my_opts:
        if o == '-b':
            batches = int(a)
        elif o == '-i':
            index = int(a)
        else:
            print("Usage: %s -b batches -i server id" % sys.argv[0])
    return batches, index


def main(argv: []) -> int:
    """
    Create, and start a new server
    :param argv: list of arguments
    :return: Return 0 if no error
    """
    batches, index = parse_args(argv)
    server = Server(index)
    server.start(batches)
    return 0


if __name__ == "__main__":
    main(sys.argv)
