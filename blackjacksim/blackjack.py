import numpy as np
import pandas as pd
from .strategy import read_strategy
from .deck import deck_setup
from .analysis import plot_hist, sim_stats



class Simulator(object):
    def __init__(self, bet_size, strategy_name="basic_strategy"):
        """
        BlackJack Simulator.

        Parameters
        ----------
        bet_size: float
            size of the bet per game.

        strategy_name: str, default="basic_strategy"
            name of the strategy contained in a csv in the
            "/strategy" subdirectory.
        """
        # inital bet size
        self.initial_bet_size = bet_size
        # current bet size (may be larger than the inital bet size in some cases)
        self.bet = self.initial_bet_size
        # three strategies
        self.strategy_h, self.strategy_s, self.strategy_p = read_strategy(strategy_name)
        # initalize deck
        self.deck = deck_setup()
        # player hand and House hand (initialize a large array)
        self.p_hand = np.zeros((4, 20), dtype=int)
        self.h_hand = np.zeros((1, 20), dtype=int)
        # first House draw is the "face-up" card
        self.h_faceup = 0
        # indicator for number of splits (max 3)
        self.n_sp = 0
        # index for the hand currently in play (used for splits)
        self.c_sp = 0


    def playgames(self, num_games=1000):
        """
        Simulate n independent games of BlackJack using the given strategy.

        Parameters
        ----------
        num_games: int, default=1000
            number of games to simulate for a given strategy.
        """
        # results
        self.winnings = 0
        self.results = np.zeros(num_games)

        for n in range(num_games):
            self._deal_to_player(num_cards=2)
            self._deal_to_house(num_cards=2)
            # first House draw is the "face-up" card
            self.h_faceup = self.h_hand[0,0].astype(int)
            self._play()
            self.results[n] = self.winnings
            self._reset()


    def summary(self, plots=True):
        """
        Print descriptive statistics on simulation results.

        Parameters
        ----------
        plots: bool, default=True
            Optional histogram plot.
        """
        sim_stats(self.results)
        plot_hist(self.results)


    ### private methods ###

    def _deal_to_player(self, num_cards):
        """
        Deal face-up cards to the player.

        Parameters
        ----------
        num_cards: int
            number of cards to deal
        """
        # draw n random cards from the deck (without replacement)
        ind = np.random.choice(self.deck.shape[0], size=num_cards, replace=False)
        draw = self.deck[ind]
        # remove drawn cards from deck
        self.deck = np.delete(self.deck, ind)
        # locate the first zero index in the given hand
        zero_ind = np.argwhere(self.p_hand[self.c_sp,:]==0)[0][0]
        # add to hand
        self.p_hand[self.c_sp, zero_ind:zero_ind+num_cards] = draw


    def _deal_to_house(self, num_cards):
        """
        Deal one face-up and one face-down card to the house on first deal.
            Then one face-up card at a time after.

        Parameters
        ----------
        """
        # draw n random cards from the deck (without replacement)
        ind = np.random.choice(self.deck.shape[0], size=num_cards, replace=False)
        draw = self.deck[ind]
        # remove drawn cards from deck
        self.deck = np.delete(self.deck, ind)
        # locate the first zero index
        zero_ind = np.argwhere(self.h_hand[0,:]==0)[0][0]
        # add to hand
        self.h_hand[0, zero_ind:zero_ind+num_cards] = draw


    def _pick_strategy(self):
        """
        Pick which strategy to use based on the dealt cards.

        Parameters
        ----------
        """
        # split strategy
        if ((self.p_hand[self.c_sp,0] == self.p_hand[self.c_sp,1])
            and (self.p_hand[self.c_sp,2]==0)
            and (self.n_sp <= 3)):
            return self.strategy_p

        # soft strategy
        elif np.any(self.p_hand[self.c_sp,:] == 11):
            return self.strategy_s

        # hard strategy
        else:
            return self.strategy_h


    def _implement_move(self, move):
        """
        Pick which strategy to use based on the dealt cards.

        Parameters
        ----------
        move: str, ("h", "s", "d", "p")
            a string encoding of which move to implement.
        """
        assert move in ("h", "s", "d", "p"), "invalid move"

        # hit (recurive)
        if move == "h":
            self._deal_to_player(num_cards=1)
            self._play()

        # split (recurive)
        elif move == "p":
            # implement split
            self.n_sp += 1
            # first empty hand
            zero_ind = np.argwhere(self.p_hand[:,0]==0)[0][0]
            self.p_hand[zero_ind,0] = self.p_hand[self.c_sp,1]
            self.p_hand[self.c_sp,1] = 0
            for _ in range(2):
                self._deal_to_player(num_cards=1)
                self._play()

        # double bet (terminal condition)
        elif move == "d":
            self.bet *= 2
            # check winner and payout
            self._winner()
            self.c_sp += 1

        # stand (terminal condition)
        else:
            # check winner and payout
            self._winner()
            self.c_sp += 1


    def _implement_strategy(self):
        """
        Implement strategy based on the dealt cards.

        Parameters
        ----------
        """
        # pick a strategy based on dealt cards
        strategy = self._pick_strategy()

        # next move based on the House's face-up card
        total = self.p_hand[self.c_sp,:].sum(dtype=int)

        # check if bust
        if total > 21:
            return

        move = strategy.loc[total, self.h_faceup]
        # implement the move and return winnings
        self._implement_move(move)


    def _convert_soft_total(self, hand, ind):
        """
        Convert to soft total.

        Parameters
        ----------
        hand: np.array
            player or House hand.

        ind: int
            index of current hand.
        """
        # Calculate soft value (if applicable)
        if (hand[ind,:].sum() > 21) and (np.any(hand[ind,:] == 11)):
            # if over 21 and has ace, use soft value
            hand[ind,:] = np.where(hand[ind,:]==11, 1, hand[ind,:])
        return hand


    def _winner(self):
        """
        Check winner of game and payout bet.

        House stands on all 17s.

        Parameters
        ----------
        """
        # Proportion of total bet to wager.
        if self.n_sp == 0.:
            size = 1.
        elif self.n_sp > 0.:
            size = (self.bet/self.n_sp)/self.bet
        assert size <= 1 and size > 0

        # BlackJack check
        player_blackjack = bool(self.p_hand[self.c_sp,:2].sum()==21)
        house_blackjack = bool(self.h_hand[0,:2].sum()==21)

        if player_blackjack and house_blackjack:
            # draw
            return
        elif player_blackjack:
            self.winnings += (self.bet * size) * 1.5
            return
        elif house_blackjack:
            self.winnings -= (self.bet * size)
            return

        # Calculate soft value (if applicable)
        self.p_hand = self._convert_soft_total(self.p_hand, ind=self.c_sp)

        # Check if player bust
        if self.p_hand[self.c_sp,:].sum() > 21:
            self.winnings -= (self.bet * size)
            return

        # House hit until (all) 17
        while self.h_hand.sum() < 17:
            self._deal_to_house(num_cards=1)

        # Calculate soft value (if applicable)
        self.h_hand = self._convert_soft_total(self.h_hand, ind=0)

        # Check if House bust
        if self.h_hand.sum() > 21:
            self.winnings += (self.bet * size)
            return

        # Pick winner
        if self.p_hand[self.c_sp,:].sum() > self.h_hand.sum():
            self.winnings += (self.bet * size)
            return
        elif self.p_hand[self.c_sp,:].sum() < self.h_hand.sum():
            self.winnings -= (self.bet * size)
            return
        else:
            # draw
            return


    def _play(self):
        """
        Play a single game.

        Parameters
        ----------
        """
        # implement the strategy and return winnings
        self._implement_strategy()


    def _reset(self):
        """
        Reset variables.

        Parameters
        ----------
        """
        # current bet size (may be larger than the inital bet size in some cases)
        self.bet = self.initial_bet_size
        # initalize deck
        self.deck = deck_setup()
        # player hand and House hand
        self.p_hand = np.zeros((4, 20), dtype=int)
        self.h_hand = np.zeros((1, 20), dtype=int)
        # first House draw is the "face-up" card
        self.h_faceup = 0
        # indicator for number of splits
        self.n_sp = 0
        # index for the hand currently in play (used for splits)
        self.c_sp = 0
        # reset winnings
        self.winnings = 0
