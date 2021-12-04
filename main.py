from __future__ import annotations

import pygame
import random


# 0 - empty
# 1 - ship
# 2 - injured
# 3 - destroyed
# 4 - miss

class CustomList(list):
    def __getitem__(self, index):
        if index < 0:
            raise IndexError(f'Expected a positive index, instead got {index}')

        return super(CustomList, self).__getitem__(index)

    def __setitem__(self, key, value):
        if key < 0:
            raise IndexError(f'Expected a positive index, instead got {key}')

        return super(CustomList, self).__setitem__(key, value)


class Ship:
    def __init__(self, size: int, x: int, y: int, direction: str):
        self.size = size
        self.hp = size
        self.x = x
        self.y = y
        self.direction = direction
        self.coordinates = []

    def __str__(self):
        return f'{self.size=}, {self.x=}, {self.y=}, {self.direction=}'


class Player:
    def __init__(self, name: str, index: int, is_ai=False):
        self.field = Field()
        self.is_ai = is_ai
        self.name = name
        self.index = index
        self.hp = 0

    def reduce_hp(self):
        self.hp -= 1

    def set_hp(self, hp: int):
        self.hp = hp

    @staticmethod
    def shot_to_field(target_player: Player, x: int, y: int):
        if target_player.field.shot(x, y):
            target_player.reduce_hp()


class Field:
    def __init__(self, size=10):
        self.size = size
        self.field = []
        self.coordinates = {}
        self.section = None
        self.init_field()
        self.ships = []

    def init_field(self):
        self.field = CustomList(CustomList([0] * self.size) for i in range(self.size))

    def arrange_ships(self) -> None:
        """ Arrange ships on player's field """
        directions = ['up', 'down', 'left', 'right']
        for ship_size, count in Game.ships.items():  # unpack ships
            # go through all ship with selected size
            for i in range(count):
                while True:
                    # get random position on the field
                    y = random.choice(range(len(self.field)))  # int
                    y_array = self.field[y]  # list
                    x = random.choice(range(len(y_array)))  # int

                    direction = random.choice(directions)

                    # if in selected position with selected direction can arrange ship -> arrange it
                    if self._check_ship(ship_size, direction, x, y):
                        ship = Ship(ship_size, x, y, direction)
                        self._arrange_ship(ship)
                        self.ships.append(ship)
                        print(ship, ship.coordinates)
                        break

    def _check_ship(self, ship: int, direction: str, x: int, y: int) -> bool:
        """
        Check if ship with selected parameters can be arranged at the selected position
        :param ship: ship length
        :param direction: direction of ship's arranging
        :param x: x position
        :param y: y position
        :return: True if it can, False if not
        """
        try:
            # check if there is no ship in selected position or near
            if self.field[y][x] == 1 \
                    or self.field[y - 1][x - 1] == 1 \
                    or self.field[y - 1][x] == 1 \
                    or self.field[y - 1][x + 1] == 1 \
                    or self.field[y][x + 1] == 1 \
                    or self.field[y + 1][x + 1] == 1 \
                    or self.field[y + 1][x] == 1 \
                    or self.field[y + 1][x - 1] == 1 \
                    or self.field[y][x - 1] == 1:
                return False
        except IndexError:
            pass

        # check if can arrange ship in selected place
        if direction == 'up':
            try:
                for i in range(ship):
                    if self.field[y - 1][x] == 1 \
                            or self.field[y - 1][x - 1] == 1 \
                            or self.field[y - 1][x + 1] == 1:
                        return False

                    y -= 1
            except IndexError:
                return False
        elif direction == 'down':
            try:
                for i in range(ship):
                    if self.field[y + 1][x] == 1 \
                            or self.field[y + 1][x - 1] == 1 \
                            or self.field[y + 1][x + 1] == 1:
                        return False

                    y += 1
            except IndexError:
                return False
        elif direction == 'right':
            try:
                for i in range(ship):
                    if self.field[y][x + 1] == 1 \
                            or self.field[y + 1][x + 1] == 1 \
                            or self.field[y - 1][x + 1] == 1:
                        return False

                    x += 1
            except IndexError:
                return False
        elif direction == 'left':
            try:
                for i in range(ship):
                    if self.field[y - 1][x - 1] == 1 \
                            or self.field[y + 1][x - 1] == 1 \
                            or self.field[y][x - 1] == 1:
                        return False

                    x -= 1
            except IndexError:
                return False

        return True

    def _arrange_ship(self, ship: Ship) -> None:
        """
        Arrange one ship on field
        :param ship: ship object to arrange
        :return: None
        """
        if ship.direction == 'up':
            for i in range(ship.size):
                self.field[ship.y - i][ship.x] = 1
                ship.coordinates.append((ship.x, ship.y - i))
        if ship.direction == 'down':
            for i in range(ship.size):
                self.field[ship.y + i][ship.x] = 1
                ship.coordinates.append((ship.x, ship.y + i))
        if ship.direction == 'left':
            for i in range(ship.size):
                self.field[ship.y][ship.x - i] = 1
                ship.coordinates.append((ship.x - i, ship.y))
        if ship.direction == 'right':
            for i in range(ship.size):
                self.field[ship.y][ship.x + i] = 1
                ship.coordinates.append((ship.x + i, ship.y))

    def show_field(self):
        for row in self.field:
            print(row)

    def get_value(self, x: int, y: int) -> None:
        return self.field[y][x]

    def _set_value(self, x: int, y: int, value: int) -> None:
        self.field[y][x] = value

    def _get_ship_by_coordinates(self, x: int, y: int) -> Ship:
        """
        Return ship by selected coordinates
        :param x: x position
        :param y: y position
        :return: Ship object
        """
        for ship in self.ships:
            if (x, y) in ship.coordinates:
                return ship

    def _check_if_ship_destroyed(self, x: int, y: int) -> bool:
        """
        Check if ship on selected coordinates is destroyed or not
        :param x: x position
        :param y: y position
        :return: True if destroyed, False if not
        """
        ship = self._get_ship_by_coordinates(x, y)
        if ship.hp == 0:
            return True

        return False

    def _destroy_ship(self, ship: Ship):
        for coordinate in ship.coordinates:
            x, y = coordinate
            self._set_value(x, y, 3)

    def shot(self, x: int, y: int) -> bool:
        """
        Make shot to field
        :param x: x position
        :param y: y position
        :return: True if shot to ship, False if not
        """
        if self.get_value(x, y) == 0:
            self._set_value(x, y, 4)

            return False
        elif self.get_value(x, y) == 1:
            self._set_value(x, y, 2)
            ship = self._get_ship_by_coordinates(x, y)

            # reduce ship's hp
            if ship.hp > 0:
                ship.hp -= 1

            if self._check_if_ship_destroyed(x, y):
                self._destroy_ship(ship)

            return True

        return False


class Game:
    ships = {
        4: 1,
        3: 2,
        2: 3,
        1: 4
    }

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 124)

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
        self._set_players_hp()

        self.players[0].field.arrange_ships()

        # for player in self.players:
        #     player.field.arrange_ships()

        self.window_size = (1200, 600)
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self.WHITE)

        pygame.display.set_caption('Warships')

        self.font_size = int(self.cell_width / 1.5)
        self.font = pygame.font.SysFont('notosans', self.font_size)

        self.game_over = False
        self.start_game = False

        self._draw_grid()
        pygame.display.update()

    def _draw_field(self, player: Player) -> None:
        """ Draw field for selected player """
        x, y = 0, 0
        field_size = player.field.size

        # draw text under field
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
                value = player.field.get_value(col, row)
                box_rect = [x, y, self.cell_width, self.cell_height]
                if value == 0:  # empty
                    pygame.draw.rect(self.screen, self.BLACK, box_rect, 2)
                elif value == 1:  # ship
                    pygame.draw.rect(self.screen, self.BLUE, box_rect, 0)
                elif value == 2:  # injured
                    pygame.draw.rect(self.screen, self.RED, box_rect, 0)
                elif value == 3:  # destroyed
                    pygame.draw.rect(self.screen, self.BLACK, box_rect, 0)
                elif value == 4:  # miss
                    x_circle = self.cell_width / 2 + x
                    y_circle = self.cell_height / 2 + y
                    pygame.draw.rect(self.screen, self.BLACK, box_rect, 2)
                    pygame.draw.circle(self.screen, self.BLACK, (x_circle, y_circle), 5)

                # save cell coordinates
                player.field.coordinates[(col, row)] = (x, y, x + self.cell_width, y + self.cell_height)
                x += self.cell_width

            if player.index == 0:
                x = self.left_margin
            elif player.index == 1:
                x = self.left_margin + self.cell_width * field_size + self.fields_distance

            y += self.cell_width

        player.field.section = (x_begin, y_begin, x + field_size * self.cell_width, y)

    def _draw_buttons(self) -> None:
        """ Draw buttons """
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

    def _draw_grid(self) -> None:
        """ Draw all game field """
        self.screen.fill(self.WHITE)

        for player in self.players:
            self._draw_field(player)

        self._draw_buttons()

    def _button_press(self, button: str) -> None:
        """
        Press on the selected button
        :param button: button name
        :return: None
        """
        if button == 'Start':
            self.start_game = True
            print('start')
        elif button == 'Arrange':
            self.players[0].field.init_field()
            self.players[0].field.arrange_ships()
            self._draw_grid()
            pygame.display.update()

    def _change_player(self):
        """ Change player's turn """
        if self.player_index == 0:
            self.player_index = 1
        elif self.player_index == 1:
            self.player_index = 0

    def _make_shot(self, mouse, player_from, player_to) -> None:
        """
        Make shot to enemy's field
        :param mouse: mouse coordinates
        :param player_from: player that make shot
        :param player_to: player on what field makes shot
        :return: None
        """
        user2_x_begin, user2_y_begin, user2_x_end, user2_y_end = self.players[player_to].field.section

        # check if mouse pressed in player_to field section
        if user2_x_begin < mouse[0] < user2_x_end and user2_y_begin < mouse[1] < user2_y_end:
            # go through all cells coordinates
            for cell, coordinates in self.players[player_to].field.coordinates.items():
                x_begin, y_begin, x_end, y_end = coordinates
                # found pressed cell
                if x_begin < mouse[0] < x_end and y_begin < mouse[1] < y_end:
                    x, y = cell
                    self.players[player_from].shot_to_field(self.players[player_to], x, y)
                    self._draw_grid()
                    self._change_player()
                    pygame.display.update()

    def _check_hp(self, player: Player) -> None:
        if player.hp == 0:
            self._end_game()

    def _set_players_hp(self) -> None:
        for player in self.players:
            hp = 0
            for ship in range(1, len(self.ships) + 1):
                hp += self.ships.get(ship) * ship

            player.set_hp(hp)

    def game_loop(self):
        while not self.game_over:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if not self.start_game:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        butt_x_begin, butt_y_begin, butt_x_end, butt_y_end = self.buttons_section
                        # check if mouse pressed in buttons section
                        if butt_x_begin < mouse[0] < butt_x_end and butt_y_begin < mouse[1] < butt_y_end:
                            for button, coordinates in self.buttons_coordinates.items():
                                x_begin, y_begin, x_end, y_end = coordinates
                                if x_begin < mouse[0] < x_end and y_begin < mouse[1] < y_end:
                                    self._button_press(button)
                if self.start_game:
                    if self.player_index == 0:
                        # if player is computer
                        if self.players[0].is_ai:
                            pass
                        else:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self._make_shot(mouse, 0, 1)
                                self._check_hp(self.players[1])

                    elif self.player_index == 1:
                        # if player is computer
                        if self.players[1].is_ai:
                            pass
                        else:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self._make_shot(mouse, 1, 0)
                                self._check_hp(self.players[0])

    def _end_game(self) -> None:
        self.game_over = True


if __name__ == '__main__':
    players = [Player('User', 0), Player('Computer', 1, is_ai=False)]
    game = Game(players)
    game.game_loop()
    pygame.quit()
