from ..blackjack import Simulator


def main():

    sim = Simulator(bet_size=10, strategy_name="basic_strategy")
    sim.playgames(num_games=100000)
    sim.summary(plots=True)


if __name__ == '__main__':
    main()
