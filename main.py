import pygame
import os
import random
import sys
import time
import pygame_gui


def load_image(name):
    fullname = os.path.join('img', name + '.png')
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image

width = 1000
height = 800


class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
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
                        poker_game = Poker_start()
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


class Poker_start:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font('font/CoffeeTin.ttf', 150)
        self.font2 = pygame.font.Font('font/IndianPoker.ttf', 75)
        self.background = pygame.image.load('img/background.jpg')
        self.font2.set_bold(True)

        self.startText = self.font2.render("Welcome to Poker!", 1, (0, 0, 0))
        self.startSize = self.font2.size("Welcome to Poker!")
        self.startLoc = (width / 2 - self.startSize[0] / 2, 50)

        self.startButton = self.font.render(" Start ", 1, (0, 0, 0))
        self.buttonSize = self.font.size(" Start ")
        self.buttonLoc = (width / 2 - self.buttonSize[0] / 2, height / 2 - self.buttonSize[1] / 2)

        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.screen.blit(self.background, (-320, -100))

        # draw welcome text
        self.screen.blit(self.startText, self.startLoc)

        # draw the start button
        pygame.draw.rect(self.screen, (207, 0, 0), self.buttonRect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.buttonRectOutline, 2)
        self.screen.blit(self.startButton, self.buttonLoc)

        pygame.display.flip()
        self.start_up()

    def start_up(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # when the user clicks the start button, change to the playing state
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttonRect.collidepoint(event.pos):
                        Poker().run()
                        return


class Poker:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Poker Game")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('img/background.jpg')
        self.screen.blit(self.background, (0, 0))
        self.suits = ['C', 'H', 'D', 'S']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        self.font = pygame.font.Font(None, 30)
        self.card_images = {}
        for suit in self.suits:
            for rank in self.ranks:
                self.card_images[(rank, suit)] = load_image(rank+suit)
        self.deck = self.generate_deck()
        self.player_hand = []
        self.ai1_hand = []
        self.ai2_hand = []
        self.ai3_hand = []
        self.money = 1000  # Стартовая сумма денег у игрока
        self.bet = 0
        self.timer = 10  # Таймер для сброса карт после 10 секунд
        self.timer_active = False  # Флаг для активации таймера
        self.move = 0
        self.current_bet = 0
        self.small_blind = 5
        self.big_blind = 10
        self.deal_cards()
        self.gui_manager = pygame_gui.UIManager((width, height))

        # Добавлен слайдер для выбора ставки
        self.bet_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((width//2 + 100, height - 20), (150, 20)),
                                                       start_value=0, value_range=(0, self.money), manager=self.gui_manager)
        self.bet_slider.hide()
        self.button_make_bet = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width//2 + 100, height-100), (150, 30)),
                                                            text='Make Bet', manager=self.gui_manager, visible=False)
        self.slider_value_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width//2 + 100, 740), (150, 30)),
            text="Your Bet: 0",
            manager=self.gui_manager,
            visible=False
        )
        self.button_call = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 + 100, height - 50), (100, 30)),
            text='Call', manager=self.gui_manager, visible=False)
        self.button_raise = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 + 100, height - 100), (100, 30)),
            text='Raise', manager=self.gui_manager, visible=False)

    def generate_deck(self):
        deck = [(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(deck)
        return deck[:13]

    def draw_card(self):
        x, y = 0, 0
        for offset, card in enumerate(self.player_hand):
            x, y = width // 2 - 100 + offset * 100, height-100
            self.screen.blit(self.card_images[card], (x, y))
        for offset, card in enumerate(self.ai1_hand):
            x, y = 0, height // 2 - 100 + offset * 100
            img = load_image('back')
            img = pygame.transform.rotate(img, 90)
            self.screen.blit(img, (x, y))
        for offset, card in enumerate(self.ai2_hand):
            x, y = width // 2 - 100 + offset * 100, 0
            self.screen.blit(load_image('back'), (x, y))
        for offset, card in enumerate(self.ai3_hand):
            x, y = width-140, height // 2 - 100 + offset * 100
            img = load_image('back')
            img = pygame.transform.rotate(img, -90)
            self.screen.blit(img, (x, y))

    def deal_cards(self):
        for offset in range(2):
            card = self.deck.pop()
            self.player_hand.append(card)
            card = self.deck.pop()
            self.ai1_hand.append(card)
            card = self.deck.pop()
            self.ai2_hand.append(card)
            card = self.deck.pop()
            self.ai3_hand.append(card)
        self.draw_card()
        print(self.deck)

    def draw_money(self):
        font = pygame.font.Font(None, 36)
        money_text = font.render(f"Money: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))

    def reset_game(self):
        self.deck = self.generate_deck()
        self.player_hand = []
        self.ai1_hand = []
        self.ai2_hand = []
        self.ai3_hand = []
        self.bet = 0
        self.timer = 10
        self.timer_active = False
        self.deal_cards()

    def make_bet(self):
        bet = int(self.bet_slider.get_current_value())
        if self.current_bet < bet <= self.money:
            self.money -= bet
            self.bet = bet
            self.button_make_bet.visible = False
            self.bet_slider.hide()
            self.timer_active = False
            self.timer = 10

    def run(self):
        while True:
            time_delta = self.clock.tick(30) / 1000.0  # Обновление времени для pygame_gui
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.bet_slider:
                        slider_value = int(self.bet_slider.get_current_value())
                        self.slider_value_text.visible = True
                        self.slider_value_text.set_text(f"Your Bet: {slider_value}")
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_call:
                        self.button_call.visible = False
                        self.button_raise.visible = False
                        self.move = (self.move + 1) % 4
                        self.timer_active = False
                        self.timer = 10
                    if event.ui_element == self.button_raise:
                        self.button_raise.visible = False
                        self.button_call.visible = False
                        self.button_make_bet.visible = True
                        self.bet_slider.value_range = (self.current_bet, self.money)
                        self.bet_slider.show()
                        self.move = (self.move + 1) % 4
                    if event.ui_element == self.button_make_bet:
                        self.make_bet()
                self.gui_manager.process_events(event)
            if self.move == 0:
                self.timer_active = True
                self.button_raise.visible = True
                self.button_call.visible = True
            self.screen.blit(self.background, (0, 0))
            self.draw_card()
            self.draw_money()
            if self.timer_active:
                self.timer -= time_delta
                if self.timer <= 0:
                    self.reset_game()

            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.screen)  # Отрисовка элементов pygame_gui
            pygame.display.flip()


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

