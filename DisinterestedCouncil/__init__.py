from otree.api import *
import random
import copy
import string
import io

class Constants(BaseConstants):
    name_in_url = 'DisinterestedCouncil'
    players_per_group = 3
    num_rounds = 10

    # REIHENFOLGE der Rollen wichtig - wird später in player.role übernommen!!!
    opfer_role = 'Opfer'
    entscheider_role = 'Entscheider'
    berater_role = 'Berater'

    # Flat-Auszahlung für den Berater
    berater_auszahlung_pro_Runde = 70

    timeOutSeconds = 600
    waehrungsFaktorDKK = 10.0



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    BeraterEmpfehlung = models.StringField(initial="NOVALUE")
    EntscheiderEmpfehlung = models.StringField(initial="NOVALUE")
    EntscheiderEmpfehlungFalsch = models.StringField(initial="NOVALUE")
    EndgueltigeEntscheidung = models.StringField(initial="NOVALUE")
    # mit Participants hackt, also zwischenspeicherung hier
    BeraterKennung = models.StringField(initial="NOVALUE")
    BeraterAuszahlungDKK = models.FloatField()
    BeraterAuszahlungPunkte = models.IntegerField()
    EntscheiderKennung = models.StringField(initial="NOVALUE")
    EntscheiderAuszahlungDKK = models.FloatField()
    EntscheiderAuszahlungPunkte = models.IntegerField()
    OpferKennung = models.StringField(initial="NOVALUE")
    OpferAuszahlungDKK = models.FloatField()
    OpferAuszahlungPunkte = models.IntegerField()
    BeraterKlickfolge = models.StringField(initial="NOVALUE")


class Player(BasePlayer):

    Entscheidung = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F']], widget=widgets.RadioSelect)

    # Für den Berater-Quiz
    Quiz1b = models.StringField(choices=[['1', 'This depends on the Project implemented by Player Z'], ['2', 'My payoff is 50.'], ['3', 'My payoff is 70, no matter which Project is implemented.']], widget=widgets.RadioSelect)
    Quiz2b = models.StringField(choices=[['1', 'Player X earns 50 and Player Z earns 190'], ['2', 'Player X earns 190 and Player Z earns 50'], ['3', 'This depends on the Message sent by Player X.']], widget=widgets.RadioSelect)
    Quiz1e = models.StringField(choices=[['1', 'My payoff is 190, no matter which Project is implemented.'], ['2', 'My payoff is 50.'], ['3', 'My payoff depends on the Project implemented by Player Z.']], widget=widgets.RadioSelect)
    Quiz2e = models.StringField(choices=[['1', 'My payoff is 50, Player Z`s payoff is 190 and Player Y`s payoff is 70.'], ['2', 'I earn 190 and Player Z earns 50'], ['3', 'My payoff is independent of which Project is implemented.']], widget=widgets.RadioSelect)

    # Für die Umfrage des Beraters
    Frage1A = models.IntegerField(min=0, max=100)
    Frage1B = models.IntegerField(min=0, max=100)
    Frage1C = models.IntegerField(min=0, max=100)
    Frage1D = models.IntegerField(min=0, max=100)
    Frage1E = models.IntegerField(min=0, max=100)
    Frage1F = models.IntegerField(min=0, max=100)
    Frage2 = models.StringField(choices=[['1', 'Yes'], ['0', 'No']], widget=widgets.RadioSelectHorizontal)
    Frage3 = models.StringField()
    Frage4 = models.StringField(choices=[['5', 'Very responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Not responsible at all']], widget=widgets.RadioSelectHorizontal)
    Frage5 = models.StringField(choices=[['5', 'I would feel very guilty'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'I would not feel guilty at all']], widget=widgets.RadioSelectHorizontal)
    Frage61 = models.StringField(choices=[['5', 'I am fully responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'I am not responsible']], widget=widgets.RadioSelectHorizontal)
    Frage62e = models.StringField(choices=[['5', 'Player Y is fully responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Player Y is not responsible']], widget=widgets.RadioSelectHorizontal)
    Frage62b = models.StringField(choices=[['5', 'Player X is fully responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Player X is not responsible']], widget=widgets.RadioSelectHorizontal)
    Frage63 = models.StringField(choices=[['5', 'Player Z is fully responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Player Z is not responsible']], widget=widgets.RadioSelectHorizontal)
    # FRAGE 7 steht nur beim Entscheider und zwar als die NUMMER 4 auf der Liste!!!
    Frage7 = models.StringField(choices=[['5', 'Very important'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Not important at all']], widget=widgets.RadioSelectHorizontal)


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
            #print(txtT.format(auswahlChar, result))
    if (not resultFound):
        print("Something gets wrong. group.EndgueltigeEntscheidung: " + auswahlChar)
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
            #print(txtO.format(auswahlChar, result))
    if (not resultFound):
        print("Something gets wrong. group.EndgueltigeEntscheidung: " + auswahlChar)
    return result


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
        angeboteSpiel1 = [60, 180, 210, 30, 150, 90, 180, 60, 30, 210, 90, 150]
        angeboteSpiel2 = [210, 30, 150, 90, 180, 60, 30, 210, 90, 150, 60, 180]
        angeboteSpiel3 = [30, 210, 90, 150, 60, 180, 210, 30, 150, 90, 180, 60]
        angeboteSpiel4 = [90, 90, 30, 30, 120, 120, 80, 80, 100, 100, 60, 60]
        angeboteSpiel5 = [80, 80, 100, 100, 60, 60, 90, 90, 30, 30, 120, 120]
        session.AngebotsMatrix = [angeboteSpiel1, angeboteSpiel2, angeboteSpiel3, angeboteSpiel4, angeboteSpiel5]

        # Welche Spielart (Spiel 1 bis 4) kommt wann vor
        session.Spielarten_Folge = [1, 4, 2, 5, 3, 2, 5, 4, 1, 3]

        # Folge der Auszahlungen für das Team (das, was in der Runde erhalten wurde, wird diesem Team-Spieler zugeschlagen.
        # SPÄTER EVTL. echte Zufall-Zuordnung
        # 1 - Berater, 2 - Entscheider
        session.AuszahlungImTeamFolge = [1, 1, 2, 2, 1, 2, 1, 1, 2, 1]

#TODO: Berater verdient flat

        # oTree will then automatically assign each role to a different player (sequentially according to id_in_group).
        # Rollen WERDEN von Otree Automatisch festgelegt also Quasi

        #  group.get_player_by_id(1).role = Constants.opfer_role
        #  group.get_player_by_id(2).role = Constants.berater_role
        #  group.get_player_by_id(3).role = Constants.entscheider_role

        # Speichern im "Participant" ist wichtig, weil derselbe Spieler in wetieren Runden evtl. eine andere Nummer hat
        player.participant.zugeordneteRole = player.role

        # Neues Spiel - neue Auszahlung.
        player.payoff = 0
        player.participant.payoff = 0

        # Payoff macht Probleme in der Anzeige, entweder POINTS oder Kr für beides. Daher über die Session
        session.EntscheiderAuszahlungPunkte = 0
        session.BeraterAuszahlungPunkte = 0
        session.OpferAuszahlungPunkte = 0


class RoleBerater(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.zugeordneteRole == Constants.berater_role) and (player.round_number == 1)

class RoleEntscheider(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.zugeordneteRole == Constants.entscheider_role) and (player.round_number == 1)

class RoleOpfer(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.zugeordneteRole == Constants.opfer_role) and (player.round_number == 1)



# Verständnis-Quiz für den Berater
class QuizBerater(Page):
    # timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["Quiz1b", "Quiz2b"]

    @staticmethod
    def is_displayed(player: Player):
        # Nur für den Berater und nur in der ersten Runde
        return (player.participant.zugeordneteRole == Constants.berater_role) and (player.round_number == 1)

    @staticmethod
    def error_message(player, values):
        if not ((values['Quiz1b'] == '3') and (values['Quiz2b'] == '1')):
            return 'Try again please. One or both answers are not yet correct.'

    @staticmethod
    def vars_for_template(player: Player):
        #TODO Auszahlung in der echten 1. Runde!!!! Ggf. andere Auszahlungen?
        auszahlung = getAuszahlungArray(player.session, 1)
        group = player.group
        return {
            'auszahlung': auszahlung,
            'empfehlung': group.BeraterEmpfehlung,
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role),
        }

# Verständnis-Quiz für den Entscheider
class QuizEntscheider(Page):
    # timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["Quiz1e", "Quiz2e"]

    @staticmethod
    def is_displayed(player: Player):
        # Nur für den Berater und nur in der ersten Runde
        return (player.participant.zugeordneteRole == Constants.entscheider_role) and (player.round_number == 1)

    @staticmethod
    def error_message(player, values):
        if not ((values['Quiz1e'] == '3') and (values['Quiz2e'] == '1')):
            return 'Try again please. One or both answers are not yet correct.'

    @staticmethod
    def vars_for_template(player: Player):
        pass


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass



class SeiteFuerDenBerater(Page):
   # timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["Entscheidung"]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.zugeordneteRole == Constants.berater_role

    @staticmethod
    def vars_for_template(player: Player):
        auszahlung = getAuszahlungArray(player.session, player.round_number)

        return {
            'auszahlung': auszahlung,
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        group.BeraterEmpfehlung = player.Entscheidung
        session = player.session
        if player.round_number == 1:
            session.BeraterKlickfolge = ""
        session.BeraterKlickfolge += player.Entscheidung
        if player.round_number != 10:
            session.BeraterKlickfolge += ","
        else:
            group.BeraterKlickfolge = session.BeraterKlickfolge

        #print("Berater Empfehlung: player.Entscheidung: ", player.Entscheidung, " group.BeraterEmpfehlung: ", group.BeraterEmpfehlung)


# Auswahl des Beraters. Opfer und Entscheider warten
class WarteAufDenBerater(WaitPage):
    body_text = "Waiting for the other participants"

    def after_all_players_arrive(group: Group):
        pass
        # Auswahl des Beraters
        #berater = group.get_player_by_role(Constants.berater_role)
        #group.BeraterEmpfehlung = berater.Entscheidung


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

        ## auszahlung = getAuszahlungArray(player)
        auszahlung = getAuszahlungArray(player.session, player.round_number)

        return {
            'beraterEmpfehlung': player.group.BeraterEmpfehlung,
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
    body_text = "Waiting for the other participants"
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
            beraterInkrement = Constants.berater_auszahlung_pro_Runde
            entscheiderInkrement = getTeamAuszahlung(group.EndgueltigeEntscheidung, auszahlung)


        # Payoffs werden erhöht
        # Problem mit direkten Payoffs ist die Anzeige der Punkte - entweder beides als KR oder beides in POINTS
        # Daher noch einmal extra über die Gruppe
        opfer = group.get_player_by_role(Constants.opfer_role)
        opfer.participant.payoff = opfer.participant.payoff + opferInkrement
        #group.OpferAuszahlungPunkte = group.OpferAuszahlungPunkte + opferInkrement
        session.OpferAuszahlungPunkte += opferInkrement

        # NUR IN DER LETZTEN RUNDE
        #nameOpfer = ''.join(random.sample(string.ascii_uppercase, 6))
        #group.OpferKennung = copy.deepcopy(nameOpfer)
        #group.OpferAuszahlungDKK = group.OpferAuszahlungPunkte / Constants.waehrungsFaktorDKK
        #opfer.payoff = opfer.participant.payoff

        berater = group.get_player_by_role(Constants.berater_role)
        berater.participant.payoff += beraterInkrement
        #group.BeraterAuszahlungPunkte += beraterInkrement
        session.BeraterAuszahlungPunkte += beraterInkrement

        #nameBerater = ''.join(random.sample(string.ascii_uppercase, 6))
        #group.BeraterKennung = copy.deepcopy(nameBerater)
        #group.BeraterAuszahlungPunkte = berater.participant.payoff
        #group.BeraterAuszahlungDKK = berater.participant.payoff / Constants.waehrungsFaktorDKK

        entscheider = group.get_player_by_role(Constants.entscheider_role)
        entscheider.participant.payoff += entscheiderInkrement
        #group.EntscheiderAuszahlungPunkte += entscheiderInkrement
        session.EntscheiderAuszahlungPunkte += entscheiderInkrement

        #nameEntscheider = ''.join(random.sample(string.ascii_uppercase, 6))
        #group.EntscheiderKennung = copy.deepcopy(nameEntscheider)
        #group.EntscheiderAuszahlungDKK = entscheider.participant.payoff / Constants.waehrungsFaktorDKK
        #entscheider.payoff = entscheider.participant.payoff



# Umfrage - nur für den Berater
class SeiteFragenAnDenBerater(Page):
    # timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    form_fields = ["Frage1A", "Frage1B", "Frage1C", "Frage1D","Frage1E", "Frage1F", "Frage2", "Frage3", "Frage4", "Frage5", "Frage61", "Frage62b", "Frage63"]

    @staticmethod
    def is_displayed(player: Player):
        # Nur für den Berater und nur in der letzten Runde
        return (player.participant.zugeordneteRole == Constants.berater_role) and (player.round_number == Constants.num_rounds)

    @staticmethod
    def error_message(player, values):
        if values['Frage1A'] + values['Frage1B'] + values['Frage1C'] + values['Frage1D'] + values['Frage1E'] + values['Frage1F'] != 100:
            return 'ERROR: The sum of the likelihoods for question 1) must add up to 100.'

    @staticmethod
    def vars_for_template(player: Player):
        auszahlung = getAuszahlungArray(player.session, Constants.num_rounds)
        group = player.group
        return {
            'auszahlung': auszahlung,
            'empfehlung': group.BeraterEmpfehlung,
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        group.BeraterEmpfehlung = player.Entscheidung
        #print("Berater Empfehlung: player.Entscheidung: ", player.Entscheidung, " group.BeraterEmpfehlung: ", group.BeraterEmpfehlung)

# Umfrage - nur für den Entscheider
class SeiteFragenAnDenEntscheider(Page):
    # timeout_seconds = Constants.timeOutSeconds
    form_model = 'player'
    # FRAGE 7 steht auf der Form unter der Nummer 4) !!!!!!!!!!!!!!!!!! Die anderen verschieben sich um eine Frage4 ist also 5) usw. "Frage4" ist dagegen nicht drin - Sonst knallt die Vlidierung
    form_fields = ["Frage1A", "Frage1B", "Frage1C", "Frage1D","Frage1E", "Frage1F", "Frage2", "Frage3",  "Frage5", "Frage61", "Frage62e", "Frage63", "Frage7"]

    @staticmethod
    def is_displayed(player: Player):
        # Nur für den Berater und nur in der letzten Runde
        return (player.participant.zugeordneteRole == Constants.entscheider_role) and (player.round_number == Constants.num_rounds)

    @staticmethod
    def error_message(player, values):
        if values['Frage1A'] + values['Frage1B'] + values['Frage1C'] + values['Frage1D'] + values['Frage1E'] + values['Frage1F'] != 100:
            #print(values['Frage1A'] + values['Frage1B'] + values['Frage1C'] + values['Frage1D'] + values['Frage1E'] + values['Frage1F'])
            return 'ERROR: The sum of the likelihoods for question 1) must add up to 100.'

    @staticmethod
    def vars_for_template(player: Player):
        auszahlung = getAuszahlungArray(player.session, Constants.num_rounds)
        group = player.group
        return {
            'auszahlung': auszahlung,
            'empfehlungBerater': group.BeraterEmpfehlung,
            'empfehlung': group.EntscheiderEmpfehlung,
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role),
        }



# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    form_fields = ['Fachrichtung', 'Altersgruppe', 'Geschlecht']

    def is_displayed(player: Player):
        # Nur in der letzten Runde
        return player.round_number == Constants.num_rounds

    def vars_for_template(player: Player):

        group = player.group
        session = player.session

        # ToDO GGF Auszahlungskorrektur
        # if Auszahlung_Punkte_Opfer > 4900:
        #     Auszahlung_Punkte_Opfer = random.randint(135, 246)*20

        opfer = group.get_player_by_role(Constants.opfer_role).participant
        nameOpfer = ''.join(random.sample(string.ascii_uppercase, 6))
        opfer.AuszahlungUserName = copy.deepcopy(nameOpfer)
        group.OpferKennung = copy.deepcopy(nameOpfer)
        # HIER über die Session!
        group.OpferAuszahlungDKK = round(session.OpferAuszahlungPunkte / Constants.waehrungsFaktorDKK, 0)
        group.OpferAuszahlungPunkte = session.OpferAuszahlungPunkte

        berater = group.get_player_by_role(Constants.berater_role).participant
        nameBerater = ''.join(random.sample(string.ascii_uppercase, 6))
        berater.AuszahlungUserName = copy.deepcopy(nameBerater)
        group.BeraterKennung = copy.deepcopy(nameBerater)
        group.BeraterAuszahlungDKK = round(session.BeraterAuszahlungPunkte / Constants.waehrungsFaktorDKK,0)
        group.BeraterAuszahlungPunkte = session.BeraterAuszahlungPunkte

        entscheider = group.get_player_by_role(Constants.entscheider_role).participant
        nameEntscheider = ''.join(random.sample(string.ascii_uppercase, 6))
        entscheider.AuszahlungUserName = copy.deepcopy(nameEntscheider)
        group.EntscheiderKennung = copy.deepcopy(nameEntscheider)
        ## TODO NUR GANZE KRONEN - für andere Währungen könnte man hier auch mit 2 Nachkommastellen arbeiten (auf der Seite dann |to2 statt |to0)
        group.EntscheiderAuszahlungDKK = round(session.EntscheiderAuszahlungPunkte / Constants.waehrungsFaktorDKK, 0)
        group.EntscheiderAuszahlungPunkte = session.EntscheiderAuszahlungPunkte





# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class ErgebnisDisinterestedCouncil(Page):

    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role)

        }


page_sequence = [Intro, RoleBerater, RoleEntscheider, RoleOpfer, QuizBerater, QuizEntscheider, SeiteFuerDenBerater, WarteAufDenBerater, SeiteFuerDenEntscheider, WarteAufDenEntscheider, SeiteFuerDieOpfer, WarteAufDieOpfer, SeiteFragenAnDenBerater, SeiteFragenAnDenEntscheider, AuszahlungUmfrage, ErgebnisDisinterestedCouncil]