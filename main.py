import pygame
import os
import random
import sys


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


pygame.init()
height = 720
width = 1280
screen_size = (height, width)
screen = pygame.display.set_mode(screen_size)
FPS = 50


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Deck(Sprite):
    def __init__(self, name, pos_x, pos_y, player):
        super().__init__(sprite_group)
        if player == 'player':
            self.image = load_image(name+'png')
        else:
            self.image = load_image('back.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()


def generate_deck(level):
    new_player, x, y = None, None, None
    suits = ['H', 'D', 'S', 'C']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    random_suit = random.choice(suits)
    random_rank = random.choice(ranks)
    card1 = random_rank + random_suit
    suits.remove(random_suit)
    ranks.remove(random_rank)
    random_suit = random.choice(suits)
    random_rank = random.choice(ranks)
    card2 = random_rank + random_suit
    Deck(card1, 100, 100, 'player')
    Deck(card2, 100, 150, 'player')


class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Start Screen")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)

        self.poker_button = pygame.Rect(50, 200, 200, 50)
        self.blackjack_button = pygame.Rect(50, 300, 200, 50)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.poker_button.collidepoint(event.pos):
                        poker_game = Poker()
                        poker_game.run()
                    elif self.blackjack_button.collidepoint(event.pos):
                        blackjack_game = Blackjack()
                        blackjack_game.run()

            self.screen.fill((255, 255, 255))

            pygame.draw.rect(self.screen, (0, 255, 0), self.poker_button)
            pygame.draw.rect(self.screen, (0, 0, 255), self.blackjack_button)

            poker_text = self.font.render("Poker", True, (255, 255, 255))
            blackjack_text = self.font.render("Blackjack", True, (255, 255, 255))

            self.screen.blit(poker_text, (self.poker_button.x + 50, self.poker_button.y + 15))
            self.screen.blit(blackjack_text, (self.blackjack_button.x + 20, self.blackjack_button.y + 15))

            pygame.display.flip()
            self.clock.tick(30)

class Poker:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Poker Game")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 255, 0))
            pygame.display.flip()
            self.clock.tick(30)

class Blackjack:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Blackjack Game")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 255))
            pygame.display.flip()
            self.clock.tick(30)


StartScreen().run()

