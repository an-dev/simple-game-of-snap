from random import random, randrange, shuffle, randint
from time import sleep

VALUES     = ['1','2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
SUITS      = ['Spades','Hearts','Diamonds','Clubs']
    

class Player(object):
    
    def __init__(self, cards=[], name=''):
        self.cards = cards
        self.name  = name

    def get_card_num(self):
        return len(self.cards)

    def __str__(self):
        return 'Player %s with %s cards' % (self.name, self.get_card_num())


class Game(object):

   
    def _same_suit_condition(c1, c2):
        return None if not c2 else c1['suit'] == c2['suit']

    def _same_symbol_condition(c1, c2):
        return None if not c2 else c1['value'] == c2['value']

    def _same_card_condition(c1, c2):
        return None if not c2 else (c1['value'] == c2['value'] or c1['suit'] == c2['suit'])
    
    # I'm sure there's a better way to do this but it's 2am
    # so whatever
    CONDITIONS = {
        1: _same_suit_condition,
        2: _same_symbol_condition,
        3: _same_card_condition
    }
    

    def __init__(self, N, C):
        self.number_packs = int(N)
        self.condition    = self.CONDITIONS[int(C)]
        self.p1           = Player(name='Foo')
        self.p2           = Player(name='Bar')
        self.pile         = []
        self.discard_pile = []
    
    def _prepare_pile(self):
        for i in range(self.number_packs):
            shuffle(SUITS)
            suit = SUITS.pop()
            for value in VALUES:
                self.pile.append({
                    'value':value,
                    'suit':suit
                })

        shuffle(self.pile)
        self.pile.reverse()
        
    def _get_winner(self):
        if self.p1.get_card_num() == self.p2.get_card_num():
            return 'No clear winner'
        else:
            if self.p1.get_card_num() > self.p2.get_card_num():
                return 'The winner is %s (Player1)' % self.p1
            else:
                return 'The winner is %s (Player2)' % self.p2


    def play(self):
        self._prepare_pile()
        prev_card = None

        p1 = []
        p2 = []
    
        # game logic
        while len(self.pile) > 0:
            
            current_card = self.pile.pop()
            
            print 'Drawn card %s' % current_card
            print 'Last card drawn was %s\n\n' % prev_card
            
            self.discard_pile.append(current_card)

            if self.condition(current_card, prev_card):
                print 'Condition is met! The discard pile goes to...\n\n'
                
                if randint(0, 1) == 1:
                    p1.extend(self.discard_pile)
                    print 'Player1!'
                else:
                    p2.extend(self.discard_pile)
                    print 'Player2!'
                self.discard_pile = []
            else:
                print 'Condition not met! Into the trash it goes...\n\n'
            prev_card = current_card
            print '=============================================\n\n'
            sleep(1)
        
        self.p1.cards, self.p2.cards = p1,p2

        print self._get_winner()

if __name__ == '__main__':

    packs_choices = ['1','2','3','4']
    condition_choices = ['1','2','3']

    while True:
        N = raw_input('How many packs of cards to use? (choose from 1/2/3/4)\n')
        C = raw_input('Which of the three matching conditions to use? (choose from:\
            \n\t1 Cards have same suit\n\t2 Cards have same value\n\t3 Cards have same suit OR value)\n')
        
        if N not in packs_choices or C not in condition_choices:
            print 'Ehm...some parameters are wrong...Try again...'
        else:
            break

    game = Game(N, C)
    game.play()
