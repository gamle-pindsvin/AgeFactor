from otree.api import *
import random
import copy
import string

class Constants(BaseConstants):
    name_in_url = 'Computer_Counsel'
    # nur 2, weil Berater jetzt ein Computer ist
    players_per_group = 2
    num_rounds = 6

    # REIHENFOLGE der Rollen wichtig - wird später in player.role übernommen!!!
    opfer_role = 'Opfer'
    entscheider_role = 'Entscheider'
    berater_role = 'Berater'

    # Flat-Auszahlung für den Berater
    berater_auszahlung_pro_Runde = 60

    timeOutSeconds = 600

class Subsession(BaseSubsession):
    pass
        #subsession.A_Team_Werte = [60, 180, 200, 100]
        #subsession.A_Opfer_Werte = [180, 60, 100, 50]
        #subsession.B_Team_Werte = [180, 60, 100, 200]
        #subsession.B_Opfer_Werte = [60, 180, 50, 100]
        #subsession.C_Team_Werte = [240, 0, 150, 150]
        #subsession.C_Opfer_Werte = [0, 240, 75, 75]

        # Welcher Spielart kommt wann
        #subsession.Wertigkeit_Folge = [1, 4, 2, 1, 3, 2]


        # Auszahlungen werden hier zwischengespeichert. Für das Opfer direkt und für das Team als Array
        #subsession.AuszahlungInPunktenFuerDasOpfer = 0

        # Folge der Auszahlungen für das Team (das, was in der Runde erhalten wurde, wird diesem Team-Spieler zugeschlagen.
        # SPÄTER EVTL. echte Zufall-Zuordnung
        #subsession.Auszahlung_Folge = [1, 1, 2, 2, 1, 2]


class Group(BaseGroup):
    # BeraterEmpfehlung wie bei IC und DC gibt es nicht, stattdessen wird eine Folge aus eines menschlichen Beraters
    #       gezogen und nach dem Aufruf von Intro muss in der Session gespeichert werden. Hier geht nicht, weil
    #       models keine Dictionary speichern können

    EntscheiderEmpfehlung = models.StringField(initial="NOVALUE")
    EndgueltigeEntscheidung = models.StringField(initial="NOVALUE")

class Player(BasePlayer):

    Entscheidung = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F']], widget=widgets.RadioSelect)

    # Statistik am Ende
    Fachrichtung = models.StringField(choices=[['Man', 'Management'], ['Eco', 'Economics'], ['Law', 'Law'], ['Cog', 'Cognitive Science'], ['Nat', 'Natural Science or Mathematics'], ['Other', 'Other field'], ['None', "I'm not a student"]], widget=widgets.RadioSelect)
    Altersgruppe = models.StringField(choices=[['1', '20 years or less'], ['2', '21 - 24'], ['3', '25 - 28'], ['4', '29 - 35'], ['5', 'more than 35']], widget=widgets.RadioSelect)
    Geschlecht = models.StringField(choices=[['F', 'Female'], ['M', 'Male'], ['D', 'Not listed'], ['N', 'Prefer not to answer']], widget=widgets.RadioSelect)

    # Auszahlung
    #weg, da eigentlich player.payoff
    #AuszahlungInPunkten = models.IntegerField(initial=0)

    #Am Ende player.payoff aus dem PARTICIPANT ggf. mit real_world_currency_per_point im Config
    AuszahlungInDKK = models.CurrencyField(initial=0)
    AuszahlungUserName = models.StringField()


class Intro(Page):
    # timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        session = player.session

        # Hier wird die "Angebotsmatrix" festgelegt - welche Prämie für welche Entscheidung
        # ABWEICHEND vom letzten Experiment keine SPALTEN sondenr Array aus Arrays
        # Auszahlungen in der Form
        # [ Auswahl A - Team | Auswahl A - Oper | Ausw. B - Team | Ausw. B - Opfer | Ausw. C - Team | Ausw.C - Opfer ]
        angeboteSpiel1 = [60, 180, 180, 60, 240, 0, 60, 180, 180, 60, 240, 0]
        angeboteSpiel2 = [180, 60, 60, 180, 0, 240, 180, 60, 60, 180, 0, 240]
        angeboteSpiel3 = [200, 100, 100, 50, 150, 75, 200, 100, 100, 50, 150, 75]
        angeboteSpiel4 = [100, 50, 200, 100, 150, 75, 100, 50, 200, 100, 150, 75]
        session.AngebotsMatrix = [angeboteSpiel1, angeboteSpiel2, angeboteSpiel3, angeboteSpiel4]

        # Welche Spielart (Spiel 1 bis 4) kommt wann vor
        session.Spielarten_Folge = [1, 4, 2, 1, 3, 2]

        # Speichern im "Participant" ist wichtig, weil derselbe Spieler in wetieren Runden evtl. eine andere Nummer hat
        player.participant.zugeordneteRole = player.role

        # Neues Spiel - neue Auszahlung.
        player.payoff = 0
        player.participant.payoff = 0

        # Die Klick-Vorschläge des Computer-Beraters werden hier gezogen
        # encoding='utf-8-sig' !!!! ist wichtig! Sonst wird erstes nicht sichtbare Zeichen als '\ufeff dazugeklebt
        import csv
        with open('ComputerCouncil\it.csv', encoding='utf-8-sig') as file:
            rows = list(csv.DictReader(file))

        # Anzahl der Alternativen, die Computer spielen kann (aus dem Experiment mit normalen Menschen)
        #     automatisch als Anzahl der Zeilen in der CSV-Datei
        member_count = 0

        # gespeicherteClickFolgen ist  ein Dictionary mit 1->erste Auswahl des menschlichen Beraters (z.B. "A"),
        #         2->zweite Auswahl des Beraters usw.
        for gespeicherteClickFolgen in rows:
            if member_count == 0:
                print(f'Column names are {", ".join(gespeicherteClickFolgen)}')
            print(f'\t{gespeicherteClickFolgen["1"]} , {gespeicherteClickFolgen["2"]} , {gespeicherteClickFolgen["3"]}.')
            member_count += 1

        # wir ziehen eine davon aus 1 bis member_count (technisch 0 bis member_count.
        #      es wird -2 und nicht -1 abgezogen, weil die erste Zeile Header ist und rows den nicht mehr hat
        zufallKlickFolgeIndex = random.randint(0,member_count-2)
        zufallKlickFolge = rows[zufallKlickFolgeIndex]
        print("zufallKlickFolge: ", zufallKlickFolge, " index: ", zufallKlickFolgeIndex)

        player.session.BeraterEmpfehlungFolge  = zufallKlickFolge



# Pro Spiel wird die Runde aus der Session gelesen
# Zurück kommt der Auszahlungsarray  
#   [ Auswahl A - Team | Auswahl A - Oper | Ausw. B - Team | Ausw. B - Opfer | Ausw. C - Team | Ausw.C - Opfer ]
def getAuszahlungArray(session: Subsession, round_number):
    posInArray = round_number - 1
    #[1, 4, 2, 1, 3, 2]
    spieleArt = session.Spielarten_Folge[posInArray]
    spielAngebote = session.AngebotsMatrix[spieleArt - 1]
    return spielAngebote

# Für gegebenes Auszahlungsarray (Spielart) und den ausgewählten Buchstaben wird hier
# die Auszahlung für das Team (Berater / Entscheider) geliefert.
def getTeamAuszahlung(auswahlChar, auszahlungsArray):
    txtT = "Das Team kriegt für die Auswahl {} den Betrag von {} Punkten."
    letterArray = ["A", "B", "C", "D", "E", "F"]
    resultFound = False
    for i in range(6):
        if letterArray[i] == auswahlChar:
            result = auszahlungsArray[2*i]
            resultFound = True
            print(txtT.format(auswahlChar, result))
    if (not resultFound):
        print("Something gets wrong. getTeamAuszahlung group.EndgueltigeEntscheidung: " + auswahlChar)
    return result


# Für gegebenes Auszahlungsarray (Spielart) und den ausgewählten Buchstaben wird hier
# die Auszahlung für das Team (Berater / Entscheider) geliefert.
def getOpferAuszahlung(auswahlChar, auszahlungsArray):
    txtO = "Das Opfer kriegt für die Auswahl {} den Betrag von {} Punkten."
    letterArray = ["A", "B", "C", "D", "E", "F"]
    resultFound = False
    for i in range(6):
        if letterArray[i] == auswahlChar:
            result = auszahlungsArray[2*i+1]
            resultFound = True
            print(txtO.format(auswahlChar, result))
    if (not resultFound):
        print("Something gets wrong. getOpferAuszahlung group.EndgueltigeEntscheidung: " + auswahlChar)
    return result


# Nur für den Entscheider
class SeiteFuerDenEntscheider(Page):
    #timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["Entscheidung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.zugeordneteRole == Constants.entscheider_role

    @staticmethod
    def vars_for_template(player: Player):

        # auszahlung = getAuszahlungArray(player)
        auszahlung = getAuszahlungArray(player.session, player.round_number)

        # Wir müssen die Berater-Empfehlung, die vom Computer kommt zeigen. D
        #   Dazu wird aus dem Dictionary BeraterEmpfehlungFolge die für die
        #   konkrete Runde dazugehörige Empfehlung gezogen
        ###schluessel = ''.join(player.round_number)
        empfehlung = player.session.BeraterEmpfehlungFolge[str(player.round_number)]
        print("runde: ", player.round_number, " mit der Empfehlung: ", empfehlung)

        return {
            'beraterEmpfehlung': empfehlung,
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role),
            'auszahlung': auszahlung

        }

    # Speichre die Wahl des Entscheiders 
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.EntscheiderEmpfehlung = player.Entscheidung

# Auswahl des Entscheiders. Opfer und Berater warten
class WarteAufDenEntscheider(WaitPage):
    body_text = "Waiting for the other participants"

    def after_all_players_arrive(group: Group):
        pass
        #entscheider = group.get_player_by_role(Constants.entscheider_role)
        #group.EntscheiderEmpfehlung = entscheider.Entscheidung


class SeiteFuerDieOpfer(Page):
    #timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["Entscheidung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.zugeordneteRole == Constants.opfer_role

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role)

        }
 
    # Speichere die Entscheidung der Opfer
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        group.EndgueltigeEntscheidung = player.Entscheidung



# Auswahl des Opfer. Berater und Entscheider warten
class WarteAufDieOpfer(WaitPage):
    body_text = "Waiting for the other participants ???? ggf. schreiben, dass gerade der I-Participant entscheidet?"
    @staticmethod
    def after_all_players_arrive(group: Group):

        session = group.session
        round_number = group.round_number

        # Auszahlung

        opferInkrement = 0
        beraterInkrement = 0
        entscheiderInkrement = 0

        # Zuerst die Werte
        #[ Auswahl A - Team | Auswahl A - Oper | Ausw. B - Team | Ausw. B - Opfer | Ausw. C - Team | Ausw.C - Opfer ]


        ## auszahlung = getAuszahlungArray(player)
        auszahlung = getAuszahlungArray(session, round_number)

        # Jetzt schauen wir, ob A, B oder C und weisen die Zuwächse zu
        # Berater wird flat bezahlt
        # Entscheider bekommt die ganze Team-Auszahlung
        if (group.EndgueltigeEntscheidung is not None):
            opferInkrement = getOpferAuszahlung(group.EndgueltigeEntscheidung, auszahlung)
            entscheiderInkrement = getTeamAuszahlung(group.EndgueltigeEntscheidung, auszahlung)

        # Payoffs werden erhöht

        opfer = group.get_player_by_role(Constants.opfer_role)
        opfer.participant.payoff = opfer.participant.payoff + opferInkrement

        entscheider = group.get_player_by_role(Constants.entscheider_role)
        entscheider.participant.payoff += entscheiderInkrement



# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    form_fields = ['Fachrichtung', 'Altersgruppe', 'Geschlecht']

    def is_displayed(player: Player):
        # FEST die letzte 12. Runde des letzten Spiels
        # NATÜRLICH AM ENDE - 12 nicht 6 ################################ !!!! ###############################################
        return player.round_number == 6

    def vars_for_template(player: Player):

        group = player.group

        # ToDO GGF Auszahlungskorrektur
        # if Auszahlung_Punkte_Opfer > 4900:
        #     Auszahlung_Punkte_Opfer = random.randint(135, 246)*20

        opfer = group.get_player_by_role(Constants.opfer_role).participant
        name = ''.join(random.sample(string.ascii_uppercase, 6))
        opfer.AuszahlungUserName = copy.deepcopy(name)

        entscheider = group.get_player_by_role(Constants.entscheider_role).participant
        name = ''.join(random.sample(string.ascii_uppercase, 6))
        entscheider.AuszahlungUserName = copy.deepcopy(name)



# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class ErgebnisComputerCouncil(Page):

    def is_displayed(player: Player):
        # FEST die letzte 12. Runde des letzten Spiels
        # NATÜRLICH AM ENDE - 12 nicht 6 ################################ !!!! ###############################################
        return player.round_number == 6

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role)

        }


page_sequence = [Intro, SeiteFuerDenEntscheider, WarteAufDenEntscheider, SeiteFuerDieOpfer, WarteAufDieOpfer, AuszahlungUmfrage, ErgebnisComputerCouncil]