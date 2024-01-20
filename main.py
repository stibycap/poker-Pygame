import pygame
import os
import random
import sys


def load_image(name):
    fullname = os.path.join('img', name + '.png')
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
    def __init__(self, name, pos_x, pos_y, player=None):
        super().__init__(sprite_group)
        if player == 'player':
            self.image = load_image(name+'.png')
        else:
            self.image = load_image('back.png')
        self.rect = self.image.get_rect().move(
            1 * pos_x, 2 * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()


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
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Poker Game")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('img/background.jpg')
        self.screen.blit(self.background, (0, 0))
        self.suits = ['C', 'H', 'D', 'S']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

        self.card_images = {}
        for suit in self.suits:
            for rank in self.ranks:
                self.card_images[(rank, suit)] = load_image(rank+suit)

        self.deck = self.generate_deck()
        self.player_hand = []
        self.ai_hand = []
        self.x = 300
        self.deal_cards()

    def generate_deck(self):
        deck = [(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(deck)
        return deck[:8]

    def draw_card(self, card, position):
        x, y = 0, 0
        if position == 'player':
            x, y = self.x + 50, 500
            self.screen.blit(self.card_images[card], (x, y))
        elif position == 'ai':
            x, y = self.x + 50, 50
            self.screen.blit(load_image('back'), (x, y))
        self.x += 50

    def deal_cards(self):
        for _ in range(2):
            print(self.deck)
            player_card = self.deck.pop()
            ai_card = self.deck.pop()

            self.player_hand.append(player_card)
            self.ai_hand.append(ai_card)

            self.draw_card(player_card, 'player')
            self.draw_card(ai_card, 'ai')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

