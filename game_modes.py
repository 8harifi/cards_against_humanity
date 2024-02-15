import random
import threading
import time

from cah import get_card
from custom_logging import clog
from game import Player


class GameModeBase:
    def __init__(self, players: [Player]):
        self.players = dict.fromkeys(players, 0)
        self.is_running = False
        self.main_thread: threading.Thread = None

        # configurations
        self.round_duration = 30
        self.finish_vote_duration = 15

    def broadcast(self, msg):
        for p in self.players:
            p.callback(msg)

    def start_round(self):
        """
        this function needs to be overwritten in the actual game modes
        :return:
        """
        pass

    def finish_vote(self) -> bool:
        """
        vote for finishing the game or continuing to play
        :return: bool (result of the poll)
        """
        self.broadcast(
            {
                'event': 'finish_vote',
                'status': 'start'
            }
        )
        for p in self.players:
            clog("some error might occur here")
            p.choice = None
        # dict.fromkeys([x.username for x in self.players], None) fix the next one
        poll = dict.fromkeys(self.players, None)
        i = 0
        while i <= self.finish_vote_duration and None in poll:
            for p in self.players:
                if p.choice is not None:
                    poll[p] = p.choice
                    p.choice = None
            time.sleep(1)
            i += 1
        self.broadcast(
            {
                'event': 'finish_vote',
                'status': 'end'
            }
        )
        if i > self.finish_vote_duration:  # time is up and some players didnt vote
            for p in poll:
                poll[p] = False if p.choice is None else p.choice

        return len(list(filter(lambda x: poll[x] == True, poll))) >= len(list(filter(lambda x: poll[x] == False, poll)))

    def start(self):
        """
        start the actual game process
        - start a round
        - broadcast the scores
        - game over vote (if at least 4 people, continue to the next round/go to step 1)
        - close the game
        :return:
        """
        self.start_round()
        self.broadcast(
            {
                'event': 'score_board',
                'scores': {p.username: self.players[p] for p in self.players}
            }
        )
        self.finish_vote()

    def start_round_timer(self) -> None:
        """
        start a timer for a round
        :return:
        """
        msg = {
            'event': 'start',
        }
        # self.callback(msg)
        self.broadcast(msg)
        self.is_running = True

        def main_thread_function():
            delay = 1
            i = 0
            while i < self.round_duration / 1 and self.is_running:
                time.sleep(delay)
                i += 1
            if self.is_running:
                msg = {
                    'event': 'close',
                }
                # self.callback(msg)
                self.broadcast(msg)
                self.is_running = False

        self.main_thread = threading.Thread(target=main_thread_function)
        self.main_thread.start()

    def restart(self):
        msg = {
            'event': 'restart',
        }
        # self.callback(msg)
        self.broadcast(msg)

    def stop(self):
        msg = {
            'event': 'close',
        }
        self.is_running = False
        # self.callback(msg)
        self.broadcast(msg)


class SimpleCah(GameModeBase):
    def __init__(self, players: [Player]):
        super(SimpleCah, self).__init__(players)
        self.players: [Player] = players
        self.czar = None

        # configurations

    def choose_czar(self):
        self.czar = random.choice(self.players)

    def deal_cards(self):
        """
        deal the cards between players
        10 white cards each
        :return:
        """
        for p in self.players:
            cards = get_card('white', n=10)
            p.callback(
                {
                    'event': 'deal_white_cards',
                    'cards': cards
                }
            )

    def start_round(self):
        """
        start a round:
        - choose a czar
        - deal the cards
        - timer start
        - (maybe sync time every n sec)
        - get cards
        - if time was up or all players picked a card, continue
        - judge
        - modify scores
        - end of round
        :return:
        """
        self.choose_czar()
