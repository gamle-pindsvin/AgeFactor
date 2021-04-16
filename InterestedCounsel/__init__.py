from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'InterestedCounsel'
    players_per_group = 3
    num_rounds = 5

class Subsession(BaseSubsession):
    pass

def my_function(group):
    pass

class Group(BaseGroup):
    my_function = my_function

class Player(BasePlayer):
    istEntscheider = models.BooleanField(initial=False)
    Entscheidung = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C']], widget=widgets.RadioSelect)
    Fachrichtung = models.StringField(choices=[['Man', 'Management'], ['Eco', 'Economics'], ['Law', 'Law'], ['Cog', 'Cognitive Science'], ['Nat', 'Natural Science or Mathematics'], ['Other', 'Other field'], ['None', "I'm not a student"]], widget=widgets.RadioSelect)
    Altersgruppe = models.StringField(choices=[['1', '20 years or less'], ['2', '21 - 24'], ['3', '25 - 28'], ['4', '29 - 35'], ['5', 'more than 35']], widget=widgets.RadioSelect)
    Geschlecht = models.StringField(choices=[['F', 'Female'], ['M', 'Male'], ['D', 'Not listed'], ['N', 'Prefer not to answer']], widget=widgets.RadioSelect)
    AuszahlungInPunkten = models.IntegerField(initial=0)
    AuszahlungInDKK = models.CurrencyField(initial=0)
    AuszahlungUserName = models.StringField()
    istOpfer = models.BooleanField(initial=False)

class Intro(Page):

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player):

        # Rollen werden hier festgelegt
        # Wer in der ersten Runde Opfer ist, bleibt für immer die Opfer
        aktuelleSpielerInDerGruppe = player.group.get_players()

        aktuelleSpielerInDerGruppe[0].istOpfer = True
        aktuelleSpielerInDerGruppe[1].istOpfer = False
        aktuelleSpielerInDerGruppe[2].istOpfer = False

        aktuelleSpielerInDerGruppe[0].istEntscheider = False
        aktuelleSpielerInDerGruppe[1].istEntscheider = False
        aktuelleSpielerInDerGruppe[2].istEntscheider = True

        # Speichern im "Participant" ist wichtig, weil derselbe Spieler in wetieren Runden evtl. eine andere Nummer hat
        player.participant.opfer = player.istOpfer
        player.participant.entscheider = player.istEntscheider

        # Hier muss die "Auszahlungsmatrix" - welche Prämie für welche Entscheidung definiert werden
        # TODO

class Intro_IC(Page):
    form_model = 'player'
page_sequence = [Intro, Intro_IC]