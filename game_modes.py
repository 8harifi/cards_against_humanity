import random
import threading
import time

from game import Player


class GameModeBase:
    def __init__(self, callback: callable, players: [Player], game_duration: int = 30):
        self.callback = callback
        self.players = players
        self.game_duration = game_duration
        self.is_running = False
        self.main_thread: threading.Thread = None

    def start(self):
        """
        start the actual game process
        - start a round
        - broadcast the scores
        - game over vote (if at least 4 people, continue to the next round/go to step 1)
        - close the game
        :return:
        """
        pass

    def start_round_timer(self) -> None:
        """
        start a timer for a round
        :return:
        """
        msg = {
            'event': 'start',
        }
        self.callback(msg)
        self.is_running = True

        def main_thread_function():
            delay = 1
            i = 0
            while i < self.game_duration / 1 and self.is_running:
                time.sleep(delay)
                i += 1
            if self.is_running:
                msg = {
                    'event': 'close',
                }
                self.callback(msg)
                self.is_running = False

        self.main_thread = threading.Thread(target=main_thread_function)
        self.main_thread.start()

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
        pass

    def restart(self):
        msg = {
            'event': 'restart',
        }
        self.callback(msg)

    def stop(self):
        msg = {
            'event': 'close',
        }
        self.is_running = False
        self.callback(msg)


class SimpleCah(GameModeBase):
    def __init__(self, callback: callable, players: [Player], game_duration: int = 30):
        super(SimpleCah, self).__init__(callback, players, game_duration)
        self.callback = callback
        self.players = players
        self.game_duration = game_duration
        self.czar = None

    def choose_czar(self):
        self.czar = random.choice(self.players)
