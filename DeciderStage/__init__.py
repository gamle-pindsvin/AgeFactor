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
    name_in_url = 'DeciderStage'
    #TODO: MUSS MEHR SEIN, als die tatsächlich mögliche Anzahl der Teilnehmer also deutlich mehr als 12!!!
    players_per_group = 12
    num_rounds = 3
    timeOutSeconds = 6000

    # Umrechnungfaktor aus den Punkten / E$ z.B. in DKK oder USD
    waehrungsFaktor = 1
    waehrungsName = 'USD'
    # 3 verschiedene Rollen
    role_T1 = 'T1'
    role_T2 = 'T2'
    role_T3 = 'T3'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):

    ProlificID = models.StringField( label='')
    AnzahlRichtigerAntworten = models.IntegerField()
    zugeordneteRole = models.StringField()

    QuizKodieren1 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect, label='')
    QuizKodieren2 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect, label='')
    QuizBezahlung = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect, label='')

    # Zufällig gezogene Ergebnisse zur Anzeige
    aktuellesErgebnisTWSSpieler1_Anzeige = models.IntegerField(label='')
    aktuellesErgebnisTWSSpieler2_Anzeige = models.IntegerField(label='')

    # Und Eingaben der Entscheider, was sie denken, dass einer beigetragen hat
    aktuellesErgebnisTWSSpieler1_Schaetzung = models.IntegerField(label='')
    aktuellesErgebnisTWSSpieler2_Schaetzung = models.IntegerField(label='')

    # Prüfen, ob man selbst decodieren kann
    SelbstTest = models.StringField(label='')

    # Statistik am Ende
    Fachrichtung = models.StringField(choices=[['Man', 'Management'], ['Eco', 'Economics'], ['Law', 'Law'], ['Cog', 'Cognitive Science'], ['Nat', 'Natural Science or Mathematics'], ['Other', 'Other field'], ['None', "I'm not a student"]], widget=widgets.RadioSelect, label='Field of study')
    Age = models.StringField(choices=[['1', '20 years or less'], ['2', '21 - 24'], ['3', '25 - 28'], ['4', '29 - 35'], ['5', 'more than 35']], widget=widgets.RadioSelect)
    Gender = models.StringField(choices=[['F', 'Female'], ['M', 'Male'], ['D', 'Not listed'], ['N', 'Prefer not to answer']], widget=widgets.RadioSelect)

    #Am Ende ggf. mit real_world_currency_per_point im Config korrigieren
    AuszahlungInWaehrung = models.IntegerField(initial=0)
    VerdientePunkte = models.IntegerField(initial=0)
    AuszahlungWaehrungName = models.StringField();


    # Liefert EIN Ergebnis aus der TeamWorkStage-Runde, also so etwas wie [10, 20, 30]
def waehleEinErgebnisAusTWS(player):
    rows = player.session.ergebnisseVonTWS
    # Anzahl der Ergebnisse automatisch als Anzahl der Zeilen in der CSV-Datei
    results_count = len(rows) - 1
    resultsFolgeIndex = random.randint(0, results_count)
    angezeigteErgebnisse = rows[resultsFolgeIndex]
    print('insgesamt: ', results_count, 'resultsFolgeIndex: ', resultsFolgeIndex, ' angezeigteErgebnisse: ', angezeigteErgebnisse)
    return angezeigteErgebnisse


    # Liefert EIN Ergebnis aus der TeamWorkStage-Runde, also so etwas wie [10, 20, 30]
def berechneAuszahlung(anzeige1, anzeige2, schaetzung1, schaetzung2):
    maxA = max(anzeige1, anzeige2);
    minA = min(anzeige1, anzeige2);
    maxS = max(schaetzung1, schaetzung2);
    minS = min(schaetzung1, schaetzung2);
    print('A1: ', anzeige1, 'A2: ', anzeige2, ' S1: ', schaetzung1,  ' S2: ', schaetzung2, ' MAX-Diff: ', abs(maxA-maxS) , ' MIN-Diff: ', abs(minA-minS))
    # berechnet wird (|maxA-maxS| + |minA-minS|)
    result = abs(maxA-maxS) + abs(minA-minS)

    return result

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

        # Welche Rolle
        zufallszahl = random.randint(0,300)
        if (zufallszahl <= 100):
            player.zugeordneteRole = Constants.role_T1;
            player.participant.zugeordneteRole = Constants.role_T1;
        elif (zufallszahl <= 200):
            player.zugeordneteRole = Constants.role_T2;
            player.participant.zugeordneteRole = Constants.role_T2;
        else:
            player.zugeordneteRole = Constants.role_T3;
            player.participant.zugeordneteRole = Constants.role_T3;

        #TODO HIER NUR UM ALLES IN T1 zu testen - DANACH LÖSCHEN!!!!
        #player.zugeordneteRole = Constants.role_T1;
        #player.participant.zugeordneteRole = Constants.role_T1;


        # Hier werden die Ergebnisse des TeamWorkStage eingelesen
        # Constants.trennzeichen ist für Windows \ und für Heroku /
        #
        # Muss schon hier passieren, damit man nicht jedes mal die Datei neu lädt
        fileNameMitOSTrenner = "DeciderStage" + os.sep + "resultTWS.csv"

        with open(fileNameMitOSTrenner, encoding='utf-8-sig', newline='') as file:
        #rows = list(csv.DictReader(file))
            reader = csv.reader(file)
            rows = list(reader)
        session.ergebnisseVonTWS = rows

        #print('Participant', player.participant.ProlificID, ' Player ID: ', player.ProlificID)
        # Neues Spiel - neue Auszahlung.
        player.payoff = 0
        player.participant.payoff = 0
        player.AuszahlungInWaehrung = 0
        player.VerdientePunkte = 0
        player.participant.VerdientePunkte = 0
        player.AnzahlRichtigerAntworten = 0




# Verständnis-Quiz
class Quiz(Page):
    form_model = 'player'
    form_fields = ["QuizKodieren1", "QuizKodieren2", "QuizBezahlung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        if not ((values['QuizKodieren1'] == 'B') and (values['QuizKodieren2'] == 'C') and (values['QuizBezahlung'] == 'C')):
            #print('QuizKodieren1: ', values['QuizKodieren1'], ' QuizKodieren2: ', values['QuizKodieren2'], 'QuizBezahlung: ', values['QuizBezahlung'])
            return 'Try again please. One or both answers are not yet correct.'

    @staticmethod
    def vars_for_template(player: Player):
        pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass

class RealEffortTask(Page):
    form_model = 'player'
    form_fields = ["SelbstTest"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def live_method(player, data):
        player.participant.AnzahlRichtigerAntworten = data
        player.AnzahlRichtigerAntworten = data
        print('$$ 1 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)

    @staticmethod
    def error_message(player, values):
        if not (values['SelbstTest'] == '123234234456123'):
            #print('QuizKodieren1: ', values['QuizKodieren1'], ' QuizKodieren2: ', values['QuizKodieren2'], 'QuizBezahlung: ', values['QuizBezahlung'])
            return 'The encoding is not correct. Please try again.'



class ResultsOfTWS(Page):
    form_model = 'player'
    #form_fields = ["AnzahlRichtigerAntworten"]
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1




# Nur für die Rolle T1
class SeiteFuerT1(Page):
    #timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung", "aktuellesErgebnisTWSSpieler2_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.zugeordneteRole == Constants.role_T1

    @staticmethod
    def vars_for_template(player: Player):

        # Ziehe einer der Ergebnisse aus TWS
        aktuellAngezeigteErgebnisse = waehleEinErgebnisAusTWS(player)

        player.aktuellesErgebnisTWSSpieler1_Anzeige = int(aktuellAngezeigteErgebnisse[0])
        player.aktuellesErgebnisTWSSpieler2_Anzeige = int(aktuellAngezeigteErgebnisse[1])

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        neuePunkteInDieserRunde = berechneAuszahlung(player.aktuellesErgebnisTWSSpieler1_Anzeige, player.aktuellesErgebnisTWSSpieler2_Anzeige, player.aktuellesErgebnisTWSSpieler1_Schaetzung, player.aktuellesErgebnisTWSSpieler2_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde


# Nur für die Rolle T2
class SeiteFuerT2(Page):
    #timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung", "aktuellesErgebnisTWSSpieler2_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.zugeordneteRole == Constants.role_T2

    @staticmethod
    def vars_for_template(player: Player):

        # Ziehe einer der Ergebnisse aus TWS
        aktuellAngezeigteErgebnisse = waehleEinErgebnisAusTWS(player)

        player.aktuellesErgebnisTWSSpieler1_Anzeige = int(aktuellAngezeigteErgebnisse[0])
        player.aktuellesErgebnisTWSSpieler2_Anzeige = int(aktuellAngezeigteErgebnisse[1])

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        neuePunkteInDieserRunde = berechneAuszahlung(player.aktuellesErgebnisTWSSpieler1_Anzeige, player.aktuellesErgebnisTWSSpieler2_Anzeige, player.aktuellesErgebnisTWSSpieler1_Schaetzung, player.aktuellesErgebnisTWSSpieler2_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde


# Nur für die Rolle T3
class SeiteFuerT3(Page):
    #timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung", "aktuellesErgebnisTWSSpieler2_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.zugeordneteRole == Constants.role_T3

    @staticmethod
    def vars_for_template(player: Player):

        # Ziehe einer der Ergebnisse aus TWS
        aktuellAngezeigteErgebnisse = waehleEinErgebnisAusTWS(player)

        player.aktuellesErgebnisTWSSpieler1_Anzeige = int(aktuellAngezeigteErgebnisse[0])
        player.aktuellesErgebnisTWSSpieler2_Anzeige = int(aktuellAngezeigteErgebnisse[1])

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        neuePunkteInDieserRunde = berechneAuszahlung(player.aktuellesErgebnisTWSSpieler1_Anzeige, player.aktuellesErgebnisTWSSpieler2_Anzeige, player.aktuellesErgebnisTWSSpieler1_Schaetzung, player.aktuellesErgebnisTWSSpieler2_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde

# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    form_fields = ['Fachrichtung', 'Age', 'Gender']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff = player.participant.VerdientePunkte / Constants.waehrungsFaktor;
        player.participant.payoff = player.participant.VerdientePunkte / Constants.waehrungsFaktor;


# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class Ergebnis(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds




page_sequence = [Intro, ResultsOfTWS, RealEffortTask, SeiteFuerT1, SeiteFuerT3, SeiteFuerT3, AuszahlungUmfrage, Ergebnis]