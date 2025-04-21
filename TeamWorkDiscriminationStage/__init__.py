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
    name_in_url = 'TeamWorkDiscriminationStage'
    #TODO: MUSS MEHR SEIN, als die tatsächlich mögliche Anzahl der Teilnehmer also deutlich mehr als 12!!!
    players_per_group = 12
    num_rounds = 1
    # Wie lange soll die Aufgabe gelöst werden
    dauerDesThreatmentsInSekunden = 420
    # Pence flat
    festerAnteilderBezahlung = 0.40
    # Pence pro richtige Antwort
    bezahlungProAntwort = 0.05
    # Für die Quiz - wie oft sollte man hypothetisch spielen
    quizAngenommeneAnzahlAntowrten = 100
    # Umrechnungfaktor aus den Punkten
    waehrungsFaktor = 1
    waehrungsName = 'GBP'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):

    ProlificID = models.StringField( label='')
    AnzahlRichtigerAntworten = models.IntegerField(initial=0)

    QuizKodieren1 = models.StringField(choices=[['a', 'a'], ['b', 'b'], ['c', 'c']], widget=widgets.RadioSelect, label='')
    QuizKodieren2 = models.StringField(choices=[['a', 'a'], ['b', 'b'], ['c', 'c']], widget=widgets.RadioSelect, label='')
    QuizBezahlung = models.StringField(choices=[['a', 'a'], ['b', 'b'], ['c', 'c']], widget=widgets.RadioSelect, label='')

    # Statistik am Ende
    #PoliticalOrientation = models.StringField(choices=[['1', 'Very left-leaning'], ['2', 'Left-leaning'], ['3', 'Slightly left-leaning'], ['4', 'Centrist'], ['5', 'Slightly right-leaning'], ['6', 'Right-leaning'], ['7', "Very right-leaning"]], widget=widgets.RadioSelect, label='Where would you place yourself on the following political spectrum?')
    Education = models.StringField(choices=[['1', 'No formal qualifications'], ['2', 'GCSEs or equivalent (e.g., O-Levels)'], ['3', 'A-Levels or equivalent (e.g., high school diploma)'], ['4', 'Vocational qualification (e.g., NVQ, BTEC)'], ['5', 'Undergraduate degree (e.g., BA, BSc)'], ['6', 'Postgraduate degree (e.g., MA, MSc, PhD)'], ['0', "Other "]], widget=widgets.RadioSelect, label='What is the highest level of education you have completed? ')
    GeburtsJahr = models.IntegerField(min=1930, max=2010, label='In which year were you born?')
    Gender = models.StringField(choices=[['F', 'Female'], ['M', 'Male'], ['D', 'Not listed'], ['N', 'Prefer not to answer']], widget=widgets.RadioSelect, label='What is your gender?')

    #Am Ende ggf. mit real_world_currency_per_point im Config korrigieren
    #AuszahlungInWaehrung = models.IntegerField(initial=0)
    VerdientePunkte = models.FloatField(initial=0.0)
    AuszahlungWaehrungName = models.StringField();

    # ProlificID - Fehlerhinweis kann noch angezeigt werden
    HinweisLangeProlificID = models.BooleanField(initial=True)

    # Zählt falsche Versuche beim Quiz
    FreiVersucheImQuiz = models.IntegerField(initial=3)
    HatSichQualifiziert = models.BooleanField(initial=True)

    # Checkbox für Consent
    Akzeptiert_bedingungen = models.BooleanField(label="", widget=widgets.CheckboxInput, blank=True)


class Intro(Page):
    form_model = 'player'
    form_fields = ["ProlificID"]

    # einmal warnen wir, dass ProlificID ggf. nicht korrekt ist
    einmaligeWartung = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    def error_message(player, values) :
        if len(values['ProlificID']) != 24 and player.HinweisLangeProlificID :
            # nächstes Mal wird nicht nehr gewarnt
            player.HinweisLangeProlificID = False
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
        #player.AuszahlungInWaehrung = 0
        player.VerdientePunkte = 0.0
        player.participant.VerdientePunkte = 0.0
        player.AnzahlRichtigerAntworten = 0
        player.participant.AnzahlRichtigerAntworten = 0
        player.FreiVersucheImQuiz = 5


class Intro2(Page):
    form_model = 'player'
    form_fields = ['Akzeptiert_bedingungen']

    @staticmethod
    def error_message(player, values):
        # print(values['Akzeptiert_bedingungen'])
        # Checkbox nicht ausgewählt
        if ( not (values['Akzeptiert_bedingungen'])):
           return 'Please confirm that you have read the instructions and the Informed Consent'

# Verständnis-Quiz
class Quiz(Page):
    form_model = 'player'
    form_fields = ["QuizKodieren1", "QuizKodieren2", "QuizBezahlung"]


    @staticmethod
    def error_message(player, values):
        # Wenn player.FreiVersucheImQuiz 0 werden, geht weiter, aber gleich zu der Auszahlungsseite.
        quizKorrekt = ((values['QuizKodieren1'] == 'b') and (values['QuizKodieren2'] == 'c') and (values['QuizBezahlung'] == 'b'))
        #print(values['QuizKodieren1'], 'bool: ', (values['QuizKodieren1'] == 'B'))
        #print(values['QuizKodieren2'], 'bool: ', (values['QuizKodieren2'] == 'C'))
        #print(values['QuizBezahlung'], 'bool: ', (values['QuizBezahlung'] == 'C'))
        if not quizKorrekt:
            #print('NICHT KORREKT player.FreiVersucheImQuiz war: ', player.FreiVersucheImQuiz, " / quizKorrekt: ", quizKorrekt)
            player.FreiVersucheImQuiz -= 1
            if player.FreiVersucheImQuiz > 0 :
                #print('Try again please. One or both answers are not yet correct. You have ', str(player.FreiVersucheImQuiz), ' attempts left.')
                return 'Try again please. One or more answers are not yet correct. You have ' + str(player.FreiVersucheImQuiz) + ' attempts left.'
            else:
                #keine Freiversuche mehr
                player.HatSichQualifiziert = False
        else:
            #print('KORREKT!!')
            pass

    @staticmethod
    def vars_for_template(player: Player):
        #Werte für die Auszahlungsfragen
        antwortA = Constants.quizAngenommeneAnzahlAntowrten*Constants.bezahlungProAntwort
        antwortB = Constants.quizAngenommeneAnzahlAntowrten*Constants.bezahlungProAntwort + Constants.festerAnteilderBezahlung
        antwortC = Constants.quizAngenommeneAnzahlAntowrten + Constants.festerAnteilderBezahlung
        return {
            'AntwortA': antwortA,
            'AntwortB': antwortB,
            'AntwortC': antwortC
        }



    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass



class RealEffortTask(Page):
    form_model = 'player'
    #form_fields = ["AnzahlRichtigerAntworten"]
    timeout_seconds = Constants.dauerDesThreatmentsInSekunden

    @staticmethod
    # Wird bei denen NICHT anzgezeigt, die das Quiz nicht geschafft haben.
    def is_displayed(player: Player):
        #print('HatSichQualifiziert: ', player.HatSichQualifiziert)
        return player.HatSichQualifiziert

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'dauerDesThreatmentsInSekunden': Constants.dauerDesThreatmentsInSekunden
        }

    @staticmethod
    def live_method(player, data):
        # Initial auszahlung = 0
        auszahlung = 0.0
       # Nur wenn data nicht NULL ist UND keine -1 übergeben wurde (was das Button ABBRECHEN macht!)
        if data is not None and data != -1:
            # OK-Button
            player.participant.AnzahlRichtigerAntworten = data
            player.AnzahlRichtigerAntworten = data
            #print('$$ 1 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)

            # BERECHNE die Auszahlung
            auszahlung = Constants.festerAnteilderBezahlung + data*Constants.bezahlungProAntwort
            player.VerdientePunkte = auszahlung
            player.participant.VerdientePunkte = auszahlung

            # Umrechnnen in verschiedene Währungen?
            player.payoff = auszahlung * Constants.waehrungsFaktor
            player.participant.payoff = auszahlung * Constants.waehrungsFaktor

            print('player.participant.ProlificID: ', player.participant.ProlificID, ' player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten, ' player.participant.VerdientePunkte: ', player.participant.VerdientePunkte)
        else:
            # Abbrechen-Button
            print('ABBRECHEN 1: ', ' player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten)
            # Die Auszahlung

            print('$$ 22222222222222222222222222222222222222222222222222222222222222222222  $$')
            for key, value in player.participant.vars.items():
                print(key, value)

            print('$$ 22222222222222222222222222222222222222222222222222222222222222222222  ENDE $$')

            if 'VerdientePunkte' in player.participant.vars:
                wert = player.participant.vars['VerdientePunkte']
                print('$$ 22222222222222222222222222222222222222222222222222222222222222222222  $$ wert: ', wert)
            else:
                wert = None  # oder einen anderen Standardwert



            #if player.participant.VerdientePunkte is None:
            #    player.participant.VerdientePunkte = Constants.festerAnteilderBezahlung
            #    player.participant.AnzahlRichtigerAntworten = 0

            print('ABBRECHEN 2: ', ' player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten, ' player.participant.VerdientePunkte: ', player.participant.VerdientePunkte)
            print('ABBRECHEN: ', ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten, ' player.participant.VerdientePunkte: ', player.participant.VerdientePunkte)
            return {player.id_in_group: 'next_page'}

# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    # GeburtsJahr wird EXTRA aufgeführt!! Wenn nicht funktioniert, wie unten.
    #form_fields = ['GeburtsJahr', 'Gender', 'Education', 'PoliticalOrientation']
    form_fields = ['GeburtsJahr', 'Gender', 'Education']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        if not player.HatSichQualifiziert:
            player.AnzahlRichtigerAntworten = 0
            player.VerdientePunkte = Constants.festerAnteilderBezahlung
            player.payoff = player.VerdientePunkte * Constants.waehrungsFaktor
            player.participant.AnzahlRichtigerAntworten = 0
            player.participant.VerdientePunkte = Constants.festerAnteilderBezahlung
            player.participant.payoff = player.participant.VerdientePunkte * Constants.waehrungsFaktor
            #print('$$ Y $$ player.participant.VerdientePunkte: ', player.participant.VerdientePunkte )
        #else:
            #print('$$ N $$ player.participant.VerdientePunkte: ', player.participant.VerdientePunkte )


# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class Ergebnis(Page):
    form_model = 'player'




page_sequence = [Intro, Intro2, Quiz, RealEffortTask, AuszahlungUmfrage, Ergebnis]