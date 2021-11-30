import pygame
import random


class Game:
    colors = {
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0)
    }

    ships = {
        4: 1,
        3: 2,
        2: 3,
        1: 4
    }

    def __init__(self, size=10):
        pygame.init()

        # initial size of game field
        self.field_size = size

        # initial sizes of game window
        self.block_size = self.field_size * 3
        self.left_margin = self.field_size * 20
        self.upper_margin = self.field_size * 5

        self.window_size = (self.left_margin + 30 * self.block_size, self.upper_margin + 15 * self.block_size)

        self.user_field = self.init_field()
        self.computer_field = self.init_field()

        self.arrange_ships(self.user_field)
        self.show_field(self.user_field)

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Warship')

        self.font_size = int(self.block_size / 1.5)

        self.font = pygame.font.SysFont('notosans', self.font_size)
        self.game_over = False

        self.screen.fill(self.colors.get('WHITE'))

    def init_field(self):
        field = []
        for i in range(self.field_size):
            field.append([0] * self.field_size)

        return field

    def arrange_ships(self, field: list):
        directions = ['up', 'down', 'left', 'right']
        for ship, count in self.ships.items():  # unpack ships
            print(ship, count)
            # go through all ship with selected size
            for i in range(count):
                while True:
                    # get random position on the field
                    pos_y = random.choice(range(len(field)))  # int
                    y_array = field[pos_y]  # list
                    pos_x = random.choice(range(len(y_array)))  # int

                    direction = random.choice(directions)

                    # if in selected position with selected direction can arrange ship -> arrange it
                    if self._check_ship(field, ship, direction, pos_x, pos_y):
                        self._arrange_ship(field, ship, direction, pos_x, pos_y)
                        break

    @staticmethod
    def _check_ship(field: list, ship: int, direction: str, pos_x: int, pos_y: int) -> bool:
        try:
            # check if there is no ship in selected position or near
            if field[pos_y][pos_x] == 1 \
                    or field[pos_y - 1][pos_x - 1] == 1 \
                    or field[pos_y - 1][pos_x] == 1 \
                    or field[pos_y - 1][pos_x + 1] == 1 \
                    or field[pos_y][pos_x + 1] == 1 \
                    or field[pos_y + 1][pos_x + 1] == 1 \
                    or field[pos_y + 1][pos_x] == 1 \
                    or field[pos_y + 1][pos_x - 1] == 1 \
                    or field[pos_y][pos_x - 1] == 1:
                return False
        except IndexError:
            pass

        if direction == 'up':
            try:
                # pos_y -= 1
                for i in range(ship):
                    if pos_x < 0 or pos_y < 0:
                        return False

                    if field[pos_y - 1][pos_x] == 1 \
                            or field[pos_y - 1][pos_x - 1] == 1 \
                            or field[pos_y - 1][pos_x + 1] == 1:
                        return False

                    pos_y -= i
            except IndexError:
                return False
        elif direction == 'down':
            try:
                # pos_y += 1
                for i in range(ship):
                    if pos_x < 0 or pos_y < 0:
                        return False

                    if field[pos_y + 1][pos_x] == 1 \
                            or field[pos_y + 1][pos_x - 1] == 1 \
                            or field[pos_y + 1][pos_x + 1] == 1:
                        return False

                    pos_y += i
            except IndexError:
                return False
        elif direction == 'right':
            try:
                # pos_x += 1
                for i in range(ship):
                    if pos_x < 0 or pos_y < 0:
                        return False

                    if field[pos_y][pos_x + 1] == 1 \
                            or field[pos_y + 1][pos_x + 1] == 1 \
                            or field[pos_y - 1][pos_x + 1] == 1:
                        return False

                    pos_x += i
            except IndexError:
                return False
        elif direction == 'left':
            try:
                # pos_x -= 1
                for i in range(ship):
                    if pos_x < 0 or pos_y < 0:
                        return False

                    if field[pos_y - 1][pos_x - 1] == 1 \
                            or field[pos_y + 1][pos_x - 1] == 1 \
                            or field[pos_y][pos_x - 1] == 1:
                        return False

                    pos_x -= i
            except IndexError:
                return False
        return True

    @staticmethod
    def _arrange_ship(field: list, ship: int, direction: str, pos_x: int, pos_y: int):
        if direction == 'up':
            for i in range(ship):
                field[pos_y - i][pos_x] = 1
        if direction == 'down':
            for i in range(ship):
                field[pos_y + i][pos_x] = 1
        if direction == 'left':
            for i in range(ship):
                field[pos_y][pos_x - i] = 1
        if direction == 'right':
            for i in range(ship):
                field[pos_y][pos_x + i] = 1


    def show_field(self, field):
        for y_array in field:
            print(y_array)
        print('\n')


    def draw_grid(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(11):
            # Hor grid1
            pygame.draw.line(self.screen, self.colors.get('BLACK'),
                             (self.left_margin, self.upper_margin + i * self.block_size),
                             (self.left_margin + 10 * self.block_size, self.upper_margin + i * self.block_size), 1)
            # Vert grid1
            pygame.draw.line(self.screen, self.colors.get('BLACK'),
                             (self.left_margin + i * self.block_size, self.upper_margin),
                             (self.left_margin + i * self.block_size, self.upper_margin + 10 * self.block_size), 1)
            # Hor grid2
            pygame.draw.line(self.screen, self.colors.get('BLACK'),
                             (self.left_margin + 15 * self.block_size, self.upper_margin +
                              i * self.block_size),
                             (self.left_margin + 25 * self.block_size, self.upper_margin + i * self.block_size), 1)
            # Vert grid2
            pygame.draw.line(self.screen, self.colors.get('BLACK'),
                             (self.left_margin + (i + 15) * self.block_size, self.upper_margin),
                             (self.left_margin + (i + 15) * self.block_size, self.upper_margin + 10 * self.block_size),
                             1)

            if i < 10:
                num_ver = self.font.render(str(i + 1), True, self.colors.get('BLACK'))
                letters_hor = self.font.render(letters[i], True, self.colors.get('BLACK'))

                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_width = letters_hor.get_width()

                # Ver num grid1
                self.screen.blit(num_ver, (self.left_margin - (self.block_size // 2 + num_ver_width // 2),
                                           self.upper_margin + i * self.block_size + (
                                                       self.block_size // 2 - num_ver_height // 2)))
                # Hor letters grid1
                self.screen.blit(letters_hor, (self.left_margin + i * self.block_size + (self.block_size //
                                                                                         2 - letters_hor_width // 2),
                                               self.upper_margin + 10 * self.block_size))
                # Ver num grid2
                self.screen.blit(num_ver, (self.left_margin - (self.block_size // 2 + num_ver_width // 2) + 15 *
                                           self.block_size,
                                           self.upper_margin + i * self.block_size + (
                                                       self.block_size // 2 - num_ver_height // 2)))
                # Hor letters grid2
                self.screen.blit(letters_hor, (self.left_margin + i * self.block_size + (self.block_size // 2 -
                                                                                         letters_hor_width // 2) + 15 * self.block_size,
                                               self.upper_margin + 10 * self.block_size))

    def start_game(self):
        pass

    def end_game(self):
        self.game_over = True




def main():
    game = Game()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True

        game.draw_grid()
        pygame.display.update()


main()
pygame.quit()
