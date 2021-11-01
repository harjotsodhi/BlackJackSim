# BlackJackSim

## Project purpose
The purpose of this project is to implement a Python simulator for the game of
BlackJack.

This project allows users to easily simulate thousands of independent BlackJack
using a given strategy. The project also includes the ability to assess a
strategy's performance over tens, thousands, or millions of games through
evaluation metrics and plots.

## Table of Contents
  - [Installation](#installation)
    * [With conda](#with-conda)
  - [Implementations](#implementations)
    * [Rules](#rules)
    * [How to use](#how-to-use)
    * [Example](#example)
  - [Contact](#contact)

## Installation
### With conda
    $ git clone https://github.com/harjotsodhi/BlackJackSim.git
    $ cd BlackJackSim
    $ conda env create -f environment.yml
    $ conda activate blackjacksim_env

## Implementations
### Rules

The goal of BlackJack is to obtain a hand of cards whose total point value is
higher than the dealer, but not exceeding 21.

At the start of the game, both the dealer and the player are dealt two cards.
Both of the players' cards will be face-up, whereas the dealer will only have
one face-up card.

Numbered cards are valued at their respective values. Face-cards (i.e., King, Queen, Jack)
are valued at 10 points. Aces are valued at either 1 point or 11 points.

In general, there are 4 moves a player can make:
1. Hit: draw another card
2. Stand: do not draw another card
3. Split: divide hand into two (only possible if pairs are in hand)
4. Double: double the initial bet

Once the player is done making moves, the dealer will flip over the face-down card
and hit until a total of 17 is reached.

BlackJack includes two types of totals, which have to do with the value of the ace:
1. Hard total: a total in which an ace is counted as 11.
2. Soft total: a total in which an ace is counted as 1.

Depending on whether the player has an ace, the hard or soft total may be used to
decide the final winner. If the player reaches a total of 21 from the initial draw,
a "BlackJack" is declared, and the player wins 1.5x the initial bet, unless the dealer
also has a "BlackJack," in which case the game is considered a draw.

### How to use

Using this simulator is very simple. A BlackJack strategy, using the 4 aforementioned
move types, should be encoded as a .csv file and placed in
the "blackjacksim/strategies" subdirectory.

When encoding a new strategy, there are three "sub-strategies" which should be
considered:
1. hard strategy: a strategy for when the hand contains no aces.
2. soft strategy: a strategy for when the hand contains aces.
3. split strategy: a strategy for when the hand contains pairs.

An example (annotated) strategy is shown below.

<p align="center">
    <img src="https://github.com/harjotsodhi/BlackJackSim/blob/main/basic_strategy.png?raw=true" width="640"\>
</p>
<p align="center">
    Figure 1: Example "basic" strategy.
</p>

Here, "s" represented "Stand," "h" represents "Hit," "d" represents "Double," and
"p" represents "Split." The column axis indicates the face-up card of the dealer
and the row axis represents both the total value of the players' hand and
which of the three "sub-strategies" to use.

The strategy shown in figure 1 is a very famous strategy known as the "basic strategy"
(src: https://wizardofodds.com/games/blackjack/strategy/4-decks/). A working .csv
implementation of this strategy is already provided in the "blackjacksim/strategies" subdirectory.

Once a strategy is encoded, using it in practice couldn't be easier. Below is an example
of how to simulate 10,000 independent games of BlackJack, with an initial bet size of
$20 per game.

```python
from blackjack import Simulator

sim = Simulator(bet_size=20, strategy_name="your_strategy.csv")
sim.playgames(num_games=10000)
sim.summary(plots=True)
```
A full working example of this simulator is provided in the "blackjacksim/examples"
subdirectory. This full example simulates 100,000 independent games of BlackJack,
with an initial bet size of $10 per game, using the "basic strategy".

Summary tables and plots are also provided when the "summary" method is used.

$ python -m blackjacksim.examples.basic_strategy_example

<p align="center">
<img src="https://github.com/harjotsodhi/BlackJackSim/blob/main/figure1.png?raw=true" width="640"\>
</p>
<p align="center">
Figure 2: Histogram and KDE plot of basic strategy results.
</p>

| Statistic | Value |
| --- | ----------- |
| Count | 100,000 |
| Mean | $0.723 |
| St. Dev | $10.886 |
| Max | $60.00 |
| Min | $-60.00 |

As we may expect, the expected value of winnings is close to zero when using
a near optimal strategy in the game of BlackJack.

## Contact
Email: harjotsodhi17@gmail.com

LinkedIn: https://www.linkedin.com/in/harjot-sodhi/
