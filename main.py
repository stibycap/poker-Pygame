import pygame
import os
import random
import sys
import pygame_gui
import operator
import animat
from TeammateCode import Code


def load_image(name):
    fullname = os.path.join('img', name + '.png')
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


width = 1200
height = 675
pygame.init()
check = pygame.mixer.Sound('audio/check.ogg')
dealCard = pygame.mixer.Sound('audio/dealCard.MP3')
dealChip = pygame.mixer.Sound('audio/dealChip.MP3')
fold = pygame.mixer.Sound('audio/fold.MP3')
grab = pygame.mixer.Sound('audio/grab chips.MP3')
new_card = pygame.mixer.Sound('audio/new card.MP3')
win = pygame.mixer.Sound('audio/win.MP3')


class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Start Screen")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.poker_button = pygame.Rect(50, 200, 200, 50)
        self.blackjack_button = pygame.Rect(50, 300, 200, 50)
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.poker_button.collidepoint(event.pos):
                        PokerStart()
                    elif self.blackjack_button.collidepoint(event.pos):
                        game = Code()
                        game.run()

            self.screen.fill((255, 255, 255))

            pygame.draw.rect(self.screen, (0, 255, 0), self.poker_button)
            pygame.draw.rect(self.screen, (0, 0, 255), self.blackjack_button)

            poker_text = self.font.render("Poker", True, (255, 255, 255))
            blackjack_text = self.font.render("Blackjack", True, (255, 255, 255))

            self.screen.blit(poker_text, (self.poker_button.x + 50, self.poker_button.y + 15))
            self.screen.blit(blackjack_text, (self.blackjack_button.x + 20, self.blackjack_button.y + 15))

            pygame.display.flip()
            self.clock.tick(30)


class PokerStart:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font('font/CoffeeTin.ttf', 150)
        self.font2 = pygame.font.Font('font/IndianPoker.ttf', 75)
        self.background = pygame.image.load('img/background.jpg')
        self.font2.set_bold(True)
        self.startText = self.font2.render("Welcome to Poker!", True, (0, 0, 0))
        self.startSize = self.font2.size("Welcome to Poker!")
        self.startLoc = (width / 2 - self.startSize[0] / 2, 50)
        self.startButton = self.font.render(" Start ", True, (0, 0, 0))
        self.buttonSize = self.font.size(" Start ")
        self.buttonLoc = (width / 2 - self.buttonSize[0] / 2, height / 2 - self.buttonSize[1] / 2)
        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.screen.blit(self.background, (-320, -100))
        self.screen.blit(self.startText, self.startLoc)
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


class PokerEnd:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font('font/CoffeeTin.ttf', 150)
        self.font2 = pygame.font.Font('font/IndianPoker.ttf', 75)
        self.background = pygame.image.load('img/background.jpg')
        self.font2.set_bold(True)

        self.startText = self.font2.render("Welcome to Poker!", True, (0, 0, 0))
        self.startSize = self.font2.size("Welcome to Poker!")
        self.startLoc = (width / 2 - self.startSize[0] / 2, 50)

        self.startButton = self.font.render(" Play again ", True, (0, 0, 0))
        self.buttonSize = self.font.size(" Play again ")
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
        self.run()

    def run(self):
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
        self.background = pygame.image.load('img/green-table.png')
        self.background = pygame.transform.scale(self.background, (width, height))
        self.dealer = load_image('dealerchip')
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
        self.raise_mod = False
        self.ai1_money = 1000
        self.ai1_bet = 0
        self.ai2_money = 1000
        self.ai2_bet = 0
        self.ready = [False, False, False]
        self.money = 1000
        self.bet = 0
        self.allChips = 0
        self.timer = 10
        self.timer_active = False
        self.move = 0
        self.startMove = random.randint(0, 2)
        self.round = 0
        self.current_bet = 0
        self.blinds = [10, 5, 0]
        self.cur_players = 3
        self.deal_cards()
        self.k = 0
        self.gui_manager = pygame_gui.UIManager((width, height))
        self.reset = False
        self.reset_count = 0
        self.starter = self.startMove
        self.win = False
        self.total_rounds = 0
        self.combs = False
        self.buttonRect = pygame.Rect((400, 50), (80, 100))

        self.bet_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((width//2 + 100, height - 20), (150, 20)),
                                                                 start_value=0, value_range=(0, self.money), manager=self.gui_manager)
        self.bet_slider.hide()
        self.button_make_bet = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width//2 + 100, height-100), (150, 30)),
                                                            text='Make Bet', manager=self.gui_manager, visible=False)
        self.slider_value_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width//2 + 100, 740), (150, 30)),
            text="Your Bet: 0", manager=self.gui_manager, visible=False
        )
        self.player_action = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((550, 600), (40, 30)), text="",
            manager=self.gui_manager, visible=False
        )
        self.ai1_action = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 270), (40, 30)), text="",
            manager=self.gui_manager, visible=False
        )
        self.ai2_action = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((1000, 270), (40, 30)), text="",
            manager=self.gui_manager, visible=False
        )
        self.winner = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((400, 80), (300, 30)), text="",
            manager=self.gui_manager, visible=False
        )
        self.winner.text_colour = 'red'
        self.button_call = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 + 100, height - 65), (100, 30)),
            text='Call', manager=self.gui_manager, visible=False)
        self.button_raise = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 + 100, height - 100), (100, 30)),
            text='Raise', manager=self.gui_manager, visible=False)
        self.button_fold = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 + 100, height - 30), (100, 30)),
            text='Fold', manager=self.gui_manager, visible=False)

    def generate_deck(self):
        deck = [(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(deck)
        return deck[:11]

    def draw_card(self, win=False):
        for offset, card in enumerate(self.player_hand):
            img = self.card_images[card]
            x, y = width // 2 - 120 + offset * 80, height - 280
            if offset == 0:
                img = pygame.transform.rotate(img, 10)
            else:
                img = pygame.transform.rotate(img, -10)
            img = pygame.transform.scale(img, (img.get_width() / 1.2, img.get_height() / 1.2))
            self.screen.blit(img, (x, y))
        for offset, card in enumerate(self.ai1_hand):
            x, y = width // 5, height // 2 - 100 + offset * 50
            img = load_image('back')
            img = pygame.transform.rotate(img, 90)
            img = pygame.transform.scale(img, (img.get_width() / 1.7, img.get_height() / 1.7))
            self.screen.blit(img, (x, y))
        for offset, card in enumerate(self.ai2_hand):
            x, y = width - 380, height // 2 - 100 + offset * 50
            img = load_image('back')
            img = pygame.transform.rotate(img, -90)
            img = pygame.transform.scale(img, (img.get_width() / 1.7, img.get_height() / 1.7))
            self.screen.blit(img, (x, y))
            self.screen.blit(img, (x, y))
        if win:
            for offset, card in enumerate(self.player_hand):
                img = self.card_images[card]
                x, y = width // 2 - 120 + offset * 80, height - 280
                if offset == 0:
                    img = pygame.transform.rotate(img, 10)
                else:
                    img = pygame.transform.rotate(img, -10)
                img = pygame.transform.scale(img, (img.get_width() / 1.2, img.get_height() / 1.2))
                self.screen.blit(img, (x, y))
            for offset, card in enumerate(self.ai1_hand):
                x, y = width // 5, height // 2 - 100 + offset * 50
                img = self.card_images[card]
                img = pygame.transform.rotate(img, 90)
                img = pygame.transform.scale(img, (img.get_width() / 1.7, img.get_height() / 1.7))
                self.screen.blit(img, (x, y))
            for offset, card in enumerate(self.ai2_hand):
                x, y = width - 380, height // 2 - 100 + offset * 50
                img = self.card_images[card]
                img = pygame.transform.rotate(img, -90)
                img = pygame.transform.scale(img, (img.get_width() / 1.7, img.get_height() / 1.7))
                self.screen.blit(img, (x, y))
                self.screen.blit(img, (x, y))

    def deal_cards(self):
        for offset in range(2):
            card = self.deck.pop()
            if self.money:
                self.player_hand.append(card)
            else:
                self.cur_players -= 0.5
            card = self.deck.pop()
            if self.ai1_money:
                self.ai1_hand.append(card)
            else:
                self.cur_players -= 0.5
            card = self.deck.pop()
            if self.ai2_money:
                self.ai2_hand.append(card)
            else:
                self.cur_players -= 0.5
        self.cur_players = int(self.cur_players)
        if self.cur_players == 1:
            self.win = True
        elif self.cur_players == 2:
            self.blinds.pop()
            dealCard.play()
        else:
            dealCard.play()
        self.draw_card()

    def draw_money(self):
        font = pygame.font.Font('font/IndianPoker.ttf', 25)
        money_text = font.render(f"Money: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))
        stav_text = font.render(f"{self.allChips}", True, (255, 255, 255))
        self.screen.blit(stav_text, (550, 175))
        player = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(player, (540, 530))
        ai1 = font.render(f"{self.ai1_money}", True, (0, 0, 0))
        self.screen.blit(ai1, (260, 200))
        ai2 = font.render(f"{self.ai2_money}", True, (0, 0, 0))
        self.screen.blit(ai2, (840, 200))

    def reset_game(self):
        self.reset = False
        self.deck = self.generate_deck()
        self.total_rounds += 1
        self.player_hand = []
        self.ai1_hand = []
        self.ai2_hand = []
        self.cur_players = 3
        self.allChips = 0
        self.round = 0
        self.startMove = (self.starter + 1) % 3
        self.timer_active = False
        self.winner.visible = False
        if self.total_rounds % 3 == 0:
            self.up_blinds()
        self.deal_cards()
        self.start()

    def make_bet(self):
        bet = int(self.bet_slider.get_current_value())
        self.money -= bet - self.bet
        self.bet = bet
        self.current_bet = bet
        self.button_make_bet.visible = False
        self.bet_slider.hide()
        self.timer_active = False
        self.timer = 10
        self.player_action.set_text("raise")
        self.move = (self.move + 1) % 3
        self.raise_mod = False
        dealChip.play()

    def call(self):
        if self.move == 0:
            self.button_call.visible = False
            self.button_raise.visible = False
            self.button_fold.visible = False
            self.move = (self.move + 1) % 3
            self.timer_active = False
            self.timer = 10
            if self.current_bet == self.bet:
                self.player_action.set_text("check")
                check.play()
            elif self.current_bet < self.money:
                bet = self.current_bet
                self.money -= bet - self.bet
                self.bet = self.current_bet
                self.player_action.set_text("call")
                dealChip.play()
            else:
                self.bet += self.money
                self.player_action.set_text("call")
                self.money = 0
                dealChip.play()
            self.player_action.visible = True
            self.ready[0] = True
        elif self.move == 1:
            self.move = (self.move + 1) % 3
            self.timer_active = False
            self.timer = 10
            if self.current_bet == self.ai1_bet:
                self.ai1_action.set_text("check")
                check.play()
            elif self.current_bet < self.ai1_money:
                bet = self.current_bet
                self.ai1_money -= bet - self.ai1_bet
                self.ai1_bet = self.current_bet
                self.ai1_action.set_text("call")
                dealChip.play()
            else:
                bet = self.ai1_money
                self.ai1_money = 0
                self.ai1_bet += bet
                self.ai1_action.set_text("call")
                dealChip.play()
            self.ai1_action.visible = True
            self.ready[1] = True
        elif self.move == 2:
            self.move = (self.move + 1) % 3
            self.timer_active = False
            self.timer = 10
            if self.current_bet == self.ai2_bet:
                self.ai2_action.set_text("check")
                check.play()
            elif self.current_bet < self.ai1_money:
                bet = self.current_bet
                self.ai2_money -= bet - self.ai2_bet
                self.ai2_bet = self.current_bet
                self.ai2_action.set_text("call")
                dealChip.play()
            else:
                self.ai2_bet += self.ai2_money
                self.ai2_action.set_text("call")
                self.ai2_money = 0
                dealChip.play()
            self.ai2_action.visible = True
            self.ready[2] = True

    def raise_bet(self):
        if self.move == 0:
            self.raise_mod = True
            self.button_raise.visible = False
            self.button_call.visible = False
            self.button_fold.visible = False
            self.button_make_bet.visible = True
            self.bet_slider.value_range = (self.current_bet, self.money+self.bet)
            self.bet_slider.show()
        elif self.move == 1:
            if self.ai1_money > self.current_bet:
                bet = random.randint(self.current_bet, self.ai1_money)
            else:
                bet = self.ai1_money
            self.ai1_money -= bet + self.ai1_bet
            self.ai1_bet = bet
            self.current_bet = bet
            self.move = (self.move + 1) % 3
            self.timer_active = False
            self.timer = 10
            self.ai1_action.set_text("raise")
            self.ready[1] = True
            self.ready[0] = False
            self.ready[2] = False
            dealChip.play()
        elif self.move == 2:
            if self. ai2_money > self.current_bet:
                bet = random.randint(self.current_bet, self.ai2_money)
            else:
                bet = self.ai2_money
            self.ai2_money -= bet + self.ai2_bet
            self.ai2_bet = bet
            self.current_bet = bet
            self.move = (self.move + 1) % 3
            self.timer_active = False
            self.timer = 10
            self.ai2_action.set_text("raise")
            self.ready[2] = True
            self.ready[0] = False
            self.ready[1] = False
            dealChip.play()

    def fold(self):
        if self.move == 0:
            self.timer = 10
            self.timer_active = False
            self.player_hand = []
            self.player_action.visible = True
            self.player_action.set_text("fold")
            self.ready[0] = True
        elif self.move == 1:
            self.ai1_hand = []
            self.timer = 10
            self.timer_active = False
            self.ai1_action.visible = True
            self.ai1_action.set_text("fold")
            self.ready[1] = True
        elif self.move == 2:
            self.ai2_hand = []
            self.timer = 10
            self.timer_active = False
            self.ai2_action.visible = True
            self.ai2_action.set_text('fold')
            self.ready[2] = True
        self.cur_players -= 1
        self.move = (self.move + 1) % 3
        fold.play()

    def draw_bet(self):
        font = pygame.font.Font(None, 36)
        player_bet = font.render(f"{int(self.bet)}", True, (0, 0, 0))
        self.screen.blit(player_bet, (550, 370))
        ai1_bet = font.render(f"{int(self.ai1_bet)}", True, (0, 0, 0))
        self.screen.blit(ai1_bet, (350, 250))
        ai2_bet = font.render(f"{int(self.ai2_bet)}", True, (0, 0, 0))
        self.screen.blit(ai2_bet, (770, 250))

    def move_logic(self):
        if self.cur_players == 1 and not self.reset:
            self.bank()
            self.round = 4
            self.next_round()
            self.player_action.visible = False
            self.ai1_action.visible = False
            self.ai2_action.visible = False
        if self.move == 0:
            if not self.player_hand or self.money == 0:
                self.move = (self.move + 1) % 3
                self.ready[0] = True
                return
            font = pygame.font.Font(None, 36)
            timer = font.render(f"{int(self.timer)}", True, (255, 255, 255))
            self.screen.blit(timer, (700, 500))
            if not self.raise_mod:
                self.timer_active = True
                if self.money > self.current_bet:
                    self.button_raise.visible = True
                self.button_call.visible = True
                if self.current_bet == self.bet:
                    self.button_call.set_text('Check')
                else:
                    self.button_call.set_text('Call')
                self.button_fold.visible = True
        elif self.move == 1:
            if not self.ai1_hand or self.ai1_money == 0:
                self.move = (self.move + 1) % 3
                self.ready[1] = True
                return
            font = pygame.font.Font(None, 36)
            timer = font.render(f"{int(self.timer)}", True, (255, 255, 255))
            self.timer_active = True
            self.screen.blit(timer, (400, 300))
            self.button_raise.visible = False
            self.button_call.visible = False
            self.button_fold.visible = False
            self.k += 1
            if self.k > 75:
                a = random.random()
                if a > 0.95:
                    self.raise_bet()
                elif a > 0.8:
                    self.fold()
                else:
                    self.call()
                self.k = 0
        elif self.move == 2:
            if not self.ai2_hand or self.ai2_money == 0:
                self.move = (self.move + 1) % 3
                self.ready[2] = True
                return
            font = pygame.font.Font(None, 36)
            timer = font.render(f"{int(self.timer)}", True, (255, 255, 255))
            self.timer_active = True
            self.screen.blit(timer, (800, 300))
            self.button_raise.visible = False
            self.button_call.visible = False
            self.button_fold.visible = False
            self.k += 1
            if self.k > 75:
                a = random.random()
                if a > 0.95:
                    self.raise_bet()
                elif a > 0.8:
                    self.fold()
                else:
                    self.call()
                self.k = 0
        elif self.move == -1:
            font = pygame.font.Font(None, 50)
            timer = font.render(f"{int(self.reset_count)}", True, (255, 255, 255))
            self.screen.blit(timer, (500, 300))

    def start(self):
        if self.startMove == 0:
            if not self.player_hand:
                self.startMove = (self.startMove + 1) % 3
                self.start()
                return
            self.move = 0
        elif self.startMove == 1:
            if not self.ai1_hand:
                self.startMove = (self.startMove + 1) % 3
                self.start()
                return
            self.move = 1
        elif self.startMove == 2:
            if not self.ai2_hand:
                self.startMove = (self.startMove + 1) % 3
                self.start()
                return
            self.move = 2
        self.starter = self.startMove
        if self.money:
            self.bet = self.blinds[(self.starter + 2) % len(self.blinds)]
        if self.ai1_money:
            self.ai1_bet = self.blinds[(self.starter + 1) % len(self.blinds)]
        if self.ai2_money:
            self.ai2_bet = self.blinds[self.starter]
        self.money -= self.bet
        self.ai1_money -= self.ai1_bet
        self.ai2_money -= self.ai2_bet
        self.current_bet = self.blinds[0]

    def next_round(self):
        if self.startMove == 0:
            if not self.player_hand:
                self.startMove = (self.startMove + 1) % 3
                self.next_round()
            self.move = 0
            self.bet = 0
            self.ai1_bet = 0
            self.ai2_bet = 0
        elif self.startMove == 1:
            if not self.ai1_hand:
                self.startMove = (self.startMove + 1) % 3
                self.next_round()
            self.move = 1
            self.ai1_bet = 0
            self.ai2_bet = 0
            self.bet = 0
        elif self.startMove == 2:
            if not self.ai2_hand:
                self.startMove = (self.startMove + 1) % 3
                self.next_round()
            self.move = 2
            self.ai1_bet = 0
            self.ai2_bet = 0
            self.bet = 0
        grab.play()
        self.current_bet = 0

    def deal_chip(self):
        if self.starter == 0:
            self.screen.blit(self.dealer, (250, 300))
        elif self.starter == 1:
            self.screen.blit(self.dealer, (100, 150))
        elif self.starter == 2:
            self.screen.blit(self.dealer, (600, 150))

    def bank(self):
        self.allChips += self.bet + self.ai1_bet + self.ai2_bet

    def draw_board(self):
        if self.round == 1:
            for offset, card in enumerate(self.deck[:3]):
                img = self.card_images[card]
                x, y = width // 2 - 200 + offset * 60, 250
                img = pygame.transform.scale(img, (img.get_width() / 1.4, img.get_height() / 1.4))
                self.screen.blit(img, (x, y))
        elif self.round == 2:
            for offset, card in enumerate(self.deck[:4]):
                img = self.card_images[card]
                x, y = width // 2 - 200 + offset * 60, 250
                img = pygame.transform.scale(img, (img.get_width() / 1.4, img.get_height() / 1.4))
                self.screen.blit(img, (x, y))
        elif self.round == 3:
            for offset, card in enumerate(self.deck):
                img = self.card_images[card]
                x, y = width // 2 - 200 + offset * 60, 250
                img = pygame.transform.scale(img, (img.get_width() / 1.4, img.get_height() / 1.4))
                self.screen.blit(img, (x, y))
        elif self.round == 4:
            self.win_cond()
            self.round = 3
            self.reset = True
            self.reset_count = 5
            self.move = -1

    def next_move(self):
        if all(self.ready) and not self.reset:
            self.startMove = (self.startMove + 1) % 3
            self.bank()
            pygame.time.delay(2000)
            self.next_round()
            self.round += 1
            self.player_action.visible = False
            self.ai1_action.visible = False
            self.ai2_action.visible = False
            self.ready = [False, False, False]
            new_card.play()

    def win_cond(self):
        score1 = 0
        score2 = 0
        score3 = 0
        if self.player_hand:
            score1 = self.get_score(self.player_hand + self.deck)
        if self.ai1_hand:
            score2 = self.get_score(self.ai1_hand + self.deck)
        if self.ai2_hand:
            score3 = self.get_score(self.ai2_hand + self.deck)
        winner = max(score1, max(score2, score3))
        self.winner.visible = True
        win.play()
        if winner == score1:
            self.winner.set_text('player победил с комбинацией ' + self.convert_score(score1))
            self.money += self.allChips
        elif winner == score2:
            self.winner.set_text('ai1 победил с с комбинацией ' + self.convert_score(score2))
            self.ai1_money += self.allChips
        elif winner == score3:
            self.winner.set_text('ai2 победил с с комбинацией ' + self.convert_score(score3))
            self.ai2_money += self.allChips
        for i in range(10):
            x = random.randint(0, width)
            y = random.randint(0, height)
            animat.create_particles((x, y))
        return [score1, score2, score3]

    def get_score(self, hand):
        card_count = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        suit_count = {'C': 0, 'D': 0, 'H': 0, 'S': 0}
        for card in hand:
            card_count[int(card[0])] += 1
        for card in hand:
            suit_count[card[1]] += 1
        unique_count = 0
        for rankCount in card_count.values():
            if rankCount > 0:
                unique_count += 1
        straight = self.is_straight(hand)
        flush = False
        for i in suit_count.values():
            if i >= 5:
                flush = True
        points = 0
        if straight and flush:
            points = max(points, 9)  # straight flush
        elif unique_count == 4:
            if max(card_count.values()) == 4:
                points = 8
            elif max(card_count.values()) == 3:
                points = 7
        elif flush and not straight:
            points = max(points, 6)
        elif not flush and straight:
            points = max(points, 5)
        elif unique_count == 3:
            if max(card_count.values()) == 4:
                points = 8
            elif max(card_count.values()) == 3:
                points = 7
        elif unique_count == 5:
            if max(card_count.values()) == 3:
                points = 4
            elif max(card_count.values()) == 2:
                points = 3
        elif unique_count == 6:
            points = 2
        elif unique_count == 7:
            points = 1
        sorted_card = sorted(card_count.items(), key=operator.itemgetter(1, 0), reverse=True)
        for keyval in sorted_card:
            if keyval[1] != 0:
                points = int(str(points) + (keyval[1] * str(keyval[0]).zfill(2)))
        return int(str(points)[:11])

    def convert_score(self, score):
        if str(score)[0] == '1':
            return "Старшая карта"
        elif str(score)[0] == '2':
            return "Пара"
        elif str(score)[0] == '3':
            return "Две пары"
        elif str(score)[0] == '4':
            return "Тройка"
        elif str(score)[0] == '5':
            return "Стрит"
        elif str(score)[0] == '6':
            return "Флэш"
        elif str(score)[0] == '7':
            return "Фулл хаус"
        elif str(score)[0] == '8':
            return "Каре"
        elif str(score)[0] == '9':
            return "Стрит флэш"

    def is_straight(self, hand):
        values = []
        for card in hand:
            values.append(int(card[0]))
        values.sort()
        for i in range(0, 4):
            if values[i] + 1 != values[i + 1]:
                return False
        return True

    def up_blinds(self):
        self.blinds[0] = self.blinds[0] * 2
        self.blinds[1] = self.blinds[1] * 2

    def show_combs(self):
        if self.combs:
            self.combs = False
            self.buttonRect = pygame.Rect((400, 50), (80, 100))
        else:
            self.combs = True
            self.buttonRect = pygame.Rect((1000, 50), (70, 100))
        return

    def run(self):
        self.start()
        while True:
            time_delta = self.clock.tick(30) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.bet_slider:
                        slider_value = int(self.bet_slider.get_current_value())
                        self.slider_value_text.visible = True
                        self.slider_value_text.set_text(f"Your Bet: {slider_value}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttonRect.collidepoint(event.pos):
                        self.show_combs()
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_call:
                        self.call()
                    if event.ui_element == self.button_raise:
                        self.raise_bet()
                    if event.ui_element == self.button_make_bet:
                        self.make_bet()
                    if event.ui_element == self.button_fold:
                        self.fold()
                self.gui_manager.process_events(event)
            animat.all_sprites.update()
            self.screen.blit(self.background, (0, 0))
            animat.all_sprites.draw(self.screen)
            if self.move % 3 == self.startMove:
                self.next_move()
            self.deal_chip()
            self.move_logic()
            self.draw_bet()
            if not self.reset:
                self.draw_card()
            else:
                self.draw_card(win=True)
            self.draw_board()
            self.draw_money()
            if self.combs:
                img = load_image('combs')
                img = pygame.transform.scale(img, (img.get_width() / 1.3, img.get_height() / 1.3))
                self.screen.blit(img, (100, 0))
            if self.timer_active:
                self.timer -= time_delta
                if self.timer <= 0:
                    self.fold()
            if self.reset:
                self.reset_count -= time_delta
                if self.reset_count <= 0:
                    self.reset_game()
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()
            if self.win:
                win.play()
                PokerEnd()
                return


StartScreen()
