from otree.api import *
import random
import copy
import string

class Constants(BaseConstants):
    name_in_url = 'Interested_Counsel'
    players_per_group = 3
    num_rounds = 6

    # REIHENFOLGE der Rollen wichtig - wird später in player.role übernommen!!!
    opfer_role = 'Opfer'
    entscheider_role = 'Entscheider'
    berater_role = 'Berater'

    timeOutSeconds = 600
    waehrungsFaktorDKK = 7.0

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


class Player(BasePlayer):

    Entscheidung = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F']], widget=widgets.RadioSelect)

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
    Frage62 = models.StringField(choices=[['5', 'Player Y is fully responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Player Y is not responsible']], widget=widgets.RadioSelectHorizontal)
    Frage63 = models.StringField(choices=[['5', 'Player Z is fully responsible'], ['4', '&nbsp;'], ['3', '&nbsp;'], ['2', '&nbsp;'], ['1', '&nbsp;'], ['0', 'Player Z is not responsible']], widget=widgets.RadioSelectHorizontal)


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

        # Folge der Auszahlungen für das Team (das, was in der Runde erhalten wurde, wird diesem Team-Spieler zugeschlagen.
        # SPÄTER EVTL. echte Zufall-Zuordnung
        # 1 - Berater, 2 - Entscheider
        session.AuszahlungImTeamFolge = [1, 1, 2, 2, 1, 2]


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
            print(txtO.format(auswahlChar, result))
    if (not resultFound):
        print("Something gets wrong. group.EndgueltigeEntscheidung: " + auswahlChar)
    return result



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

        #  Jetzt - wer bekommt aus dem Team - Entscheider oder Berater z.B. [1, 1, 2, 2, 1, 2]
        # 1 - Berater, 2 - Entscheider
        AuszahlungImTeamFolge = session.AuszahlungImTeamFolge
        posInArray = round_number - 1
        auszahlungAnBerater = (AuszahlungImTeamFolge[posInArray] == 1)

        # Je nach Auswahl werden die Zuwächse zugewiesen
        # Zuest schauen wir, ob überhaupt etwas übergeben
        if (group.EndgueltigeEntscheidung is not None):
            opferInkrement = getOpferAuszahlung(group.EndgueltigeEntscheidung, auszahlung)
            if auszahlungAnBerater:
                beraterInkrement = getTeamAuszahlung(group.EndgueltigeEntscheidung, auszahlung)
            else:
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
    form_fields = ["Frage1A", "Frage1B", "Frage1C", "Frage1D","Frage1E", "Frage1F", "Frage2", "Frage3", "Frage4", "Frage5", "Frage61", "Frage62", "Frage63"]

    @staticmethod
    def is_displayed(player: Player):
        # Nur für den Berater und nur in der letzten Runde 6
        return (player.participant.zugeordneteRole == Constants.berater_role) and (player.round_number == 6)

    @staticmethod
    def error_message(player, values):
        if values['Frage1A'] + values['Frage1B'] + values['Frage1C'] + values['Frage1E'] + values['Frage1E'] + values['Frage1F'] != 100:
            return 'ERROR: The sum of the likelihoods for question 1) must add up to 100.'

    @staticmethod
    def vars_for_template(player: Player):
        #TODO fest 6, weil in der letzten Runde!!!!
        auszahlung = getAuszahlungArray(player.session, 6)
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

        berater = group.get_player_by_role(Constants.berater_role).participant
        nameBerater = ''.join(random.sample(string.ascii_uppercase, 6))
        berater.AuszahlungUserName = copy.deepcopy(nameBerater)
        group.BeraterKennung = copy.deepcopy(nameBerater)
        group.BeraterAuszahlungDKK = round(session.BeraterAuszahlungPunkte / Constants.waehrungsFaktorDKK,0)

        entscheider = group.get_player_by_role(Constants.entscheider_role).participant
        nameEntscheider = ''.join(random.sample(string.ascii_uppercase, 6))
        entscheider.AuszahlungUserName = copy.deepcopy(nameEntscheider)
        group.EntscheiderKennung = copy.deepcopy(nameEntscheider)
        ## TODO NUR GANZE KRONEN - für andere Währungen könnte man hier auch mit 2 Nachkommastellen arbeiten (auf der Seite dann |to2 statt |to0)
        group.EntscheiderAuszahlungDKK = round(session.EntscheiderAuszahlungPunkte / Constants.waehrungsFaktorDKK, 0)




# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class ErgebnisInterestedCounsel(Page):

    def is_displayed(player: Player):
        # FEST die letzte 12. Runde des letzten Spiels
        # NATÜRLICH AM ENDE - 12 nicht 6 ################################ !!!! ###############################################
        return player.round_number == 6

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'opferPart': (player.participant.zugeordneteRole == Constants.opfer_role),
            'beraterPart': (player.participant.zugeordneteRole == Constants.berater_role),
            'entscheiderPart': (player.participant.zugeordneteRole == Constants.entscheider_role)

        }


page_sequence = [Intro, SeiteFuerDenBerater, WarteAufDenBerater, SeiteFuerDenEntscheider, WarteAufDenEntscheider, SeiteFuerDieOpfer, WarteAufDieOpfer, SeiteFragenAnDenBerater, AuszahlungUmfrage, ErgebnisInterestedCounsel]