import sys
import getopt
import concurrent.futures
import subprocess
import os

verbose = False


def start_server(index: int, detective: str, ghost: str, batches: int) -> int:
    """
    Start a server with detective and ghost script for N batches
    :param index: server id
    :param detective: detective script
    :param ghost: ghost script
    :param batches: number of batches
    :return: Return 0 for no error
    """
    global verbose
    running, clients, stats = True, None, False

    print("=================== SERVER ({}) REMAINING BATCHES {} ===================".format(index, batches))
    server = subprocess.Popen(["py", "./server.py", "-i", str(index), "-b", str(batches)],
                              shell=True, stdout=subprocess.PIPE)
    while running:
        line = server.stdout.readline()
        if line != '':
            str_line = line.rstrip().decode("utf-8")
            if (verbose and not str_line.startswith("PERCENT") and not str_line.startswith("STATS")) or stats:
                print("  ", str_line)
            elif not verbose and str_line.startswith("PERCENT:"):
                p = int(str_line.split(":")[1])
                print("Batches {}/{} = {}%".format(p, batches, round((p / batches) * 100, 2)))
            if str_line.startswith("PORT:"):
                port = int(str_line[5:])
                executor, clients = start_clients(port, detective, ghost, index)
            elif str_line == "STATS":
                stats = not stats
            elif str_line == "END SERVER":
                running = False
                server.communicate()
    for client in concurrent.futures.as_completed(clients):
        s = clients[client]
        try:
            data = client.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (s, exc))
        else:
            return data
    return 0


def start_client(index: int, port: int, detective: str, ghost: str, server_id: int) -> int:
    """
    Start and connect a client to server port
    If the index == 0, the client is started with the ghost script
    Otherwise, the client is started with the detective script
    :param index: 0 if ghost otherwise start as detective
    :param port: server port
    :param detective: detective script
    :param ghost: ghost script
    :param server_id: server_id
    :return: Return 0 if not error
    """
    global verbose
    if index == 0:
        client = subprocess.Popen(["py", "./client.py", "-p", str(port), "-f", ghost, "-g", "True",
                                   "-s", str(server_id)], shell=True, stdout=subprocess.PIPE)
    else:
        client = subprocess.Popen(["py", "./client.py", "-p", str(port), "-f", detective, "-g", "False",
                                   "-s", str(server_id)], shell=True, stdout=subprocess.PIPE)
    running = True
    while running:
        line = client.stdout.readline()
        if line != "":
            str_line = line.rstrip().decode("utf-8")
            if str_line == "END":
                running = False
            elif verbose:
                if index == 0:
                    print("    Ghost :", str_line)
                else:
                    print("    Detective :", str_line)
    return 0


def start_clients(port: int, detective: str, ghost: str, server_id: int) -> (concurrent.futures.Executor, []):
    """
    Start two clients with detective and ghost script
    :param port: server port
    :param detective: detective script
    :param ghost: ghost script
    :param server_id: server id
    :return:
    """
    n_client = 2
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_client)
    clients = {executor.submit(start_client, i, port, detective, ghost, server_id): i for i in range(n_client)}
    return executor, clients


def parse_args(argv: []) -> (int, str, str, int):
    """
        Parse command arguments
        -n number of servers
        -d detective script
        -g ghost script
        -v verbose mode
        -b number of batches per server
    """
    global verbose
    my_opts, args = getopt.getopt(argv[1:], "d:g:n:v:b:")

    detective = ""
    ghost = ""
    num_game = 0
    batches = 1
    for o, a in my_opts:
        if o == '-n':
            num_game = int(a)
        elif o == '-d':
            detective = a
        elif o == "-g":
            ghost = a
        elif o == "-v":
            verbose = a == "True"
        elif o == '-b':
            batches = int(a)
        else:
            usage = "Usage: {}".format(sys.argv[0]) +\
                    " -n number_of_server -g ghost.py -d detective.py -v verbose -b batches_by_server"
            print(usage)
    print("Detective file : %s and Ghost file: %s" % (detective, ghost))
    return num_game, detective, ghost, batches


def init_dirs():
    """
        Create missing directory for future games
    """
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    if not os.path.exists("./memories"):
        os.makedirs("./memories")
    if not os.path.exists("./states"):
        os.makedirs("./states")
    if not os.path.exists("./weights"):
        os.makedirs("./weights")


def main(argv):
    """
    Start servers with a thread pool
    :param argv: command arguments
    :return: Return 0 if no error
    """
    num_game, detective, ghost, batches = parse_args(argv)
    init_dirs()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_game) as executor:
        servers = {executor.submit(start_server, i, detective, ghost, batches): i for i in range(num_game)}
        for server in concurrent.futures.as_completed(servers):
            s = servers[server]
            try:
                data = server.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (s, exc))
            else:
                return data


if __name__ == "__main__":
    main(sys.argv)
