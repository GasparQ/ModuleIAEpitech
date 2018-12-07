import socket
import codecs
from random import shuffle
from random import randrange
import time

permanents, both, before, after = {'rose'}, {'rouge', 'gris', 'bleu'}, {'violet', 'marron'}, {'noir', 'blanc'}
colors = before | permanents | after | both
passages = [{1, 4}, {0, 2}, {1, 3}, {2, 7}, {0, 5, 8}, {4, 6}, {5, 7}, {3, 6, 9}, {4, 9}, {7, 8}]
pass_ext = [{1, 4}, {0, 2, 5, 7}, {1, 3, 6}, {2, 7}, {0, 5, 8, 9}, {4, 6, 1, 8}, {5, 7, 2, 9}, {3, 6, 9, 1},
            {4, 9, 5}, {7, 8, 4, 6}]


class Game:
    def get_active_tiles(self) -> []:
        raise NotImplemented("Method play is not implemented")

    def get_blocked(self):
        raise NotImplemented("Method play is not implemented")

    def get_cards(self) -> []:
        raise NotImplemented("Method play is not implemented")

    def get_characters(self) -> []:
        raise NotImplemented("Method play is not implemented")

    def log(self, message: str):
        raise NotImplemented("Method play is not implemented")

    def ask(self, message: str, number: int):
        raise NotImplemented("Method play is not implemented")

    def get_start(self) -> int:
        raise NotImplemented("Method play is not implemented")

    def set_start(self, start: int) -> None:
        raise NotImplemented("Method play is not implemented")


class Character:
    def __init__(self, color: colors):
        """
        Create a new character
        :param color: The color of the character
        """
        self.color, self.suspect, self.position, self.power = color, True, 0, True

    def __repr__(self):
        suspect = "-suspect" if self.suspect else "-clean"
        return self.color + "-" + str(self.position) + suspect


class Player:
    def __init__(self, n: int, g: Game):
        """
        Create a new player
        :param n: id of the player
        :param g: game instance
        """
        self.number = n
        self.game = g
        self.role = "l'inspecteur" if n == 0 else "le fantome"

    def play(self) -> None:
        """
        Play a player turn
        """
        self.game.log("****\n  Tour de " + self.role)
        p = self.select_character(self.game.get_active_tiles)
        has = self.use_power(p, before | both)
        self.move(p, has, self.game.get_blocked)
        self.use_power(p, after | both)

    def select_character(self, t: []) -> Character:
        """
        Select a character by asking the player
        :param t: list of characters
        :return: Return the selected character
        """
        w = self.game.ask("Tuiles disponibles : " + str(t) + " choisir entre 0 et " + str(len(t) - 1), self.number)
        i = int(w) if w.isnumeric() and int(w) in range(len(t)) else 0
        p = t[i]
        self.game.log("REPONSE INTERPRETEE : " + str(p))
        self.game.log(self.role + " joue " + p.color)
        del t[i]
        return p

    def use_power(self, p: Character, available: colors) -> []:
        """
        Use a character power
        :param p: Character
        :param available: Mask to knowing
        :return: list of character
        """
        if p.power and p.color in available:
            a = self.game.ask("Voulez-vous activer le pouvoir (0/1) ?", self.number) == "1"
            self.game.log("REPONSE INTERPRETEE : " + str(a == 1))
            if a:
                self.game.log("Pouvoir de " + p.color + " activé")
                p.power = False
                if p.color == "rouge":
                    draw = self.game.get_cards[0]
                    self.game.log(str(draw) + " a été tiré")
                    if draw == "fantome":
                        s = self.game.get_start
                        self.game.set_start(s - 1 if self.number == 0 else s + 1)
                    elif self.number == 0:
                        draw.suspect = False
                    del self.game.get_cards[0]
                if p.color == "noir":
                    for q in self.game.get_characters:
                        if q.position in {x for x in passages[p.position] if
                                          x not in self.game.blocked or q.position not in self.game.blocked}:
                            q.position = p.position
                            self.game.log("NOUVEAU PLACEMENT : " + str(q))
                if p.color == "blanc":
                    for q in self.game.get_characters:
                        if q.position == p.position and p != q:
                            usable = {x for x in passages[p.position] if x not in self.game.blocked or
                                      q.position not in self.game.blocked}
                            w = self.game.ask(str(q) + ", positions disponibles : " + str(usable) +
                                              ", choisir la valeur", self.number)
                            x = int(w) if w.isnumeric() and int(w) in usable else usable.pop()
                            self.game.log("REPONSE INTERPRETEE : " + str(x))
                            q.position = x
                            self.game.log("NOUVEAU PLACEMENT : " + str(q))
                if p.color == "violet":
                    self.game.log("Rappel des positions :\n" + str(self.game))
                    co = self.game.ask("Avec quelle couleur échanger (pas violet!) ?", self.number)
                    if co not in colors:
                        co = "rose"
                    self.game.log("REPONSE INTERPRETEE : " + co)
                    q = [x for x in self.game.get_characters if x.color == co][0]
                    p.position, q.position = q.position, p.position
                    self.game.log("NOUVEAU PLACEMENT : " + str(p))
                    self.game.log("NOUVEAU PLACEMENT : " + str(q))
                if p.color == "marron":
                    return [q for q in self.game.get_characters if p.position == q.position]
                if p.color == "gris":
                    w = self.game.ask("Quelle salle obscurcir ? (0-9)", self.number)
                    self.game.shadow = int(w) if w.isnumeric() and int(w) in range(10) else 0
                    self.game.log("REPONSE INTERPRETEE : " + str(self.game.shadow))
                if p.color == "bleu":
                    w = self.game.ask("Quelle salle bloquer ? (0-9)", self.number)
                    x = int(w) if w.isnumeric() and int(w) in range(10) else 0
                    w = self.game.ask("Quelle sortie ? Chosir parmi : " + str(passages[x]), self.number)
                    y = int(w) if w.isnumeric() and int(w) in passages[x] else passages[x].copy().pop()
                    self.game.log("REPONSE INTERPRETEE : " + str({x, y}))
                    self.game.blocked = {x, y}
        return [p]

    def move(self, p: Character, has: [], blocked: []) -> None:
        """
        Ask, the player where to move the character
        :param p: Character to move
        :param has: Available position
        :param blocked: Blocked passage
        """
        pass_act = pass_ext if p.color == 'rose' else passages
        if p.color != 'violet' or p.power:
            available = {x for x in pass_act[p.position] if p.position not in blocked or x not in blocked}
            w = self.game.ask("positions disponibles : " + str(available) + ", choisir la valeur", self.number)
            x = int(w) if w.isnumeric() and int(w) in available else available.pop()
            self.game.log("REPONSE INTERPRETEE : " + str(x))
            for q in has:
                q.position = x
                self.game.log("NOUVEAU PLACEMENT : " + str(q))


class OperaGame(Game):
    def __init__(self, index: int):
        """
        Create a new opera game with a game id
        :param index: game id
        """
        self.index = index
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log_path = "./logs/log_game_" + str(index) + ".txt"
        codecs.open(self.log_path, "w", "utf-8").close()
        self.server_address = ('localhost', 0)
        self.port = ""
        self.detective = None
        self.ghost = None
        self.players = [Player(0, self), Player(1, self)]

        self.finished = False
        self.start, self.end, self.num_tour, self.shadow, x = 4, 22, 1, randrange(10), randrange(10)
        self.blocked = {x, passages[x].copy().pop()}
        self.characters = {Character(c) for c in colors}
        self.tiles = [p for p in self.characters]
        self.cards = self.tiles[:]
        self.ghost_card = self.cards[randrange(8)]
        self.message("!!! Le fantôme est : " + self.ghost_card.color)
        self.cards.remove(self.ghost_card)
        self.cards += ['fantome'] * 3
        self.active_tiles = []

        shuffle(self.tiles)
        shuffle(self.cards)
        for i, p in enumerate(self.tiles):
            p.position = i

    @property
    def get_active_tiles(self) -> []:
        return self.active_tiles

    @property
    def get_blocked(self):
        return self.blocked

    @property
    def get_cards(self) -> []:
        return self.cards

    @property
    def get_characters(self) -> []:
        return self.characters

    @property
    def get_start(self) -> int:
        return self.start

    def set_start(self, start: int) -> None:
        """
        Set start
        :param start: start value
        """
        self.start = start

    def reset(self) -> None:
        """
        Reset the game state
        """
        self.ghost.sendall("RESET".encode())
        self.detective.sendall("RESET".encode())
        codecs.open(self.log_path, "w", "utf-8").close()
        self.initial_state()

    def initial_state(self) -> None:
        """
        Initialize game state
        """
        self.finished = False
        self.start, self.end, self.num_tour, self.shadow, x = 4, 22, 1, randrange(10), randrange(10)
        self.blocked = {x, passages[x].copy().pop()}
        self.characters = {Character(c) for c in colors}
        self.tiles = [p for p in self.characters]
        self.cards = self.tiles[:]
        self.ghost_card = self.cards[randrange(8)]
        self.message("!!! Le fantôme est : " + self.ghost_card.color)
        self.cards.remove(self.ghost_card)
        self.cards += ['fantome'] * 3
        self.active_tiles = []

        shuffle(self.tiles)
        shuffle(self.cards)
        for i, p in enumerate(self.tiles):
            p.position = i

    def init_server(self) -> int:
        """
        Init server socket
        :return: server port
        """
        self.socket.bind(self.server_address)
        self.socket.listen(1)
        self.port = self.socket.getsockname()[1]
        self.server_address = ('localhost', self.port)
        return self.port

    def run(self, batches: int) -> None:
        """
        Run the game server
        :param batches: number of game batches
        """
        running = True
        count = 0
        detective_count = 0
        ghost_count = 0
        b = batches
        start = time.perf_counter()
        while running:
            if self.detective is None or self.ghost is None:
                connection, client_address = self.socket.accept()
                print('connection from', client_address)
                data = connection.recv(128)
                str_data = data.decode("utf-8")[8:]
                if str_data == "1":
                    self.ghost = connection
                elif str_data == "0":
                    self.detective = connection
                else:
                    print(data)
            else:
                print(
                    "\n===================================== Start game n°{} =====================================\n".format(
                        count))
                score = self.start_game()
                end_client = False
                # while not end_client:
                #     self.ghost.sendall("_".encode())
                #     data = self.ghost.recv(128)
                #     s = data.decode("utf-8").rstrip()
                #     if s == "END GAME":
                #         end_client = True
                # end_client = False
                # while not end_client:
                #     self.detective.sendall("_".encode())
                #     data = self.detective.recv(128)
                #     s = data.decode("utf-8").rstrip()
                #     if s == "END GAME":
                #         end_client = True
                print(
                    "\n===================================== End game n°{} ! =====================================".format(
                        count))
                print("PERCENT:" + str(count))
                if score > 0:
                    detective_count += 1
                else:
                    ghost_count += 1
                b -= 1
                if b == 0:
                    running = False
                else:
                    self.reset()
                    count += 1
        duration = time.process_time() - start
        print("PERCENT:" + str(count))
        self.print_stats(duration, batches, detective_count, ghost_count)
        self.socket.close()

    @staticmethod
    def print_stats(duration: float, batches: int, detective_count: int, ghost_count: int) -> None:
        """
        Print the game(s) stats
        :param duration: duration iin seconds
        :param batches: number of games
        :param detective_count: detective wins
        :param ghost_count: ghost wins
        """
        print("STATS")
        print("\n+------------------------------------------------+")
        print("|                  SERVER STATS                  |")
        print("+================================================+")
        print("| Game played     |",
              (str(batches) +
               "                              ")[:29] + "|")
        print("+------------------------------------------------+")
        print("| Time played     |",
              ("{} sec".format(duration) +
               "                              ")[:29] + "|")
        print("+------------------------------------------------+")
        print("| Detective ratio |",
              (str((detective_count / batches) * 100) +
               "% ({}/{})".format(detective_count, batches) +
               "                              ")[:29] + "|")
        print("+------------------------------------------------+")
        print("| Ghost ratio     |",
              (str((ghost_count / batches) * 100) +
               "% ({}/{})".format(ghost_count, batches) +
               "                              ")[:29] + "|")
        print("+================================================+")
        if detective_count == ghost_count:
            print("|                   DRAW GAMES                   |")
        elif detective_count > ghost_count:
            print("|                 DETECTIVE WIN                  |")
        else:
            print("|                   GHOST WIN                    |")
        print("+------------------------------------------------+")

    def message(self, txt: str) -> None:
        """
        Log a message in log file
        :param txt: Message to print
        """
        logfile = codecs.open(self.log_path, "a", "utf-8")
        logfile.write(txt + "\n")
        logfile.close()

    def log(self, txt: str) -> None:
        """
        Log a message
        :param txt: Message to print
        """
        self.message(txt)

    def ask(self, q: str, number: int) -> str:
        """
        Ask player with a query
        :param q: query
        :param number: player id
        :return: the player response
        """
        self.log("QUESTION : " + q)
        if number == 0:
            self.ghost.sendall(q.encode())
            response = self.ghost.recv(128).decode("utf-8")
        else:
            self.detective.sendall(q.encode())
            response = self.detective.recv(128).decode("utf-8")
        self.log("REPONSE DONNEE : " + response)
        return response

    def actions(self) -> None:
        """
        Update active tiles
        """
        active_player = self.num_tour % 2
        if active_player == 1:
            shuffle(self.tiles)
            self.active_tiles = self.tiles[:4]
        else:
            self.active_tiles = self.tiles[4:]
        for i in [active_player, 1 - active_player, 1 - active_player, active_player]:
            self.players[i].play()

    def light(self) -> None:
        """
        Check if ghost scream or not
        """
        partition = [{p for p in self.characters if p.position == i} for i in range(10)]
        if len(partition[self.ghost_card.position]) == 1 or self.ghost_card.position == self.shadow:
            self.log("le fantome frappe")
            self.start += 1
            for piece, gens in enumerate(partition):
                if len(gens) > 1 and piece != self.shadow:
                    for p in gens:
                        p.suspect = False
        else:
            self.log("pas de cri")
            for piece, gens in enumerate(partition):
                if len(gens) == 1 or piece == self.shadow:
                    for p in gens:
                        p.suspect = False
        self.start += len([p for p in self.characters if p.suspect])

    def turn(self) -> None:
        """
        Play a turn
        """
        self.log("**************************\n" + str(self))
        self.actions()
        self.light()
        for p in self.characters:
            p.power = True
        self.num_tour += 1

    def start_game(self) -> int:
        """
        Start a new game
        :return: Return the final score
        """
        while self.start < self.end and len([p for p in self.characters if p.suspect]) > 1:
            self.turn()
        self.log("L'enquêteur a trouvé - c'était " + str(
            self.ghost_card) if self.start < self.end else "Le fantôme a gagné")
        score = self.end - self.start
        self.log("Score final : " + str(score))
        return score

    def __repr__(self):
        return "Tour:" + str(self.num_tour) + ", Score:" + str(self.start) + "/" + str(self.end) + ", Ombre:" + str(
            self.shadow) + ", Bloque:" + str(self.blocked) + "\n" + "  ".join([str(p) for p in self.characters])

    @staticmethod
    def init_from_state(state):
        print(state)

    @staticmethod
    def generate_game_from_state(index, state):
        game = OperaGame(index)
        game.init_from_state(state)
        return game
