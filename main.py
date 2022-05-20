
import random

HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 20
SHIP_SIZES = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'

def get_random_position():
    """Generates a random location on a board of NUM_ROWS x NUM_COLS."""

    row_choice = chr(
        random.choice(
            range(
                ord(MIN_ROW_LABEL),
                ord(MIN_ROW_LABEL) + NUM_ROWS
            )
        )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return (row_choice, col_choice)


def play_battleship():
    """Controls flow of Battleship games including display of
    welcome and goodbye messages.

    :return: None
    """

    print("Let's Play Battleship!\n")

    game_over = False

    while not game_over:

        game = Game()
        game.display_board()

        while not game.is_complete():

            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Goodbye.")


### DO NOT EDIT ABOVE (with the exception of MAX_MISSES) ###


class Ship:

    def __init__(self, name, start_position, orientation):
        """Creates a new ship with the given name, placed at start_position in the
        provided orientation. The number of positions occupied by the ship is determined
        by looking up the name in the SHIP_SIZE dictionary.
        :param name: the name of the ship
        :param start_position: tuple representing the starting position of ship on the board
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return: None
        """
        self.sunk = False
        self.name = name
        length = SHIP_SIZES.get(self.name)
        orientation_dict = {start_position: False}
        x_value = start_position[COL_IDX]
        y_value = start_position[ROW_IDX]
        if orientation == VERTICAL:
            for i in range(length - 1):
                past_value = list(orientation_dict)[-1]
                y_value = past_value[ROW_IDX]
                current_value = ((chr(ord(y_value) + 1)), x_value)
                current_dict = {current_value: False}
                orientation_dict.update(current_dict)
            self.positions = (orientation_dict)
        elif orientation == HORIZONTAL:
            for i in range(length - 1):
                past_value = list(orientation_dict)[-1]
                x_value = past_value[COL_IDX]
                current_value = (y_value, x_value + 1)
                current_dict = {current_value: False}
                orientation_dict.update(current_dict)
            self.positions = (orientation_dict)


class Game:
    ########## DO NOT EDIT #########

    _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]

    def __init__(self, max_misses=MAX_MISSES):
        """ Creates a new game with max_misses possible missed guesses.
        The board is initialized in this function and ships are randomly
        placed on the board.
        :param max_misses: maximum number of misses allowed before game ends
        """
        self.max_misses = max_misses
        self.guesses = []
        self.ships = []
        self.board = {}
        Game.initialize_board(self)
        Game.create_and_place_ships(self)

    def initialize_board(self):
        """Sets the board to it's initial state with each position occupied by
        a period ('.') string.
        :return: None
        """

        current_char = MIN_ROW_LABEL
        for iteration in range(NUM_ROWS):
            self.board[current_char] = ["."] * 10
            current_char = chr(ord(current_char) + 1)

    def display_board(self):
        """ Displays the current state of the board."""

        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()

    def in_bounds(self, start_position, ship_size, orientation):
        """Checks that a ship requiring ship_size positions can be placed at start position.
        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement inside board boundary, False otherwise
    """
        if orientation == VERTICAL:
            vertical_axis = ord(start_position[ROW_IDX])
            if (vertical_axis + ship_size) > ord(MAX_ROW_LABEL):
                return False
            else:
                return True

        elif orientation == HORIZONTAL:
            horizontal_axis = start_position[COL_IDX]
            if (horizontal_axis + ship_size) > (NUM_COLS - 1):
                return False
            else:
                return True

    def overlaps_ship(self, start_position, ship_size, orientation):
        """Checks for overlap between previously placed ships and a potential new ship
        placement requiring ship_size positions beginning at start_position in the
        given orientation.
        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement overlaps previously placed ship, False otherwise
        """

        new_list = []
        for ship in self.ships:
            for position in ship.positions.keys():
                new_list.append(position)

        if orientation == VERTICAL:
            horizontal_axis = start_position[COL_IDX]
            current_char = start_position[ROW_IDX]
            for size_iteration in range(ship_size):
                new_position = (current_char, horizontal_axis)
                if new_position in new_list:
                    return True
                else:
                    current_char = (chr(ord(current_char) + 1))
            return False

        elif orientation == HORIZONTAL:
            vertical_axis = start_position[ROW_IDX]
            current_char = start_position[COL_IDX]
            for size_iteration in range(ship_size):
                new_position = (vertical_axis, current_char)
                if new_position in new_list:
                    return True
                else:
                    current_char = current_char + 1
            return False

    def place_ship(self, start_position, ship_size):
        """Determines if placement is possible for ship requiring ship_size positions placed at
        start_position. Returns the orientation where placement is possible or None if no placement
        in either orientation is possible.
        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :return orientation: 'h' if horizontal placement possible, 'v' if vertical placement possible,
        None if no placement possible
        """

        if not self.overlaps_ship(start_position, ship_size, HORIZONTAL) and self.in_bounds(start_position, ship_size, HORIZONTAL):
            return HORIZONTAL
        elif not self.overlaps_ship(start_position, ship_size, VERTICAL) and self.in_bounds(start_position,ship_size, VERTICAL):
            return VERTICAL

    def create_and_place_ships(self):
        """Instantiates ship objects with valid board placements.
        :return: None
        """

        for iteration in Game._ship_types:
            ship_size = SHIP_SIZES.get(iteration)
            random_pos = get_random_position()
            new_orientation = self.place_ship(random_pos, ship_size)
            while new_orientation != HORIZONTAL and new_orientation != VERTICAL:
                random_pos = get_random_position()
                new_orientation = self.place_ship(random_pos, ship_size)
            self.ships.append(Ship(iteration, random_pos, new_orientation))

    def get_guess(self):
        """Prompts the user for a row and column to attack. The
        return value is a board position in (row, column) format
        :return position: a board position as a (row, column) tuple
        """
        row_guess = ""
        col_guess = ""
        valid_row = False
        valid_col = False
        while (not valid_row):
            row_guess = input("Enter a row: ")
            if row_guess >= MIN_ROW_LABEL and row_guess <= MAX_ROW_LABEL and len(row_guess) == 1:
                valid_row = True
        while (not valid_col):
            col_guess = int(input("Enter a column: "))
            if col_guess >= 0 and col_guess <= NUM_COLS-1:
                valid_col = True
        print((row_guess, col_guess))
        return (row_guess, col_guess)

    def check_guess(self, position):
        """Checks whether or not position is occupied by a ship. A hit is
        registered when position occupied by a ship and position not hit
        previously. A miss occurs otherwise.
        :param position: a (row,column) tuple guessed by user
        :return: guess_status: True when guess results in hit, False when guess results in miss
        """

        all_true = True
        for ship in self.ships:
            if position in list(ship.positions):
                true_false = ship.positions.get(position)
                new_dict = {(position): not true_false}
                ship.positions.update(new_dict)
                for ship_pos in range(len(ship.positions)):
                    if list(ship.positions.values())[ship_pos] == False:
                        all_true = False
                if all_true == True:
                    ship.sunk = True
                    print(f"You sunk the {ship.name}!")
                return not true_false
        return False

    def update_game(self, guess_status, position):
        """Updates the game by modifying the board with a hit or miss
        symbol based on guess_status of position.
        :param guess_status: True when position is a hit, False otherwise
        :param position:  a (row,column) tuple guessed by user
        :return: None
        """

        if guess_status is True:
            self.board[position[ROW_IDX]][position[COL_IDX]] = HIT_CHAR

        elif guess_status is False and self.board[position[ROW_IDX]][position[COL_IDX]] == HIT_CHAR:
            self.guesses.append(position)

        elif guess_status is False and self.board[position[ROW_IDX]][position[COL_IDX]] == BLANK_CHAR:
            self.board[position[ROW_IDX]][position[COL_IDX]] = MISS_CHAR
            self.guesses.append(position)

    def is_complete(self):
        """Checks to see if a Battleship game has ended. Returns True when the game is complete
        with a message indicating whether the game ended due to successfully sinking all ships
        or reaching the maximum number of guesses. Returns False when the game is not
        complete.
        :return: True on game completion, False otherwise
        """

        ship_total = 0
        for ship in self.ships:
            if ship.sunk == True:
                ship_total += 1
        if ship_total == len(SHIP_SIZES):
            print("YOU WIN!")
            return True
        elif len(self.guesses) == MAX_MISSES:
            print("SORRY! NO GUESSES LEFT.")
            return True
        else:
            return False

def end_program():
    """Prompts the user with "Play again (Y/N)?" The question is repeated
    until the user enters a valid response (Y/y/N/n). The function returns
    False if the user enters 'Y' or 'y' and returns True if the user enters
    'N' or 'n'.

    :return response: boolean indicating whether to end the program
    """
    user_input = ""
    while user_input != "n" and user_input != "y":
        user_input = input("Play again (Y/N)?").lower()
    if user_input == "n":
        return True
    else:
        return False

def main():
    """Executes one or more games of Battleship."""
    play_battleship()

if __name__ == "__main__":
    main()
