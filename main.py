import pygame
import random


class CustomList(list):
    def __getitem__(self, index):
        if index < 0:
            raise IndexError(f'Expected a positive index, instead got {index}')

        return super(CustomList, self).__getitem__(index)

    def __setitem__(self, key, value):
        if key < 0:
            raise IndexError(f'Expected a positive index, instead got {key}')

        return super(CustomList, self).__setitem__(key, value)


class Player:
    def __init__(self, name: str, index: int, is_ai=False):
        self.field = Field()
        self.is_ai = is_ai
        self.name = name
        self.index = index


class Field:
    ships = {
        4: 1,
        3: 2,
        2: 3,
        1: 4
    }

    def __init__(self, size=10):
        self.size = size
        self.field = []
        self.coordinates = {}
        self.section = None
        self.init_field()

    def init_field(self):
        self.field = CustomList([0] * self.size for i in range(self.size))

    def arrange_ships(self):
        directions = ['up', 'down', 'left', 'right']
        for ship, count in self.ships.items():  # unpack ships
            # go through all ship with selected size
            for i in range(count):
                while True:
                    # get random position on the field
                    pos_y = random.choice(range(len(self.field)))  # int
                    y_array = self.field[pos_y]  # list
                    pos_x = random.choice(range(len(y_array)))  # int

                    direction = random.choice(directions)

                    # if in selected position with selected direction can arrange ship -> arrange it
                    if self._check_ship(ship, direction, pos_x, pos_y):
                        self._arrange_ship(ship, direction, pos_x, pos_y)
                        break

    def _check_ship(self, ship: int, direction: str, pos_x: int, pos_y: int) -> bool:
        try:
            # check if there is no ship in selected position or near
            if self.field[pos_y][pos_x] == 1 \
                    or self.field[pos_y - 1][pos_x - 1] == 1 \
                    or self.field[pos_y - 1][pos_x] == 1 \
                    or self.field[pos_y - 1][pos_x + 1] == 1 \
                    or self.field[pos_y][pos_x + 1] == 1 \
                    or self.field[pos_y + 1][pos_x + 1] == 1 \
                    or self.field[pos_y + 1][pos_x] == 1 \
                    or self.field[pos_y + 1][pos_x - 1] == 1 \
                    or self.field[pos_y][pos_x - 1] == 1:
                return False
        except IndexError:
            pass

        # check if can arrange ship in selected place
        if direction == 'up':
            try:
                for i in range(ship):
                    if self.field[pos_y - 1][pos_x] == 1 \
                            or self.field[pos_y - 1][pos_x - 1] == 1 \
                            or self.field[pos_y - 1][pos_x + 1] == 1:
                        return False

                    pos_y -= 1
            except IndexError:
                return False
        elif direction == 'down':
            try:
                for i in range(ship):
                    if self.field[pos_y + 1][pos_x] == 1 \
                            or self.field[pos_y + 1][pos_x - 1] == 1 \
                            or self.field[pos_y + 1][pos_x + 1] == 1:
                        return False

                    pos_y += 1
            except IndexError:
                return False
        elif direction == 'right':
            try:
                for i in range(ship):
                    if self.field[pos_y][pos_x + 1] == 1 \
                            or self.field[pos_y + 1][pos_x + 1] == 1 \
                            or self.field[pos_y - 1][pos_x + 1] == 1:
                        return False

                    pos_x += 1
            except IndexError:
                return False
        elif direction == 'left':
            try:
                for i in range(ship):
                    if self.field[pos_y - 1][pos_x - 1] == 1 \
                            or self.field[pos_y + 1][pos_x - 1] == 1 \
                            or self.field[pos_y][pos_x - 1] == 1:
                        return False

                    pos_x -= 1
            except IndexError:
                return False

        return True

    def _arrange_ship(self, ship: int, direction: str, pos_x: int, pos_y: int):
        if direction == 'up':
            for i in range(ship):
                self.field[pos_y - i][pos_x] = 1
        if direction == 'down':
            for i in range(ship):
                self.field[pos_y + i][pos_x] = 1
        if direction == 'left':
            for i in range(ship):
                self.field[pos_y][pos_x - i] = 1
        if direction == 'right':
            for i in range(ship):
                self.field[pos_y][pos_x + i] = 1

    def get_value(self, row, col):
        return self.field[row][col]

    def set_value(self, row, col, value):
        self.field[row][col] = value


class Game:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # sizes
    left_margin = 250
    upper_margin = 50
    fields_distance = 100
    cell_width = cell_height = 40
    button_left_margin = 50
    button_width = 140
    button_height = 50
    button_distance = 50

    buttons_section = None
    buttons_coordinates = {}

    player_index = 0

    def __init__(self, players: list):
        pygame.init()

        self.players = players

        for player in self.players:
            player.field.arrange_ships()

        self.window_size = (1200, 600)
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self.WHITE)

        pygame.display.set_caption('Warships')

        self.font_size = int(self.cell_width / 1.5)
        self.font = pygame.font.SysFont('notosans', self.font_size)

        self.game_over = False
        self.start_game = False

        self.draw_grid()
        pygame.display.update()

        self.game_loop()

    def draw_field(self, player: Player):
        # draw text under field
        x, y = 0, 0
        field_size = player.field.size

        if player.index == 0:
            x, y = (self.left_margin + field_size * self.cell_width) / 2 + self.left_margin / 3, self.upper_margin / 2
        elif player.index == 1:
            x, y = self.left_margin + self.cell_width * field_size + self.cell_width * field_size / 2, self.upper_margin / 2

        text_surface = self.font.render(f'{player.name}\'s field', False, self.BLACK)
        self.screen.blit(text_surface, (x, y))

        # draw field
        if player.index == 0:
            x, y = self.left_margin, self.upper_margin
        elif player.index == 1:
            x, y = self.left_margin + self.cell_width * field_size + self.fields_distance, self.upper_margin

        # for saving coordinates of section
        x_begin = x
        y_begin = y

        for row in range(field_size):
            for col in range(field_size):
                value = player.field.get_value(row, col)
                box_rect = [x, y, self.cell_width, self.cell_height]
                if value == 0:  # empty
                    pygame.draw.rect(self.screen, self.BLACK, box_rect, 2)
                elif value == 1:  # ship
                    pygame.draw.rect(self.screen, self.RED, box_rect, 0)

                # save cell coordinates
                player.field.coordinates[(row, col)] = (x, y, x + self.cell_width, y + self.cell_height)
                x += self.cell_width

            if player.index == 0:
                x = self.left_margin
            elif player.index == 1:
                x = self.left_margin + self.cell_width * field_size + self.fields_distance

            y += self.cell_width

        player.field.section = (x_begin, y_begin, x + field_size * self.cell_width, y)

    def draw_buttons(self):
        buttons = ['Start', 'Arrange']
        x, y = self.button_left_margin, self.upper_margin
        x_text, y_text = (self.button_left_margin + self.button_width) / 2, (
                self.upper_margin + self.button_height) / 2 + 15
        y_begin = y  # for saving coordinates of section

        for button in buttons:
            box_rect = [x, y, self.button_width, self.button_height]
            pygame.draw.rect(self.screen, self.BLACK, box_rect, 2)
            # save button coordinates
            self.buttons_coordinates[button] = (x, y, x + self.button_width, y + self.button_height)

            text_surface = self.font.render(button, False, self.RED)
            self.screen.blit(text_surface, (x_text, y_text))

            y += self.button_distance + self.button_height
            y_text += self.button_distance + self.button_height

        self.buttons_section = (x, y_begin, x + self.button_width, y - self.button_height)

    def draw_grid(self):
        self.screen.fill(self.WHITE)

        for player in self.players:
            self.draw_field(player)

        self.draw_buttons()

    def button_press(self, button: str):
        if button == 'Start':
            self.start_game = True
        elif button == 'Arrange':
            self.players[0].field.init_field()
            self.players[0].field.arrange_ships()
            self.draw_grid()
            pygame.display.update()

    def game_loop(self):
        while not self.game_over:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if self.player_index == 0 and self.start_game:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        butt_x_begin, butt_y_begin, butt_x_end, butt_y_end = self.buttons_section
                        user1_x_begin, user1_y_begin, user1_x_end, user1_y_end = self.players[0].field.section
                        user2_x_begin, user2_y_begin, user2_x_end, user2_y_end = self.players[1].field.section

                        # check if mouse pressed in buttons section
                        if butt_x_begin < mouse[0] < butt_x_end and butt_y_begin < mouse[1] < butt_y_end:
                            for button, coordinates in self.buttons_coordinates.items():
                                x_begin, y_begin, x_end, y_end = coordinates
                                if x_begin < mouse[0] < x_end and y_begin < mouse[1] < y_end:
                                    self.button_press(button)

                        # check if mouse pressed in user 1 field section
                        elif user1_x_begin < mouse[0] < user1_x_end and user1_y_begin < mouse[1] < user1_y_end:
                            for cell, coordinates in self.players[0].field.coordinates.items():
                                x_begin, y_begin, x_end, y_end = coordinates
                                if x_begin < mouse[0] < x_end and y_begin < mouse[1] < y_end:
                                    print(f'{cell} pressed')

                        # check if mouse pressed in user 2 field section
                        elif user2_x_begin < mouse[0] < user2_x_end and user2_y_begin < mouse[1] < user2_y_end:
                            for cell, coordinates in self.players[1].field.coordinates.items():
                                x_begin, y_begin, x_end, y_end = coordinates
                                if x_begin < mouse[0] < x_end and y_begin < mouse[1] < y_end:
                                    print(f'{cell} pressed')

    def end_game(self):
        self.game_over = True


def main():
    players = [Player('User', 0), Player('Computer', 1, is_ai=True)]
    game = Game(players)


main()
pygame.quit()
