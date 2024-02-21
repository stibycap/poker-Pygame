import pygame
import random
import copy

pygame.init()

w = 1000
h = 1000
screen = pygame.display.set_mode([w, h])
pygame.display.set_caption('Blackjack')
fps = 60
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)

records = [0, 0, 0]
player = 0
AI = 0
result = 0
player_hand = []
AI_hand = []
game_cards = []
results = ['', 'Вы проиграли!', 'Вы выиграли!', 'ИИ выиграл!', 'Ничья!']
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card = 4 * cards
decks = 4


def draw_game(act_, record, result_):
    btn = []
    if not act_:
        sd = pygame.draw.rect(screen, 'white', [350, 350, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [350, 350, 300, 100], 3, 5)
        tx = font.render('НАЧАТЬ', True, 'black')
        screen.blit(tx, (405, 385))
        btn.append(sd)
    else:
        sd1 = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'red', [0, 700, 300, 100], 3, 5)
        tx1 = font.render('ВЗЯТЬ', True, 'black')
        screen.blit(tx1, (55, 735))
        btn.append(sd1)
        sd2 = pygame.draw.rect(screen, 'white', [350, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'red', [350, 700, 300, 100], 3, 5)
        tx2 = font.render('СТОП', True, 'black')
        screen.blit(tx2, (430, 735))
        btn.append(sd2)
        tx3 = smaller_font.render(f'Побед: {record[0]}  Проигрышей: {record[1]}  Ничьи: {record[2]}', True, 'red')
        screen.blit(tx3, (15, 840))
    if result != 0:
        screen.blit(font.render(results[result_], True, 'blue'), (15, 25))
        sd3 = pygame.draw.rect(screen, 'white', [700, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'red', [700, 700, 300, 100], 3, 5)
        tx4 = font.render('НОВАЯ ИГРА', True, 'black')
        screen.blit(tx4, (705, 735))
        btn.append(sd3)
    return btn


def draw_scores(player_, AI_):
    screen.blit(font.render(f'Очки:{player_}', True, 'red'), (350, 400))
    if reveal_AI:
        screen.blit(font.render(f'Очки:{AI_}', True, 'red'), (350, 100))


def draw_cards(player_, AI_, card_):
    for i in range(len(player_)):
        pygame.draw.rect(screen, 'green', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player_[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player_[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    for i in range(len(AI_)):
        pygame.draw.rect(screen, 'green', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or card_:
            screen.blit(font.render(AI_[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(AI_[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('?', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('?', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


def deal_cards(qw, d):
    card1 = random.randint(0, len(d))
    qw.append(d[card1 - 1])
    d.pop(card1 - 1)
    return qw, d


def calcul(q):
    sc = 0
    ac = q.count('A')
    for i in range(len(q)):
        for j in range(8):
            if q[i] == cards[j]:
                sc += int(q[i])
        if q[i] in ['10', 'J', 'Q', 'K']:
            sc += 10
        elif q[i] == 'A':
            sc += 11
    if sc > 21 and ac > 0:
        for i in range(ac):
            if sc > 21:
                sc -= 10
    return sc


def end(sd, AI_, player_, res, total, add):
    if not sd and AI_ >= 17:
        if player_ > 21:
            res = 1
        elif AI_ < player_ <= 21 or AI_ > 21:
            res = 2
        elif player_ < AI_ <= 21:
            res = 3
        else:
            res = 4
        if add:
            if res == 1 or res == 3:
                total[1] += 1
            elif res == 2:
                total[0] += 1
            else:
                total[2] += 1
            add = False
    return res, total, add


act = False
start = False
reveal_AI = False
hand_active = False
add_score = False

run = True
while run:
    screen.fill('yellow')
    if start:
        for i in range(2):
            player_hand, game_cards = deal_cards(player_hand, game_cards)
            AI_hand, game_cards = deal_cards(AI_hand, game_cards)
        start = False
    if act:
        player = calcul(player_hand)
        draw_cards(player_hand, AI_hand, reveal_AI)
        if reveal_AI:
            AI = calcul(AI_hand)
            if AI < 17:
                AI_hand, game_cards = deal_cards(AI_hand, game_cards)
        draw_scores(player, AI)
    buttons = draw_game(act, records, result)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not act:
                if buttons[0].collidepoint(event.pos):
                    act = True
                    start = True
                    game_cards = copy.deepcopy(decks * card)
                    player_hand = []
                    AI_hand = []
                    result = 0
                    hand_active = True
                    reveal_AI = False
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player < 21 and hand_active:
                    player_hand, game_cards = deal_cards(player_hand, game_cards)
                elif buttons[1].collidepoint(event.pos) and not reveal_AI:
                    reveal_AI = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        start = True
                        game_cards = copy.deepcopy(decks * card)
                        player_hand = []
                        AI_hand = []
                        result = 0
                        hand_active = True
                        reveal_AI = False
                        add_score = True
                        AI_score = 0
                        player_score = 0

    if hand_active and player >= 21:
        hand_active = False
        reveal_AI = True

    result, records, add_score = end(hand_active, AI, player, result, records, add_score)

    pygame.display.flip()
pygame.quit()
