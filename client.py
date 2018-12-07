import sys
import getopt
import socket
import importlib.util
import inspect


class Client:
    def __init__(self, port: int, ia_file: str, is_ghost: bool, server_id: int):
        """
        Create a new client which load ia_file at runtime, define if ia is ghost or not
        :param port: server port
        :param ia_file: ia file path
        :param is_ghost: ia is a ghost or not
        :param server_id: server id
        """
        self.server_id = server_id
        self.port = port
        self.ia_file = ia_file
        self.sock = None
        self.server_address = None
        self.is_ghost = is_ghost
        ai = self.load_ia_from_file()
        print('AI:', ai)
        if ai is not None:
            self.ai = ai(self.server_id, 1 if self.is_ghost else 0)
        else:
            self.ai = None

    def load_ia_from_file(self):
        """
        Load AI from a path file
        :return: Return AI type or None if ai doesn't exist
        """
        spec = importlib.util.spec_from_file_location("client_ai", self.ia_file)
        module_ia = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_ia)
        sys.modules["client_ai"] = module_ia
        cls_members = inspect.getmembers(sys.modules["client_ai"], inspect.isclass)

        tmp = self.ia_file.split("/")
        name = tmp[len(tmp) - 1].split(".")[0]
        ai = None
        i = 0
        for m in cls_members:
            if str(m[0]).lower() == name:
                ai = getattr(module_ia, cls_members[i][0])
            i += 1
        return ai

    def connect(self):
        """
        Connect tcp client to the server with self.port
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', self.port)
        try:
            self.sock.connect(self.server_address)
        except Exception as e:
            print("something's wrong with %s:%d. Exception is %s" % ('localhost', self.port, e))
            self.sock.close()

        self.send("CONNECT:" + ("1" if self.is_ghost else "0"))

    def send(self, message: str) -> None:
        self.sock.sendall(str.encode(message))

    def play(self):
        raise NotImplementedError('Mathod play is not implemented')

    def run(self) -> None:
        """
        Run the client until server quit the connection
        """
        running = True
        while running:
            try:
                data = self.sock.recv(128)
            except ConnectionResetError:
                self.ai.update_state()
                self.sock.close()
                self.ai.close()
                running = False
            else:
                str_data = data.decode("utf-8")
                if str_data != "":
                    if str_data. rstrip() == "RESET":
                        self.ai.end()
                        self.ai.reset()
                    elif str_data.rstrip() == "REINFORCE":
                        self.ai.replay_from_file()
                    else:
                        data = self.ai.__play__(str_data)
                        self.sock.sendall(data.encode())
                else:
                    self.ai.update_state()
                    self.sock.close()
                    self.ai.close()
                    running = False
        self.ai.end()
        print("END")


def parse_args(argv: []) -> (int, str, bool, int):
    """
    Parse command arguments
    -p port
    -f ia file
    -g is ghost
    -s server id
    :param argv: list of arguments
    :return: (port, ia file, is ghost, server id)
    """
    my_opts, args = getopt.getopt(argv[1:], "p:f:g:s:")

    port = 0
    file = ""
    is_ghost = False
    server_id = 0
    for o, a in my_opts:
        if o == '-p':
            port = int(a)
        elif o == '-f':
            file = a
        elif o == "-g":
            is_ghost = a == "True"
        elif o == "-s":
            server_id = int(a)
        else:
            print("Usage: %s -p port -f ia.py" % sys.argv[0])
    # print("IA file : %s " % file)
    return port, file, is_ghost, server_id


def main(argv: []) -> int:
    """
    Create, connect to server and run a AI client
    :param argv: command arguments
    :return: Return 0 if no error
    """
    port, file, is_ghost, server_id = parse_args(argv)
    print(port, file, is_ghost, server_id)
    client = Client(port, file, is_ghost, server_id)
    client.connect()
    client.run()
    return 0


if __name__ == "__main__":
    main(sys.argv)
