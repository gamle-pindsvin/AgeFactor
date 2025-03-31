from otree.api import *
import random
import time
import string
import math
import io
import csv
import os

from uvicorn import Config


class Constants(BaseConstants):
    name_in_url = 'DeciderStage'
    #TODO: Es sollen zwar 800 echte sein, zum Testsen kann man jede vielfache von 32 nutzen.
    players_per_group = 64

    # Pro Gruppe 1 und 6 darf jeweils 200 Spieler sein. Die Gruppen sind bis auf Text identisch
    maximaleAnzahlProGruppe16 = players_per_group / 4

    # Pro Gruppe 2, 3, 4 und 5 darf jeweils 100 Spieler sein, weil man jeweils bei der hälfte die alten zuerst und
    # bei der anderen Hälfte die jungen zuerst zeigt
    maximaleAnzahlProGruppe2345 = players_per_group / 8

    # Pro Gruppe und Sequenz müssen es gleich viele Spieler sein
    maximalAnzahlSequenzProGruppe16 = players_per_group / 16
    maximalAnzahlSequenzProGruppe2345 = players_per_group / 32

    # Sequenzen: Ergebnisse des TeamWorkStage
    TWS_sequenz1 = [[33, 56],[27, 45],[26, 43],[36, 32],[33, 35],[29, 18],[14, 44],[50, 40],[44, 42],[34, 39]]
    TWS_sequenz2 = [[44, 49],[32, 47],[39, 22],[30, 40],[33, 48],[23, 24],[28, 45],[12, 47],[43, 36],[41, 45]]
    TWS_sequenz3 = [[11, 41],[34, 34],[28, 48],[39, 50],[28, 18],[29, 44],[34, 47],[35, 34],[50, 35],[36, 46]]
    TWS_sequenz4 = [[39, 40],[11, 30],[36, 41],[26, 48],[23, 47],[31, 38],[37, 51],[38, 22],[41, 29],[41, 50]]

    # Im Player speichere ich nur die Nummer der Sequenz aus diesem Array
    sequenzen = [TWS_sequenz1, TWS_sequenz2, TWS_sequenz3, TWS_sequenz4]

    num_rounds = 10
    timeOutSeconds = 6000

    # Wie lange soll die Aufgabe gelöst werden
    dauerDesThreatmentsInSekunden = 30

    ######### TEST ########## Auszahlungen für das TEST SPIEL  (RealEffortTask 20-30 Sekunden) ###### TEST ####
    # GBP flat
    festerAnteilderBezahlungRET = 0.40
    # GBP pro richtige Antwort
    bezahlungProAntwortRET = 0.05
    ################### ENDE Auszahlungen für das Test-Spiel (RealEffortTask 20-30 Sekunden) ##########

    ########## ECHT ######### Echte Auszahlungen für Probalnden ### ECHT #######
    # GBP flat
    festerAnteilDerBezahlung = 1.15
    # Genauigkiet - wie Nah muss man das Ergebnis eines Workers treffen. Ist relativ zum gemeinsamen Output der Workers
    # 0.1 heißt 10% und damit ein Intervall [realValue-5% , realValue + 5% des gemeinsamen outputs]
    schaetzgenauigkeit = 0.1
    # GBP pro richtige Antwort
    bezahlungProRichtigeSchaetzung = 0.25
    ################### ENDE AEchte Auszahlungen für Probalnden ##########

    # Für die Quiz - wie oft sollte man hypothetisch spielen
    quizAngenommeneAnzahlAntowrten = 150
    # Umrechnungfaktor aus den Punkten
    waehrungsFaktor = 1
    waehrungsName = 'GBP'

    # Umrechnungfaktor aus den Punkten / E$ z.B. in DKK oder USD
    waehrungsFaktor = 1
    waehrungsName = 'USD'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # Zähle Spieler, die schon der Gruppen/Rollen zugeordnet wurden. Darf nicht mehr als 200/100 sein.
    anzahlSpielerInDerGruppe1 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppe16)
    anzahlSpielerInDerGruppe2 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppe2345)
    anzahlSpielerInDerGruppe3 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppe2345)
    anzahlSpielerInDerGruppe4 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppe2345)
    anzahlSpielerInDerGruppe5 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppe2345)
    # Gruppe 6 ist dasselbe, wie Gruppe 1 - beide Felder ohne Bezeichnung. Aber andere Beschreibung
    anzahlSpielerInDerGruppe6 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppe16)

    # Da man Arrays zurzeit offenbar nur als json-Dump in einem LongStringField speichern kann,
    # werden jetzt int-Variablen für die Begrenzung pro Gruppe und Sequenz eingeführt
    gruppe1_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe1_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe1_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe1_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe2_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe2_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe2_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe2_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe3_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe3_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe3_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe3_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe4_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe4_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe4_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe4_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe5_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe5_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe5_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe5_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe2345)
    gruppe6_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe6_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe6_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)
    gruppe6_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppe16)

class Player(BasePlayer):

    ProlificID = models.StringField( label='')
    AnzahlRichtigerAntworten = models.IntegerField()
    # Rollen T1 sind doppelt so groß, weil die T2 und T3 in Rollen "jung zuerst" und "alt zuerst" aufgespaltet ist.
    # Für die Schätzung wird als erstes das Feld für den "jungeren" und bei  den "älteren" angezeigt
    zugeordneteRole = models.IntegerField()

    # Welche Sequenz - nummer aus dem Constants.sequenzen
    gewaehlteSequenz = models.IntegerField()

    QuizKodieren1 = models.StringField(choices=[['a', 'a'], ['b', 'b'], ['c', 'c']], widget=widgets.RadioSelect, label='')
    QuizKodieren2 = models.StringField(choices=[['a', 'a'], ['b', 'b'], ['c', 'c']], widget=widgets.RadioSelect, label='')
    QuizBezahlung = models.StringField(choices=[['a', 'a'], ['b', 'b'], ['c', 'c']], widget=widgets.RadioSelect, label='')

    # Ergebnisse aus dem vorherigen TeamWorkStage. Tuppel ist immer [oldWorker, youngWorker]
    oldWorker = models.IntegerField(label='')
    youngWorker = models.IntegerField(label='')
    gemeinsamesErgebnisBeiderWorker = models.IntegerField(label='')

    # Und Eingaben der Entscheider, was sie denken, dass einer beigetragen hat
    aktuellesErgebnisTWSSpieler1_Schaetzung = models.IntegerField(label='', blank=True, null=True)
    aktuellesErgebnisTWSSpieler2_Schaetzung = models.StringField(label='', blank=True, null=True, initial="")

    eintrittZeitAufDerSeite = models.FloatField(initial=-1.0)

    # Prüfen, ob man selbst decodieren kann
    SelbstTest = models.StringField(label='')

    # ProlificID - Fehlerhinweis kann noch angezeigt werden
    HinweisLangeProlificID = models.BooleanField(initial=True)

    # Zählt falsche Versuche beim Quiz
    FreiVersucheImQuiz = models.IntegerField(initial=2)
    HatSichQualifiziert = models.BooleanField(initial=True)
    FreiVersucheImQuiz2 = models.IntegerField(initial=2)
    HatSichQualifiziert2 = models.BooleanField(initial=True)

    # Hat "More Details" zur Auszahlung angeschaut
    HatMoreDetailsAngeschaut = models.IntegerField(initial=0)

    # Statistik am Ende
    ConfidentNivau = models.StringField(choices=[['1', 'Not confident at all'],
                                                 ['2', 'Slightly confident'],
                                                 ['3', 'Moderately confident'],
                                                 ['4', 'Very confident'],
                                                 ['5', 'Extremely confident']], widget=widgets.RadioSelect, label='<b>1. </b>How confident are you that your estimates accurately reflect the actual performances?')

    AccuracyOfEstimates = models.IntegerField(min=0, max=100, label='<b>2. </b>If you had to bet on the accuracy of your estimates, what percentage chance (0-100%) would you give that your estimates are close to the actual performances? <b><i>Enter a percentage between 0 and 100.</b></i>')


    PoliticalOrientation = models.StringField(choices=[['1', 'Left (e.g., strongly supports redistribution, government intervention)'],
                                                       ['2', 'Centre-left'],
                                                       ['3', 'Centre (e.g., neither particularly left nor right)'],
                                                       ['4', 'Centre-right'],
                                                       ['5', 'Right (e.g., strongly supports free markets, limited government)'],
                                                       ['6', 'Don’t know / Prefer not to say']], widget=widgets.RadioSelect, label='In politics, people sometimes talk about ‘left’ and ‘right’. Where would you place yourself on the following scale?')
    Education = models.StringField(choices=[['1', 'No formal qualifications'], ['2', 'GCSEs or equivalent (e.g., O-Levels)'], ['3', 'A-Levels or equivalent (e.g., high school diploma)'], ['4', 'Vocational qualification (e.g., NVQ, BTEC)'], ['5', 'Undergraduate degree (e.g., BA, BSc)'], ['6', 'Postgraduate degree (e.g., MA, MSc, PhD)'], ['0', "Other "]], widget=widgets.RadioSelect, label='What is the highest level of education you have completed? ')
    GeburtsJahr = models.IntegerField(min=1920, max=2010, label='In which year were you born?')
    Gender = models.StringField(choices=[['F', 'Female'], ['M', 'Male'], ['D', 'Not listed'], ['N', 'Prefer not to answer']], widget=widgets.RadioSelect, label='What is your gender?')
    Occupation = models.StringField(choices=[['1', 'Senior Manager / Director (e.g., CEO, finance director, senior civil servant)'],
                                             ['2', 'Professional with Management Responsibilities (e.g., doctor managing a team, senior engineer)'],
                                             ['3', 'Professional without Management Responsibilities (e.g., teacher, nurse, software developer)'],
                                             ['4', 'Skilled Worker / Technician (e.g., electrician, mechanic, police officer)'],
                                             ['5', 'Clerical / Administrative Worker (e.g., office assistant, receptionist, call center worker)'],
                                             ['6', 'Manual Worker / Labourer (e.g., factory worker, construction worker, delivery driver)'],
                                             ['7', 'Self-Employed – With Employees (e.g., business owner, shop owner with staff)'],
                                             ['8', 'Self-Employed – Without Employees (e.g., freelancer, independent consultant, sole trader)'],
                                             ['9', "Other"]], widget=widgets.RadioSelect, label='Which of the following best describes your current occupation? (If unemployed or retired, please select your most recent occupation.)')
    Household = models.StringField(choices=[['1', 'Single-person household'],
                                         ['2', 'Household with only adults of the same generation (e.g., housemates, couple without children, siblings)'],
                                         ['3', 'Household with adults and children (e.g., parents with children under 18, guardians with dependents)'],
                                         ['4', 'Multigenerational household (e.g., at least two adult generations living together, such as grandparents, parents, and children)'],
                                         ['5', 'Other']], widget=widgets.RadioSelect, label='Which of the following best describes your household composition?')
    OlderInPrivate = models.StringField(choices=[['1', 'Very frequently'],
                                            ['2', 'Occasionally'],
                                            ['3', 'Sometimes'],
                                            ['4', 'Rarely'],
                                            ['5', 'Very rarely']], widget=widgets.RadioSelect, label='How frequently do you have contact with individuals aged 55 or older in your private life (e.g., family, friends, …)?')
    OlderInProfessional = models.StringField(choices=[['1', 'Very frequently'],
                                                 ['2', 'Occasionally'],
                                                 ['3', 'Sometimes'],
                                                 ['4', 'Rarely'],
                                                 ['5', 'Very rarely']], widget=widgets.RadioSelect, label='How frequently do you have contact with individuals aged 55 or older in your professional life (e.g., colleagues, customers, …)?')
    Discrimination = models.StringField(choices=[['1', 'Gender'],
                                                      ['2', 'Age'],
                                                      ['3', 'Ethnicity'],
                                                      ['4', 'Disability (or Handicap, depending on preference)'],
                                                      ['5', 'Sexual orientation'],
                                                      ['6', 'Other reasons']], label='Have you ever experienced discrimination because of the following reasons?')
    era4 = models.StringField(choices=[['1', 'Definitely True'], ['2', 'Somewhat True'], ['3', 'Somewhat False'], ['4', 'Definitely False']], widget=widgets.RadioSelect,
                                                    label='<b>Please indicate to what extent you think the following statements are true.</b><br><br>"Every year that people age, their energy levels go down a little more."')
    era9 = models.StringField(choices=[['1', 'Definitely True'], ['2', 'Somewhat True'], ['3', 'Somewhat False'], ['4', 'Definitely False']], widget=widgets.RadioSelect,
                                                    label='"I expect that as I get older I will become more forgetful."')
    era10 = models.StringField(choices=[['1', 'Definitely True'], ['2', 'Somewhat True'], ['3', 'Somewhat False'], ['4', 'Definitely False']], widget=widgets.RadioSelect,
                                                    label='"It’s an accepted part of aging to have trouble remembering names."')
    era11 = models.StringField(choices=[['1', 'Definitely True'], ['2', 'Somewhat True'], ['3', 'Somewhat False'], ['4', 'Definitely False']], widget=widgets.RadioSelect,
                                                    label='"Forgetfulness is a natural occurrence just from growing old."')
    era12 = models.StringField(choices=[['1', 'Definitely True'], ['2', 'Somewhat True'], ['3', 'Somewhat False'], ['4', 'Definitely False']], widget=widgets.RadioSelect,
                                                    label='"It is impossible to escape the mental slowness that happens with aging."')


    #Am Ende ggf. mit real_world_currency_per_point im Config korrigieren
    AuszahlungInWaehrung = models.IntegerField(initial=0)
    # Wie viel wurde in dem 20-Sekundigen Testspiel verdient
    VerdientePunkteImTestSpiel = models.IntegerField(initial=0)
    VerdientePunkte = models.IntegerField(initial=0)
    AuszahlungWaehrungName = models.StringField();

    # Checkbox für Consent
    Akzeptiert_bedingungen = models.BooleanField(label="", widget=widgets.CheckboxInput, blank=True)

    #TODO DANACH LÖSCHEN NUR SLIDER TEST
    slider_value = models.IntegerField(null=True, blank=True)


    # Es wird geprüft, ob er das Intervall zu einem der beiden Ergebnisse trifft, wenn ja: +1
    # Intervall wird dynamisch berechnet als z.B. 10% der gemeinsamen Outputs des Spieler 1 und 2, also +/-5%.
    # Diese z.B. 10% sind in der Variable Constants.schaetzgenauigkeit gespeichert
def berechneAuszahlungT1(ergebnisSpieler1, ergebnisSpieler2, schaetzung):
    result = 0

    diff1 = abs(ergebnisSpieler1 - schaetzung)
    diff2 = abs(ergebnisSpieler2 - schaetzung)

    # Wähle die kleinste Differenz
    minimaleDiff = min(diff1, diff2)

    # ist der Abstand kleiner als die (Output*10%/2)
    schwelle = (ergebnisSpieler1 + ergebnisSpieler2)*Constants.schaetzgenauigkeit/2

    if (minimaleDiff <= schwelle):
        result = 1
    #print('S1: ', ergebnisSpieler1, 'S2: ', ergebnisSpieler2, ' Eingabe: ', schaetzung,  ' diff1: ', diff1, ' diff2: ', diff2 , ' result: ', result)
    return result

# Es wird geprüft, ob er das Intervall dem gegebenen Ergebnisse trifft, wenn ja: +1
# Intervall wird durch
# Spielerwird mal als junger mal als alter Spieler dargestellt. Beim Aufruf wird aber der richtige Übergeben
def berechneAuszahlung(ergebnisSpieler, summe, schaetzung):
    result = 0
    diff1 = abs(ergebnisSpieler - schaetzung)
    # ist der Abstand kleiner als die (Output*10%/2)
    schwelle = summe*Constants.schaetzgenauigkeit/2
    if diff1 <= schwelle:
        result = 1
    #print('S1: ', ergebnisSpieler, ' Eingabe: ', schaetzung,  ' diff1: ', diff1, ' result: ', result)
    return result

# Ist die Anzahl der Probanden pro Rolle schon ausgeschöpft - z.B. 200 - oder gibt es noch frei Plätze
# Wenn ja, gibt es für diese Rolle noch passende Sequenzen
# RETURN - Sequenzummer - wenn nicht gefunden - -1
def gibSequenzFuerDieRolle(player, rollenNummer):
    gruppe = player.group
    result = -1
    # Ziehe eine Sequenz
    zufallSequenz = random.randint(1, 4)
    if rollenNummer == 1:
        # Gibt es überhaupt noch Platz in der Gruppe
        if gruppe.anzahlSpielerInDerGruppe1 >=1:
            # ... Und gibt es noch eine Freie Sequenz für die Gruppe, bzw. die oben gewählte zufallSequenz
            if isMengeProSequenzNochNichtVoll(player, rollenNummer, zufallSequenz):
                gruppe.anzahlSpielerInDerGruppe1 = gruppe.anzahlSpielerInDerGruppe1-1
                reduziereMengeProSequenzUndRolle(player, rollenNummer, zufallSequenz)
                result = zufallSequenz
    elif rollenNummer == 2:
        if gruppe.anzahlSpielerInDerGruppe2 >=1:
            if isMengeProSequenzNochNichtVoll(player, rollenNummer, zufallSequenz):
                gruppe.anzahlSpielerInDerGruppe2 = gruppe.anzahlSpielerInDerGruppe2-1
                reduziereMengeProSequenzUndRolle(player, rollenNummer, zufallSequenz)
                result = zufallSequenz
    elif rollenNummer == 3:
        if gruppe.anzahlSpielerInDerGruppe3 >=1:
            if isMengeProSequenzNochNichtVoll(player, rollenNummer, zufallSequenz):
                gruppe.anzahlSpielerInDerGruppe3 = gruppe.anzahlSpielerInDerGruppe3-1
                reduziereMengeProSequenzUndRolle(player, rollenNummer, zufallSequenz)
                result = zufallSequenz
    elif rollenNummer == 4:
        if gruppe.anzahlSpielerInDerGruppe4 >=1:
            if isMengeProSequenzNochNichtVoll(player, rollenNummer, zufallSequenz):
                gruppe.anzahlSpielerInDerGruppe4 = gruppe.anzahlSpielerInDerGruppe4-1
                reduziereMengeProSequenzUndRolle(player, rollenNummer, zufallSequenz)
                result = zufallSequenz
    elif rollenNummer == 5:
        if gruppe.anzahlSpielerInDerGruppe5 >=1:
            if isMengeProSequenzNochNichtVoll(player, rollenNummer, zufallSequenz):
                gruppe.anzahlSpielerInDerGruppe5 = gruppe.anzahlSpielerInDerGruppe5-1
                reduziereMengeProSequenzUndRolle(player, rollenNummer, zufallSequenz)
                result = zufallSequenz
    elif rollenNummer == 6:
        # Gibt es überhaupt noch Platz in der Gruppe
        if gruppe.anzahlSpielerInDerGruppe6 >=1:
            # ... Und gibt es noch eine Freie Sequenz für die Gruppe, bzw. die oben gewählte zufallSequenz
            if isMengeProSequenzNochNichtVoll(player, rollenNummer, zufallSequenz):
                gruppe.anzahlSpielerInDerGruppe6 = gruppe.anzahlSpielerInDerGruppe6-1
                reduziereMengeProSequenzUndRolle(player, rollenNummer, zufallSequenz)
                result = zufallSequenz
    else:
        print('FEHLER: gibSequenzFuerDieRolle, RollenNummer nicht zwischen 1 und 6 sondern: ', rollenNummer)

    return result

# Ist die Anzahl der Probanden pro Sequenz und Rolle - z.B. 50 - schon ausgeschöpft
# Matrix wäre einfacher, aber scheint nicht so einfach in GROUP speicherbar
def isMengeProSequenzNochNichtVoll(player, rollenNummer, sequenzNummer):
    gruppe = player.group
    if rollenNummer == 1:
        if sequenzNummer == 1:
            return gruppe.gruppe1_sequenz1  >= 1
        elif sequenzNummer == 2:
            return gruppe.gruppe1_sequenz2  >= 1
        elif sequenzNummer == 3:
            return gruppe.gruppe1_sequenz3  >= 1
        elif sequenzNummer == 4:
            return gruppe.gruppe1_sequenz4  >= 1
    elif rollenNummer == 2:
        if sequenzNummer == 1:
            return gruppe.gruppe2_sequenz1  >= 1
        elif sequenzNummer == 2:
            return gruppe.gruppe2_sequenz2  >= 1
        elif sequenzNummer == 3:
            return gruppe.gruppe2_sequenz3  >= 1
        elif sequenzNummer == 4:
            return gruppe.gruppe2_sequenz4  >= 1
    elif rollenNummer == 3:
        if sequenzNummer == 1:
            return gruppe.gruppe3_sequenz1  >= 1
        elif sequenzNummer == 2:
            return gruppe.gruppe3_sequenz2  >= 1
        elif sequenzNummer == 3:
            return gruppe.gruppe3_sequenz3  >= 1
        elif sequenzNummer == 4:
            return gruppe.gruppe3_sequenz4  >= 1
    elif rollenNummer == 4:
        if sequenzNummer == 1:
            return gruppe.gruppe4_sequenz1  >= 1
        elif sequenzNummer == 2:
            return gruppe.gruppe4_sequenz2  >= 1
        elif sequenzNummer == 3:
            return gruppe.gruppe4_sequenz3  >= 1
        elif sequenzNummer == 4:
            return gruppe.gruppe4_sequenz4  >= 1
    elif rollenNummer == 5:
        if sequenzNummer == 1:
            return gruppe.gruppe5_sequenz1  >= 1
        elif sequenzNummer == 2:
            return gruppe.gruppe5_sequenz2  >= 1
        elif sequenzNummer == 3:
            return gruppe.gruppe5_sequenz3  >= 1
        elif sequenzNummer == 4:
            return gruppe.gruppe5_sequenz4  >= 1
    elif rollenNummer == 6:
        if sequenzNummer == 1:
            return gruppe.gruppe6_sequenz1  >= 1
        elif sequenzNummer == 2:
            return gruppe.gruppe6_sequenz2  >= 1
        elif sequenzNummer == 3:
            return gruppe.gruppe6_sequenz3  >= 1
        elif sequenzNummer == 4:
            return gruppe.gruppe6_sequenz4  >= 1
    else:
        print("FEHLER: isMengeProSequenzNochNichtVoll / rollenNummer: ", rollenNummer)



# Wenn die Sequenz genommen wurde, muss die Anzahl freiher Sequenzen reduziert werden
def reduziereMengeProSequenzUndRolle(player, rollenNummer, sequenzNummer):
    gruppe = player.group
    if rollenNummer == 1:
        if sequenzNummer == 1:
            gruppe.gruppe1_sequenz1 = gruppe.gruppe1_sequenz1-1
        elif sequenzNummer == 2:
            gruppe.gruppe1_sequenz2 = gruppe.gruppe1_sequenz2-1
        elif sequenzNummer == 3:
            gruppe.gruppe1_sequenz3 = gruppe.gruppe1_sequenz3-1
        elif sequenzNummer == 4:
            gruppe.gruppe1_sequenz4 = gruppe.gruppe1_sequenz4-1
    elif rollenNummer == 2:
        if sequenzNummer == 1:
            gruppe.gruppe2_sequenz1 = gruppe.gruppe2_sequenz1-1
        elif sequenzNummer == 2:
            gruppe.gruppe2_sequenz2 = gruppe.gruppe2_sequenz2-1
        elif sequenzNummer == 3:
            gruppe.gruppe2_sequenz3 = gruppe.gruppe2_sequenz3-1
        elif sequenzNummer == 4:
            gruppe.gruppe2_sequenz4 = gruppe.gruppe2_sequenz4-1
    elif rollenNummer == 3:
        if sequenzNummer == 1:
            gruppe.gruppe3_sequenz1 = gruppe.gruppe3_sequenz1-1
        elif sequenzNummer == 2:
            gruppe.gruppe3_sequenz2 = gruppe.gruppe3_sequenz2-1
        elif sequenzNummer == 3:
            gruppe.gruppe3_sequenz3 = gruppe.gruppe3_sequenz3-1
        elif sequenzNummer == 4:
            gruppe.gruppe3_sequenz4 = gruppe.gruppe3_sequenz4-1
    elif rollenNummer == 4:
        if sequenzNummer == 1:
            gruppe.gruppe4_sequenz1 = gruppe.gruppe4_sequenz1-1
        elif sequenzNummer == 2:
            gruppe.gruppe4_sequenz2 = gruppe.gruppe4_sequenz2-1
        elif sequenzNummer == 3:
            gruppe.gruppe4_sequenz3 = gruppe.gruppe4_sequenz3-1
        elif sequenzNummer == 4:
            gruppe.gruppe4_sequenz4 = gruppe.gruppe4_sequenz4-1
    elif rollenNummer == 5:
        if sequenzNummer == 1:
            gruppe.gruppe5_sequenz1 = gruppe.gruppe5_sequenz1-1
        elif sequenzNummer == 2:
            gruppe.gruppe5_sequenz2 = gruppe.gruppe5_sequenz2-1
        elif sequenzNummer == 3:
            gruppe.gruppe5_sequenz3 = gruppe.gruppe5_sequenz3-1
        elif sequenzNummer == 4:
            gruppe.gruppe5_sequenz4 = gruppe.gruppe5_sequenz4-1
    elif rollenNummer == 6:
        if sequenzNummer == 1:
            gruppe.gruppe6_sequenz1 = gruppe.gruppe6_sequenz1-1
        elif sequenzNummer == 2:
            gruppe.gruppe6_sequenz2 = gruppe.gruppe6_sequenz2-1
        elif sequenzNummer == 3:
            gruppe.gruppe6_sequenz3 = gruppe.gruppe6_sequenz3-1
        elif sequenzNummer == 4:
            gruppe.gruppe6_sequenz4 = gruppe.gruppe6_sequenz4-1
    else:
        print("FEHLER: reduziereMengeProSequenzUndRolle / rollenNummer: ", rollenNummer)

# Wir wollen prüfen, wie lange der Spieler auf der SEite war. Die Zeit wird pro Runde gesichert.
# Da die oTree-Modelle keine Arrays direkt unterstützen und die Funktionalität zu oft benutzt ist (so dass
# json-Dump nicht performant ist) wird diese Funktion genutzt
def speichereZeitAufDerSeite(player, dauerAufDerSeite):
    roundNummer = player.round_number
    if roundNummer == 1:
        player.participant.zeitRunde1 = dauerAufDerSeite
    elif roundNummer == 2:
        player.participant.zeitRunde2 = dauerAufDerSeite
    elif roundNummer == 3:
        player.participant.zeitRunde3 = dauerAufDerSeite
    elif roundNummer == 4:
        player.participant.zeitRunde4 = dauerAufDerSeite
    elif roundNummer == 5:
        player.participant.zeitRunde5 = dauerAufDerSeite
    elif roundNummer == 6:
        player.participant.zeitRunde6 = dauerAufDerSeite
    elif roundNummer == 7:
        player.participant.zeitRunde7 = dauerAufDerSeite
    elif roundNummer == 8:
        player.participant.zeitRunde8 = dauerAufDerSeite
    elif roundNummer == 9:
        player.participant.zeitRunde9 = dauerAufDerSeite
    elif roundNummer == 10:
        player.participant.zeitRunde10 = dauerAufDerSeite
    else:
        print("FEHLER: speichereZeitAufDerSeite / roundNummer: ", roundNummer)


class Intro(Page):
    form_model = 'player'
    form_fields = ["ProlificID"]

    # einmal warnen wir, dass ProlificID ggf. nicht korrekt ist
    einmaligeWartung = True

    @staticmethod
    def is_displayed(player: Player):
        #TODO HIER NUR UM SLIDER zu testen - DANACH LÖSCHEN!!!!
        #player.slider_value = 23
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
        gruppe = player.group


        # Welche Rolle
        # Wir bleiben solange in einer Schleife, bis der Probant einer Rolle (T1, T2 oder T3) zugeordnet ist
        # War für eine Rolle schon genug Teilnehmer zugeordnet, wird neue Zufallszahl generiert

        # Rolle wird später bei der Sequenz noch einmal gebraucht
        rolle = -1
        weiterRolleSuchen = True
        while weiterRolleSuchen:
            # Rolle 1 soll doppellt so oft erscheinen als 2 bis 5
            zufallszahl = random.randint(1, 8)

            #print("Intro: zufallszahl: ", zufallszahl)

            if (zufallszahl == 1 or zufallszahl == 2):
                # die Rolle wäre 1, es sei denn, es gibt keine "freie" Sequenz mehr für die Gruppe 1
                sequenzNummer = gibSequenzFuerDieRolle(player, 1)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 1
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 1
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif (zufallszahl == 7 or zufallszahl == 8):
                sequenzNummer = gibSequenzFuerDieRolle(player, 6)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 6
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 6
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 3:
                sequenzNummer = gibSequenzFuerDieRolle(player, 2)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 2
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 2
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 5:
                sequenzNummer = gibSequenzFuerDieRolle(player, 3)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 3
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 3
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 6:
                sequenzNummer = gibSequenzFuerDieRolle(player, 4)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 4
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 4
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 4:
                sequenzNummer = gibSequenzFuerDieRolle(player, 5)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 5
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 5
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            else:
                print("FEHLER: weiterRolleSuchen / zufallszahl: ", zufallszahl)

        # Welche Sequenz
        # Wir bleiben solange in einer Schleife, bis einem Probant eine Sequenz zugeordnet ist
        # Es muss jedoch pro Rolle UND Sequenz am Ende gleich viele Probanden geben (also z.B. 50 aus 600 Teilnehmer
        # bei 3 Rollen und 4 Sequenzen)
        # War für eine Rolle/Sequenz-KOmbi schon genug Teilnehmer zugeordnet, wird neue Zufallszahl generiert

        #sequenzNummerZurAusgabe = -1

        #weiterSequenzSuchen = True
        #while weiterSequenzSuchen:
            #zufallSequenz = random.randint(1, 4)

            #if zufallSequenz == 1 and isMengeProSequenzNochNichtVoll(player, rolle, 1):
            #    player.gewaehlteSequenz = 1;
            #    sequenzNummerZurAusgabe = 1;
            #    weiterSequenzSuchen = False
            #elif zufallSequenz == 2 and isMengeProSequenzNochNichtVoll(player, rolle, 2):
            #    player.gewaehlteSequenz = 2;
            #    sequenzNummerZurAusgabe = 2;
            #    weiterSequenzSuchen = False
            #elif zufallSequenz == 3 and isMengeProSequenzNochNichtVoll(player, rolle, 3):
            #    player.gewaehlteSequenz = 3;
            #    sequenzNummerZurAusgabe = 3;
            #    weiterSequenzSuchen = False
            #elif zufallSequenz == 4 and isMengeProSequenzNochNichtVoll(player, rolle, 4):
            #    player.gewaehlteSequenz = 4;
            #    sequenzNummerZurAusgabe = 4;
            #    weiterSequenzSuchen = False
            #else:
             #   print("FEHLER: weiterSequenzSuchen / zufallSequenz: ", zufallSequenz)

        #print("Rolle: ", player.zugeordneteRole, " Sequenz #: ",player.gewaehlteSequenz)
        #print("Neue freie Rollen: [", gruppe.anzahlSpielerInDerGruppe1, ", " , gruppe.anzahlSpielerInDerGruppe2, ", " ,gruppe.anzahlSpielerInDerGruppe3, ", " ,gruppe.anzahlSpielerInDerGruppe4, ", ", gruppe.anzahlSpielerInDerGruppe5, ", ", gruppe.anzahlSpielerInDerGruppe6, "]")
        #print("Sequenzen: [[", gruppe.gruppe1_sequenz1, ", " , gruppe.gruppe1_sequenz2, ", " ,gruppe.gruppe1_sequenz3, ", " ,gruppe.gruppe1_sequenz4, "], [" ,
        #                       gruppe.gruppe2_sequenz1, ", " , gruppe.gruppe2_sequenz2, ", " ,gruppe.gruppe2_sequenz3, ", " ,gruppe.gruppe2_sequenz4, "], [" ,
        #                       gruppe.gruppe3_sequenz1, ", " , gruppe.gruppe3_sequenz2, ", " ,gruppe.gruppe3_sequenz3, ", " ,gruppe.gruppe3_sequenz4, "], [" ,
        #                       gruppe.gruppe4_sequenz1, ", " , gruppe.gruppe4_sequenz2, ", " ,gruppe.gruppe4_sequenz3, ", " ,gruppe.gruppe4_sequenz4, "], [" ,
        #                       gruppe.gruppe5_sequenz1, ", " , gruppe.gruppe5_sequenz2, ", " ,gruppe.gruppe5_sequenz3, ", " ,gruppe.gruppe5_sequenz4, "], [" ,
        #                       gruppe.gruppe6_sequenz1, ", " , gruppe.gruppe6_sequenz2, ", " ,gruppe.gruppe6_sequenz3, ", " ,gruppe.gruppe6_sequenz4, "]]")

        #TODO HIER NUR UM ALLES IN T1 zu testen - DANACH LÖSCHEN!!!!
        #player.zugeordneteRole = 1;
        #player.participant.zugeordneteRole = 1;

# DAS WAR EINLESEN ÜBER EINE DATEI - DIES WIRD NICHT MEHR GEBRAUCHT
        # Hier werden die Ergebnisse des TeamWorkStage eingelesen
        # Constants.trennzeichen ist für Windows \ und für Heroku /
        #
        # Muss schon hier passieren, damit man nicht jedes mal die Datei neu lädt
        #fileNameMitOSTrenner = "DeciderStage" + os.sep + "resultTWS.csv"

        #with open(fileNameMitOSTrenner, encoding='utf-8-sig', newline='') as file:
        ##rows = list(csv.DictReader(file))
        #    reader = csv.reader(file)
        #    rows = list(reader)
        #session.ergebnisseVonTWS = rows

        #print('Participant', player.participant.ProlificID, ' Player ID: ', player.ProlificID)
        # Neues Spiel - neue Auszahlung.
        player.payoff = 0
        player.participant.payoff = 0
        player.AuszahlungInWaehrung = 0
        player.VerdientePunkte = 0
        player.participant.VerdientePunkte = 0
        player.VerdientePunkteImTestSpiel = 0
        player.participant.VerdientePunkteImTestSpiel = 0

        player.AnzahlRichtigerAntworten = 0


class Intro2(Page):
    form_model = 'player'
    form_fields = ['Akzeptiert_bedingungen']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        # print(values['Akzeptiert_bedingungen'])
        # Checkbox nicht ausgewählt
        if ( not (values['Akzeptiert_bedingungen'])):
            return 'Please confirm that you have read the instructions and the Informed Consent'

    # Hier merken wir, ob jemand auf "More Details" für Auszahlung geklickt hat
    @staticmethod
    def live_method(player, data):
        #print('$$ 01 $$ data: ', data)
        # Nur wenn data nicht NULL ist
        if data is not None:

            #print('$$ 1 $$ data: ', data)
            if (data == 1):
                #print('$$ 11 $$ data: 1')
                player.HatMoreDetailsAngeschaut = 1
                player.participant.HatMoreDetailsAngeschaut = 1
            else:
                #print('$$ liveData sendet nicht 1 sondern ', data)
                player.HatMoreDetailsAngeschaut = 0
                player.participant.HatMoreDetailsAngeschaut = 0





# Verständnis-Quiz, Teil 1 VOR dem Spiel
class Quiz(Page):
    form_model = 'player'
    form_fields = ["QuizKodieren2"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        # Wenn player.FreiVersucheImQuiz 0 werden, geht weiter, aber gleich zu der Auszahlungsseite.
        #print('ERROR!!')
        quizKorrekt = ((values['QuizKodieren2'] == 'c'))
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
                #print('ELSE!!')
                player.HatSichQualifiziert = False
        else:
            #print('KORREKT!!')
            pass

    @staticmethod
    def vars_for_template(player: Player):
        #Werte für die Auszahlungsfragen
        #print('VAR!!')
        antwortA = Constants.quizAngenommeneAnzahlAntowrten*Constants.bezahlungProAntwortRET
        antwortB = Constants.quizAngenommeneAnzahlAntowrten * Constants.bezahlungProAntwortRET + Constants.festerAnteilderBezahlungRET
        antwortC = Constants.quizAngenommeneAnzahlAntowrten + Constants.festerAnteilderBezahlungRET
        return {
            'AntwortA': antwortA,
            'AntwortB': antwortB,
            'AntwortC': antwortC
        }


class RealEffortTask(Page):
    form_model = 'player'
    form_fields = ["AnzahlRichtigerAntworten"]
    timeout_seconds = Constants.dauerDesThreatmentsInSekunden

    @staticmethod
    # Wird bei denen NICHT anzgezeigt, die das Quiz nicht geschafft haben.
    def is_displayed(player: Player):
        #print('HatSichQualifiziert: ', player.HatSichQualifiziert)
        return (player.HatSichQualifiziert and player.round_number == 1)

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'dauerDesThreatmentsInSekunden': Constants.dauerDesThreatmentsInSekunden
        }

    @staticmethod
    def live_method(player, data):
        # Initial auszahlung = 0
        auszahlung = 0.0
        # Nur wenn data nicht NULL ist
        if data is not None:
            #print('$$ 1 $$ data: ',data)
            player.participant.AnzahlRichtigerAntworten = data
            player.AnzahlRichtigerAntworten = data
            #print('$$ 1 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)

            # BERECHNE die Auszahlung
            auszahlung = Constants.festerAnteilderBezahlungRET + data * Constants.bezahlungProAntwortRET
        else:
            player.participant.AnzahlRichtigerAntworten = 0
            player.AnzahlRichtigerAntworten = 0
            auszahlung = Constants.festerAnteilderBezahlungRET

        # Verdiente Punkt ist ein Integer, nicht float
        player.VerdientePunkteImTestSpiel = int(auszahlung)
        player.participant.VerdientePunkteImTestSpiel = int(auszahlung)


        #print('player.participant.ProlificID: ', player.participant.ProlificID, ' player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten, ' player.participant.VerdientePunkte: ', player.participant.VerdientePunkte)
        #print('player.ProlificID: ', player.ProlificID, ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten, ' player.VerdientePunkte: ', player.VerdientePunkte)
        #print('received a bid from', player.id_in_group, ':', data)
        #print('player.participant.AnzahlRichtigerAntworten', player.participant.AnzahlRichtigerAntworten)
        #print('$$ 2 $$ player.participant.AnzahlRichtigerAntworten: ', player.participant.AnzahlRichtigerAntworten , ' player.AnzahlRichtigerAntworten: ', player.AnzahlRichtigerAntworten)



# Erklärung, was eine Histogramm ist.
class BeforeEstimation(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return (player.HatSichQualifiziert and player.round_number == 1)


# Verständnis-Quiz, Teil 2 NACH dem Spiel
class Quiz2(Page):
    form_model = 'player'
    form_fields = ["QuizBezahlung"]

    @staticmethod
    def is_displayed(player: Player):
        return (player.HatSichQualifiziert and player.round_number == 1)

    @staticmethod
    def error_message(player, values):
        # Wenn player.FreiVersucheImQuiz 0 werden, geht weiter, aber gleich zu der Auszahlungsseite.
        quizKorrekt = (values['QuizBezahlung'] == 'c')

        if not quizKorrekt:
            #print('NICHT KORREKT player.FreiVersucheImQuiz war: ', player.FreiVersucheImQuiz, " / quizKorrekt: ", quizKorrekt)
            player.FreiVersucheImQuiz2 -= 1
            if player.FreiVersucheImQuiz2 > 0 :
                #print('Try again please. One or both answers are not yet correct. You have ', str(player.FreiVersucheImQuiz), ' attempts left.')
                return 'Try again please. One or more answers are not yet correct. You have ' + str(player.FreiVersucheImQuiz2) + ' attempts left.'
            else:
                #keine Freiversuche mehr
                player.HatSichQualifiziert = False
        else:
            #print('KORREKT!!')
            pass

    @staticmethod
    def vars_for_template(player: Player):
        #Werte für die Auszahlungsfragen
        antwortA = Constants.quizAngenommeneAnzahlAntowrten*Constants.bezahlungProAntwortRET
        antwortB = Constants.quizAngenommeneAnzahlAntowrten * Constants.bezahlungProAntwortRET + Constants.festerAnteilderBezahlungRET
        antwortC = Constants.quizAngenommeneAnzahlAntowrten + Constants.festerAnteilderBezahlungRET
        return {
            'AntwortA': antwortA,
            'AntwortB': antwortB,
            'AntwortC': antwortC
        }


# Nur für die Rolle T1
class SeiteFuerT1(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 1 and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):


        # Ziehe einer der Ergebnisse aus TWS
        #aktuellAngezeigteErgebnisse = waehleEinErgebnisAusTWS(player)

        #print("Constants.sequenzen:", Constants.sequenzen)
        #print("player.participant.gewaehlteSequenz:", player.participant.gewaehlteSequenz)
        #print("player.gewaehlteSequenz:", player.gewaehlteSequenz)

        # Arbeitsergebnisse aus der Sequenz
        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        #print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker


        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('aktuellesErgebnisTWSSpieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('aktuellesErgebnisTWSSpieler2_Schaetzung')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
        # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'aktuellesErgebnisTWSSpieler1_Schaetzung': inputFieldValue,
            'summe': summe
    }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        # Hat er Intervall für EINEN der beiden Worker getroffen?
        neuePunkteInDieserRunde = berechneAuszahlungT1(player.oldWorker, player.youngWorker, player.aktuellesErgebnisTWSSpieler1_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)



# Nur für die Rolle T1 mit genauer Beschreibung
class SeiteFuerT1genau(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 6 and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):


        # Arbeitsergebnisse aus der Sequenz
        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        #print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker

        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('aktuellesErgebnisTWSSpieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('aktuellesErgebnisTWSSpieler2_Schaetzung')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'aktuellesErgebnisTWSSpieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        # Hat er Intervall für EINEN der beiden Worker getroffen?
        neuePunkteInDieserRunde = berechneAuszahlungT1(player.oldWorker, player.youngWorker, player.aktuellesErgebnisTWSSpieler1_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)

# Nur für die Rolle T2 mit JUNGEN Worker vorne - intern Rolle 2
class SeiteFuerT2j(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 2  and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):

        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        #print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker

        #print(arbeitsergebnisse)
        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('aktuellesErgebnisTWSSpieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('aktuellesErgebnisTWSSpieler2_Schaetzung')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'aktuellesErgebnisTWSSpieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        # Hat er Intervall für den JUNGEN Worker getroffen?
        # JUNGER Worker ist immer der Spieler 2
        neuePunkteInDieserRunde = berechneAuszahlung(player.youngWorker, player.gemeinsamesErgebnisBeiderWorker, player.aktuellesErgebnisTWSSpieler1_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)


# Nur für die Rolle T2 mit ALTEN Worker vorne - intern Rolle 3
class SeiteFuerT2a(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 3 and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):

        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        #print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker

        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('aktuellesErgebnisTWSSpieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('aktuellesErgebnisTWSSpieler2_Schaetzung')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'aktuellesErgebnisTWSSpieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        # Hat er Intervall für den Alten Worker getroffen?
        # ALTER Worker ist immer der Spieler 1
        neuePunkteInDieserRunde = berechneAuszahlung(player.oldWorker, player.gemeinsamesErgebnisBeiderWorker, player.aktuellesErgebnisTWSSpieler1_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)


# Nur für die Rolle T3 mit JUNGEN Worker vorne - intern Rolle 4
class SeiteFuerT3j(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 4 and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):

        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        #print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker


        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('aktuellesErgebnisTWSSpieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('aktuellesErgebnisTWSSpieler2_Schaetzung')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'aktuellesErgebnisTWSSpieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        # Hat er Intervall für den JUNGEN Worker getroffen?
        # JUNGER Worker ist immer der Spieler 2
        neuePunkteInDieserRunde = berechneAuszahlung(player.youngWorker, player.gemeinsamesErgebnisBeiderWorker, player.aktuellesErgebnisTWSSpieler1_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)



# Nur für die Rolle T3 mit ALTEN Worker vorne - intern Rolle 5
class SeiteFuerT3a(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["aktuellesErgebnisTWSSpieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        #print("Komme gleich auf die Seite: ", player.eintrittZeitAufDerSeite)
        return (player.participant.zugeordneteRole == 5 and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):

        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        #print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker

        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('aktuellesErgebnisTWSSpieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('aktuellesErgebnisTWSSpieler2_Schaetzung')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'aktuellesErgebnisTWSSpieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        #print("War auf Seite: ", dauerAufDerSeite, " s")

        # Hat er Intervall für den Alten Worker getroffen?
        # ALTER Worker ist immer der Spieler 1
        neuePunkteInDieserRunde = berechneAuszahlung(player.oldWorker, player.gemeinsamesErgebnisBeiderWorker, player.aktuellesErgebnisTWSSpieler1_Schaetzung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)



# Wie sicher ist der Probant bezüglich seiner Schätzung
class SelbstEinschaetzungUmfrage(Page):

    form_model = 'player'
    form_fields = ['ConfidentNivau', 'AccuracyOfEstimates']

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == Constants.num_rounds)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        verdient = player.participant.VerdientePunkte * Constants.bezahlungProRichtigeSchaetzung + Constants.festerAnteilDerBezahlung
        player.payoff = verdient;
        player.participant.payoff = verdient;

# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    form_fields = ['GeburtsJahr', 'Gender', 'Education',
                   'Occupation', 'Household', 'PoliticalOrientation', 'OlderInPrivate', 'OlderInProfessional',
                   'era4', 'era9', 'era10', 'era11', 'era12']

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == Constants.num_rounds or not player.HatSichQualifiziert)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        verdient = player.participant.VerdientePunkte * Constants.bezahlungProRichtigeSchaetzung + Constants.festerAnteilDerBezahlung
        player.payoff = verdient;
        player.participant.payoff = verdient;


# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class Ergebnis(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == Constants.num_rounds or not player.HatSichQualifiziert)




#page_sequence = [Intro, Intro2, ResultsOfTWS, RealEffortTask, SeiteFuerT1, SeiteFuerT3, SeiteFuerT3, AuszahlungUmfrage, Ergebnis]
page_sequence = [Intro, Intro2, Quiz, RealEffortTask, Quiz2, BeforeEstimation, SeiteFuerT1, SeiteFuerT1genau, SeiteFuerT2j, SeiteFuerT2a, SeiteFuerT3j, SeiteFuerT3a, SelbstEinschaetzungUmfrage, AuszahlungUmfrage, Ergebnis]