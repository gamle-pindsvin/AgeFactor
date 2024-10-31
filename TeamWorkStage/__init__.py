from otree.api import *
import random
import copy
import string
import math
import io
import csv
import os

from uvicorn import Config


class Constants(BaseConstants):
    name_in_url = 'TeamWorkStage'
    #TODO: MUSS MEHR SEIN, als die tatsächlich mögliche Anzahl der Teilnehmer also deutlich mehr als 12!!!
    players_per_group = 12
    num_rounds = 1
    # Wie lange soll die Aufgabe gelöst werden
    dauerDesThreatmentsInSekunden = 3000
    # Umrechnungfaktor aus den Punkten / E$ z.B. in DKK oder USD
    waehrungsFaktor = 1
    waehrungsName = 'USD'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):

    ProlificID = models.StringField( label='')
    AnzahlRichtigerAntworten = models.IntegerField()

    QuizKodieren1 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect, label='')
    QuizKodieren2 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect, label='')
    QuizBezahlung = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect, label='')

    # Statistik am Ende
    Fachrichtung = models.StringField(choices=[['Man', 'Management'], ['Eco', 'Economics'], ['Law', 'Law'], ['Cog', 'Cognitive Science'], ['Nat', 'Natural Science or Mathematics'], ['Other', 'Other field'], ['None', "I'm not a student"]], widget=widgets.RadioSelect, label='Field of study')
    Age = models.StringField(choices=[['1', '20 years or less'], ['2', '21 - 24'], ['3', '25 - 28'], ['4', '29 - 35'], ['5', 'more than 35']], widget=widgets.RadioSelect)
    Gender = models.StringField(choices=[['F', 'Female'], ['M', 'Male'], ['D', 'Not listed'], ['N', 'Prefer not to answer']], widget=widgets.RadioSelect)

    #Am Ende ggf. mit real_world_currency_per_point im Config korrigieren
    AuszahlungInWaehrung = models.IntegerField(initial=0)
    VerdientePunkte = models.IntegerField(initial=0)
    AuszahlungWaehrungName = models.StringField();

    # Zählt falsche Versuche beim Quiz
    FreiVersucheImQuiz = models.IntegerField(initial=3)


class Intro(Page):
    form_model = 'player'
    form_fields = ["ProlificID"]

    # einmal warnen wir, dass ProlificID ggf. nicht korrekt ist
    einmaligeWartung = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    def error_message(player, values) :
        if len(values['ProlificID']) != 24 and  Intro.einmaligeWartung :
            # nächstes Mal wird nicht nehr gewarnt
            Intro.einmaligeWartung = False
            print('einmaligeWartung', Intro.einmaligeWartung, ' ID: ', Player.ProlificID)
            #TODO - Text ggf. anpassen!
            return 'Are you sure? Prolific-ID is normally 24 characters long.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        session = player.session
        player.participant.ProlificID = player.ProlificID;
        #print('Participant', player.participant.ProlificID, ' Player ID: ', player.ProlificID)
        # Neues Spiel - neue Auszahlung.
        player.payoff = 0
        player.participant.payoff = 0
        player.AuszahlungInWaehrung = 0
        player.VerdientePunkte = 0
        player.AnzahlRichtigerAntworten = 0
        player.FreiVersucheImQuiz = 3


# Verständnis-Quiz
class Quiz(Page):
    form_model = 'player'
    form_fields = ["QuizKodieren1", "QuizKodieren2", "QuizBezahlung"]


    @staticmethod
    def error_message(player, values):
        # Wenn player.FreiVersucheImQuiz 0 werden, geht weiter, aber gleich zu der Auszahlungsseite.
        player.FreiVersucheImQuiz -= 1
        if not ((values['QuizKodieren1'] == 'B') and (values['QuizKodieren2'] == 'C') and (values['QuizBezahlung'] == 'C')) and player.FreiVersucheImQuiz >0:
            #print('QuizKodieren1: ', values['QuizKodieren1'], ' QuizKodieren2: ', values['QuizKodieren2'], 'QuizBezahlung: ', values['QuizBezahlung'])
            return 'Try again please. One or both answers are not yet correct. You have ' + str(player.FreiVersucheImQuiz) + ' attempts left.'

    @staticmethod
    def vars_for_template(player: Player):
        pass


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass



class RealEffortTask(Page):
    form_model = 'player'
    form_fields = ["AnzahlRichtigerAntworten"]
    timeout_seconds = Constants.dauerDesThreatmentsInSekunden

    @staticmethod
    # Wird bei denen NICHT anzgezeigt, die das Quiz nicht geschafft haben.
    def is_displayed(player: Player):
        return player.FreiVersucheImQuiz > -1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'dauerDesThreatmentsInSekunden': Constants.dauerDesThreatmentsInSekunden
        }

    @staticmethod
    def live_method(player, data):
        player.participant.AnzahlRichtigerAntworten = data
        player.AnzahlRichtigerAntworten = data
        print('$$ 1 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)

        # BERECHNE die Auszahlung - hier 10 Fest + 5 Pro korrekte Antwort
        auszahlung = 10 + data*5
        player.VerdientePunkte = auszahlung
        player.participant.VerdientePunkte = auszahlung

        # Umrechnnen in verschiedene Währungen?
        player.payoff = auszahlung * Constants.waehrungsFaktor
        player.participant.payoff = auszahlung * Constants.waehrungsFaktor
        player.AuszahlungInWaehrung = auszahlung * Constants.waehrungsFaktor

        #print('player.participant.ProlificID: ', player.participant.ProlificID, ' player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten, ' player.participant.VerdientePunkte: ', player.participant.VerdientePunkte)
        #print('player.ProlificID: ', player.ProlificID, ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten, ' player.VerdientePunkte: ', player.VerdientePunkte)
        #print('received a bid from', player.id_in_group, ':', data)
        #print('player.participant.AnzahlRichtigerAntworten', player.participant.AnzahlRichtigerAntworten)
        print('$$ 2 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)



# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    form_fields = ['Fachrichtung', 'Age', 'Gender']






# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class Ergebnis(Page):


    @staticmethod
    def vars_for_template(player: Player):
        #print('player.participant.ProlificID: ', player.participant.ProlificID, ' player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten, ' player.participant.VerdientePunkte: ', player.participant.VerdientePunkte)
        #print('player.ProlificID: ', player.ProlificID, ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten, ' player.VerdientePunkte: ', player.VerdientePunkte)
        print('$$ 3 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)
        return {
            'ProlificID': player.ProlificID,
            'ProlificID-P': player.participant.ProlificID,
            'Anzahl': player.AnzahlRichtigerAntworten,
            'Anzahl-P': player.participant.AnzahlRichtigerAntworten,
            'Auszahlung': player.VerdientePunkte,
            'Auszahlung-P': player.participant.VerdientePunkte
        }


page_sequence = [Intro, Quiz, RealEffortTask, AuszahlungUmfrage, Ergebnis]