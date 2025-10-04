from otree.api import *

class PlayerBot(Bot):

    def play_round(self):

        yield pages.Intro

