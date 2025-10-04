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
    name_in_url = 'DeciderStageHiring'

    #players_per_group = 24

    # Es gibt 4 Gruppen:
    #   1 - ohne Nennung Jung/Alt und mit einem Histogramm
    #   2 - ohne Nennung Jung/Alt und mit einem Histogramm UND einer konkreteren Info zur Altersverteilung
    #   3 - mit Nennung Jung/Alt und mit einem Histogramm
    #   4 - mit Nennung Jung/Alt und mit ZWEI Histogrammen

    # Die Anzahl der Teilnehmer muss in allen 4 Gruppen gleich sein
    #maximaleAnzahlProGruppe = players_per_group / 4

    # ... soll aber jetzt dynamisch sein. Es müssen aber Vierfache sein, damit man auf Sequenzen aufteilen kann
    maximaleAnzahlProGruppeT1 = 0
    maximaleAnzahlProGruppeT2 = 29
    maximaleAnzahlProGruppeT3 = 0
    maximaleAnzahlProGruppeT4 = 0

    # Abweichend von der vorherigen Logik, ist players_per_group die Summe von maximaleAnzahlProGruppe und nicht
    # umgekehrt, dass maximaleAnzahlProGruppe anteilig players_per_group aufteilen.
    players_per_group = maximaleAnzahlProGruppeT1 + maximaleAnzahlProGruppeT2 + maximaleAnzahlProGruppeT3 + maximaleAnzahlProGruppeT4


    # Es gibt 4 vorgegebene Sequenzen aus dem TeamWork Stage.
    # Pro Gruppe müssen die Sequenzen gleichverteilt sein

    #maximalAnzahlSequenzProGruppe = players_per_group / 16
    maximalAnzahlSequenzProGruppeT1 =  maximaleAnzahlProGruppeT1 / 4
    maximalAnzahlSequenzProGruppeT2 =  maximaleAnzahlProGruppeT2 / 4
    maximalAnzahlSequenzProGruppeT3 =  maximaleAnzahlProGruppeT3 / 4
    maximalAnzahlSequenzProGruppeT4 =  maximaleAnzahlProGruppeT4 / 4


    # Auch hier

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

    # Werte für Young und Alt
    young = 'younger'
    old = 'older'


    ########## ECHT ######### Echte Auszahlungen für Probalnden ### ECHT #######
    # Quiz-Versager
    auszahlungAnQuizVersager = 0.40
    # GBP sockel
    festerAnteilDerBezahlung = 1.15
    # Punkte umrechnung X Punkte = 0.01 GBP
    punkteUmrechnungInPenny = 2

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

    #Schafft der Proband die Quize nicht, wird er anders bezahlt, daher eine andere Prolific-StuidenNummer
    FULL_STUDIENNUMMER = 'CC1LPFS5'
    FAILED_STUDIENNUMMER = 'CI5IF1F2'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # Zähle Spieler, die schon der Gruppen/Rollen zugeordnet wurden.
    anzahlSpielerInDerGruppe1 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppeT1)
    anzahlSpielerInDerGruppe2 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppeT2)
    anzahlSpielerInDerGruppe3 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppeT3)
    anzahlSpielerInDerGruppe4 = models.IntegerField(initial=Constants.maximaleAnzahlProGruppeT4)


    # Da man Arrays zurzeit offenbar nur als json-Dump in einem LongStringField speichern kann,
    # werden jetzt int-Variablen für die Begrenzung pro Gruppe und Sequenz eingeführt
    gruppe1_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT1)
    gruppe1_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT1)
    gruppe1_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT1)
    gruppe1_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT1)

    #gruppe2_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT2)
    #gruppe2_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT2)
    #gruppe2_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT2)
    #gruppe2_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT2)
    gruppe2_sequenz1 = models.IntegerField(initial=7)
    gruppe2_sequenz2 = models.IntegerField(initial=6)
    gruppe2_sequenz3 = models.IntegerField(initial=9)
    gruppe2_sequenz4 = models.IntegerField(initial=7)

    gruppe3_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT3)
    gruppe3_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT3)
    gruppe3_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT3)
    gruppe3_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT3)



    gruppe4_sequenz1 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT4)
    gruppe4_sequenz2 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT4)
    gruppe4_sequenz3 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT4)
    gruppe4_sequenz4 = models.IntegerField(initial=Constants.maximalAnzahlSequenzProGruppeT4)



class Player(BasePlayer):

    warAufIntro = models.IntegerField(initial=-1)

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
    realEffort = models.IntegerField(label='')

    # Wir müssen bei den Gruppen 3 und 4 die Anzeige so variieren, dass mal der junge und mal alte Worker zuerst
    # angezeigt werden. Es soll also bei der Hälfte der Runden der ALTE Worker (erster Wert im Tuppel, also Index 0) und
    # mal der JUNGE Worker (zweiter Wert im Tuppel, also Index 1) zuerst angezeigt werden.

    jungOderAlt1 = models.IntegerField(initial=-1)
    jungOderAlt2 = models.IntegerField(initial=-1)
    jungOderAlt3 = models.IntegerField(initial=-1)
    jungOderAlt4 = models.IntegerField(initial=-1)
    jungOderAlt5 = models.IntegerField(initial=-1)
    jungOderAlt6 = models.IntegerField(initial=-1)
    jungOderAlt7 = models.IntegerField(initial=-1)
    jungOderAlt8 = models.IntegerField(initial=-1)
    jungOderAlt9 = models.IntegerField(initial=-1)
    jungOderAlt10 = models.IntegerField(initial=-1)

    # Wird auf der Web-Seite in den Rollen 3 und 4 links der alte oder der Junge angezeigt
    anzeigeLinks = models.StringField();
    anzeigeRechts = models.StringField();

    # Nach der letzten der 10 Entscheidungen gibt es zwei Fragen auf der Bestätigung-Seite
    BestaetigungQ1 = models.StringField(choices=[['1', 'Not at all important'],
                                                 ['2', 'Slightly important'],
                                                 ['3', 'Moderately important'],
                                                 ['4', 'Very important'],
                                                 ['5', 'Extremely important']], 
                                                 widget=widgets.RadioSelectHorizontal, label='<b>Question 1</b>: How important was it for you to hire this person rather than the other?')
    BestaetigungQ2 = models.StringField(choices=[['1', 'Not at all confident'],
                                                 ['2', 'Slightly confident'],
                                                 ['3', 'Moderately confident'],
                                                 ['4', 'Very confident'],
                                                 ['5', 'Extremely confident']], 
                                                 widget=widgets.RadioSelectHorizontal, label='<b>Question 2</b>: How confident are you that you chose the right candidate?')


    # Wir müssen speichern, welchen Worker der Entscheider einstellen will. 
    # Bei T1 und T2 sind es "one worker" und "the other worker"
    # Bei T3 und T4 sind es "older or the younger worker" 
    Entscheidung = models.StringField(choices=['One', 'Other', Constants.old, Constants.young], label="", blank=True)


# Und Eingaben der Entscheider, was sie denken, dass einer beigetragen hat
    Spieler1_Schaetzung = models.IntegerField(label='', blank=True, null=True)
    Spieler2_Aut_Berechnet = models.StringField(label='', blank=True, null=True, initial="")

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



    # Eine der beiden Buttons wurde gerückt. In T1 und T2 wird jetzt dem Spieler 
    # zufällig die Punktezahl eines der beiden Workers zugewiesen.
def berechneAuszahlungT12(ergebnisSpieler1, ergebnisSpieler2):
    result = 0
    welcherWorker = random.randint(1, 2)
    if welcherWorker == 1:
        result = ergebnisSpieler1
    elif welcherWorker == 2:
        result = ergebnisSpieler2
    else:
        print('FEHLER: berechneAuszahlungT12, welcherWorker nicht 1 oder 2 sondern: ', welcherWorker)
    print('berechneAuszahlungT12: ', ergebnisSpieler1, 'S2: ', ergebnisSpieler2, ' result: ', result)
    return result

    # Eine der beiden Buttons wurde gerückt. In T3 und T4 wird jetzt dem Spieler 
    # das Ergebnis des passenden Workers (old oder young) zugewiesen.
def berechneAuszahlungT34(ergebnisOld, ergebnisYoung, entscheidung):
    result = 0
    if entscheidung is None:
        print('berechneAuszahlungT34: entscheidung ist NULL!!')
    elif entscheidung == Constants.old:
        result = ergebnisOld
    elif entscheidung == Constants.young:
        result = ergebnisYoung
    else:
        print('FEHLER: berechneAuszahlungT32, Entscheidung nicht "Old" oder "Young" sondern: ', entscheidung)
    print('berechneAuszahlungT34: ergebnisYoung', ergebnisYoung, ' ergebnisOld: ', ergebnisOld, ' entscheidung: ', entscheidung, ' result: ', result)
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
    else:
        print('FEHLER: gibSequenzFuerDieRolle, RollenNummer nicht zwischen 1 und 6 sondern: ', rollenNummer)

    return result

# Ist die Anzahl der Probanden pro Sequenz und Rolle schon ausgeschöpft?
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
    else:
        print("FEHLER: reduziereMengeProSequenzUndRolle / rollenNummer: ", rollenNummer)

# Wir wollen prüfen, wie lange der Spieler auf der SEite war. Die Zeit wird pro Runde gesichert.
# Da die oTree-Modelle keine Arrays direkt unterstützen und die Funktionalität zu oft benutzt ist (so dass
# json-Dump nicht performant ist) wird diese Funktion genutzt
def speichereZeitAufDerSeite(player, dauerAufDerSeite):
    roundNummer = player.round_number
    setattr(player.participant, f'zeitRunde{roundNummer}', dauerAufDerSeite)

#    if roundNummer == 1:
#        player.participant.zeitRunde1 = dauerAufDerSeite
#    elif roundNummer == 2:
#        player.participant.zeitRunde2 = dauerAufDerSeite
#    elif roundNummer == 3:
#        player.participant.zeitRunde3 = dauerAufDerSeite
#    elif roundNummer == 4:
#        player.participant.zeitRunde4 = dauerAufDerSeite
#    elif roundNummer == 5:
#        player.participant.zeitRunde5 = dauerAufDerSeite
#    elif roundNummer == 6:
#        player.participant.zeitRunde6 = dauerAufDerSeite
#    elif roundNummer == 7:
#        player.participant.zeitRunde7 = dauerAufDerSeite
#    elif roundNummer == 8:
#        player.participant.zeitRunde8 = dauerAufDerSeite
#    elif roundNummer == 9:
#        player.participant.zeitRunde9 = dauerAufDerSeite
#    elif roundNummer == 10:
#        player.participant.zeitRunde10 = dauerAufDerSeite
#    else:
#        print("FEHLER: speichereZeitAufDerSeite / roundNummer: ", roundNummer)


class Intro(Page):
    form_model = 'player'
    form_fields = ["ProlificID"]

    # einmal warnen wir, dass ProlificID ggf. nicht korrekt ist
    einmaligeWartung = True

    @staticmethod
    def is_displayed(player: Player):
        # Nur um zu sehen, dass der Teilnehmer auf der 1. Seite war - also es kein technisches Problem bei Heroku gab
        player.warAufIntro = 999
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
        # Wir bleiben solange in einer Schleife, bis der Probant einer Rolle zugeordnet ist
        # War für eine Rolle schon genug Teilnehmer zugeordnet, wird neue Zufallszahl generiert

        # Rolle wird später bei der Sequenz noch einmal gebraucht
        rolle = -1
        weiterRolleSuchen = True
        while weiterRolleSuchen:
            zufallszahl = random.randint(1, 4)

            #print("Intro: zufallszahl: ", zufallszahl)

            # KEINE Kompakte Darstellung, weil zuerst die Logik war, dass die Probanten NICHT gleichmässig verteilt
            # werden, sondern für die Rolle 1 z.B. doppelt so oft. Daher lieber eine stabile IF-ELSEIF :-)
            if (zufallszahl == 1):
                # die Rolle wäre 1, es sei denn, es gibt keine "freie" Sequenz mehr für die Gruppe 1
                sequenzNummer = gibSequenzFuerDieRolle(player, 1)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 1
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 1
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 2:
                sequenzNummer = gibSequenzFuerDieRolle(player, 2)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 2
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 2
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 3:
                sequenzNummer = gibSequenzFuerDieRolle(player, 3)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 3
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 3
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            elif zufallszahl == 4:
                sequenzNummer = gibSequenzFuerDieRolle(player, 4)
                if sequenzNummer > 0:
                    player.zugeordneteRole = 4
                    player.gewaehlteSequenz = sequenzNummer
                    player.participant.zugeordneteRole = 4
                    player.participant.gewaehlteSequenz = sequenzNummer
                    weiterRolleSuchen = False
            else:
                print("FEHLER: weiterRolleSuchen / zufallszahl: ", zufallszahl)

        # Jetzt setzen wir, in welchen Runden Junge und in welcher Runde der alte zuerst angezeigt werden.
        # Generiere 5 verschiedene Integer zwischen 1 und 10
        random_integers = random.sample(range(1, 11), 5)

        # Zuweisung, also so etwas, wie
        #         if 1 in random_integers:
        #             player.jungOderAlt1 = 0
        #         else:
        #             player.jungOderAlt1 = 1
        # nur kompakt

        for i in range(1, 11):
            if i in random_integers:
                setattr(player, f'jungOderAlt{i}', 0)  # alter Spieler
            else:
                setattr(player, f'jungOderAlt{i}', 1)  # junger Spieler zuerst

        # Ausgabe der Ergebnisse
        #print("Gezogene Zahlen: ", random_integers)
        #for i in range(1, 11):
        #    print(f"player.jungOderAlt{i}: {getattr(player, f'jungOderAlt{i}')}")


        #print("Rolle: ", player.zugeordneteRole, " Sequenz #: ",player.gewaehlteSequenz)
        #print("Neue freie Rollen: [", gruppe.anzahlSpielerInDerGruppe1, ", " , gruppe.anzahlSpielerInDerGruppe2, ", " ,gruppe.anzahlSpielerInDerGruppe3, ", " ,gruppe.anzahlSpielerInDerGruppe4, "]")
        #print("Sequenzen: [[", gruppe.gruppe1_sequenz1, ", " , gruppe.gruppe1_sequenz2, ", " ,gruppe.gruppe1_sequenz3, ", " ,gruppe.gruppe1_sequenz4, "], [" ,
        #                       gruppe.gruppe2_sequenz1, ", " , gruppe.gruppe2_sequenz2, ", " ,gruppe.gruppe2_sequenz3, ", " ,gruppe.gruppe2_sequenz4, "], [" ,
        #                       gruppe.gruppe3_sequenz1, ", " , gruppe.gruppe3_sequenz2, ", " ,gruppe.gruppe3_sequenz3, ", " ,gruppe.gruppe3_sequenz4, "], [" ,
        #                       gruppe.gruppe4_sequenz1, ", " , gruppe.gruppe4_sequenz2, ", " ,gruppe.gruppe4_sequenz3, ", " ,gruppe.gruppe4_sequenz4, "]]")

        #TODO HIER NUR UM ALLES IN T2 zu testen - DANACH LÖSCHEN!!!!
        player.zugeordneteRole = 3;
        player.participant.zugeordneteRole = 3;


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

    @staticmethod
    def vars_for_template(player: Player):
        # Constants.punkteUmrechnungInPenny = 0,01GBP, 
        wertVon37Punkten = 0.37/Constants.punkteUmrechnungInPenny
        wertVon37PunktenFormatiert=f"{wertVon37Punkten:.3f}"

        return {
            'wertVon37Punkten': wertVon37PunktenFormatiert
        }



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

        quizKorrekt = ((values['QuizKodieren2'] == 'c'))
        if not quizKorrekt:
            #print('NICHT KORREKT player.FreiVersucheImQuiz war: ', player.FreiVersucheImQuiz, " / quizKorrekt: ", quizKorrekt)
            player.FreiVersucheImQuiz -= 1
            if player.FreiVersucheImQuiz > 0 :
                #print('Try again please. One or both answers are not yet correct. You have ', str(player.FreiVersucheImQuiz), ' attempts left.')
                return 'Try again please. One or more answers are not yet correct. You have ' + str(player.FreiVersucheImQuiz) + ' attempts left.'
            else:
                #keine Freiversuche mehr
                #print('ELSE!!')
                player.participant.StudienNumber = Constants.FAILED_STUDIENNUMMER
                player.HatSichQualifiziert = False
        else:
            #print('KORREKT!!')
            player.participant.StudienNumber = Constants.FULL_STUDIENNUMMER
            pass



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
            auszahlung = Constants.festerAnteilDerBezahlung + data * Constants.bezahlungProRichtigeSchaetzung
        else:
            player.participant.AnzahlRichtigerAntworten = 0
            player.AnzahlRichtigerAntworten = 0
            auszahlung = Constants.festerAnteilDerBezahlung

        # Verdiente Punkt ist ein Integer, nicht float
        player.VerdientePunkteImTestSpiel = int(auszahlung)
        player.participant.VerdientePunkteImTestSpiel = int(auszahlung)



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
                player.participant.StudienNumber = Constants.FAILED_STUDIENNUMMER
                player.HatSichQualifiziert = False
        else:
            #print('KORREKT!!')
            player.participant.StudienNumber = Constants.FULL_STUDIENNUMMER
            pass




# Nur für die Rolle T1
class SeiteFuerT1(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["Spieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 1 and player.HatSichQualifiziert)

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
        inputFieldValue = player.field_maybe_none('Spieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('Spieler2_Aut_Berechnet')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
        # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'Spieler1_Schaetzung': inputFieldValue,
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
        neuePunkteInDieserRunde = berechneAuszahlungT12(player.oldWorker, player.youngWorker)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)



# Rolle 2 - ohne Nennung Jung/Alt und mit einem Histogramm UND einer konkreteren Info zur Altersverteilung
class SeiteFuerT2(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["Spieler1_Schaetzung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 2 and player.HatSichQualifiziert)

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
        inputFieldValue = player.field_maybe_none('Spieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('Spieler2_Aut_Berechnet')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'Spieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        # Punkte für die Enscheidung
        neuePunkteInDieserRunde = berechneAuszahlungT12(player.oldWorker, player.youngWorker)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        #print("Punkte neu: ",player.participant.VerdientePunkte)

# Rolle 3 - mit Nennung Jung/Alt und mit einem Histogramm
class SeiteFuerT3(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["Entscheidung"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        return (player.participant.zugeordneteRole == 3  and player.HatSichQualifiziert)

    @staticmethod
    def vars_for_template(player: Player):
        # Zuerst die Sequenz holen - (-1) weil Array ja mit 0 starte
        aktuelleSequenz = Constants.sequenzen[player.participant.gewaehlteSequenz-1]
        # Und jetzt das i-te Element
        arbeitsergebnisse = aktuelleSequenz[player.round_number - 1]
        print("arbeitsergebnisse:", arbeitsergebnisse)
        # Die Werte braucht man unten zur Berechung der Auszahlung. Die Summe aber auch als Anzeige, daher schon hier
        player.oldWorker = int(arbeitsergebnisse[0])
        player.youngWorker = int(arbeitsergebnisse[1])
        player.gemeinsamesErgebnisBeiderWorker = player.oldWorker + player.youngWorker

        # ist es ein Junger oder Alter Workler? 0 - alt, 1 - jung
        # Man muss die ERSTE Runde lesen, danach werden die Felder neu Initialisiert
        postitionAnzeige = getattr(player.in_round(1), f'jungOderAlt{player.round_number}')
        #print("Runde: ", player.round_number, "postitionAnzeige: ", postitionAnzeige)

        if postitionAnzeige == 0:
            player.anzeigeLinks = Constants.old # alter links
            player.anzeigeRechts = Constants.young
        else:
            player.anzeigeLinks = Constants.young # junger links
            player.anzeigeRechts = Constants.old



        #print(arbeitsergebnisse)
        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker, ' real eff: ', player.realEffort);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('Spieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('Spieler2_Aut_Berechnet')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'Spieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)

        # Hier weiß ich, ob Alt oder Jung ausgewählt wurde. 
        # Und zwar unabhängig davon, ob das Button rechts oder links stand. 
        neuePunkteInDieserRunde = berechneAuszahlungT34(player.oldWorker, player.youngWorker, player.Entscheidung)
        player.participant.VerdientePunkte += neuePunkteInDieserRunde
        print("Punkte neu: ",player.participant.VerdientePunkte)



# Rolle 3 - Folgeseite mit der Frage, wie wichtig die Wahl war.  
class SeiteFuerT3Bestaetigung(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["BestaetigungQ1", "BestaetigungQ2"]

    @staticmethod
    def is_displayed(player: Player):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Start-Zeit"
        # Wir wollen auch Teile der Sekunden, daher time.perf_counter() und nicht time.time().
        player.eintrittZeitAufDerSeite = time.perf_counter()
        #print("SeiteFuerT3Bestaetigung: ",(player.participant.zugeordneteRole == 3  and player.HatSichQualifiziert))
        return (player.participant.zugeordneteRole == 3  and player.HatSichQualifiziert and (player.round_number == Constants.num_rounds))

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

        # ist es ein Junger oder Alter Workler? 0 - alt, 1 - jung
        # Man muss die ERSTE Runde lesen, danach werden die Felder neu Initialisiert
        postitionAnzeige = getattr(player.in_round(1), f'jungOderAlt{player.round_number}')
        #print("Runde: ", player.round_number, "postitionAnzeige: ", postitionAnzeige)

        if postitionAnzeige == 0:
            player.anzeigeLinks = Constants.old # alter links
            player.anzeigeRechts = Constants.young
        else:
            player.anzeigeLinks = Constants.young # junger links
            player.anzeigeRechts = Constants.old



        #print(arbeitsergebnisse)
        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker, ' real eff: ', player.realEffort);

        summe = player.gemeinsamesErgebnisBeiderWorker
    
        return {
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)
        player.participant.BestaetigungQ1 = player.BestaetigungQ1
        player.participant.BestaetigungQ2 = player.BestaetigungQ2
        print("BestaetigungQ1: ", player.BestaetigungQ1, " BestaetigungQ2: ", player.BestaetigungQ2)



# Rolle 4 - mit Nennung Jung/Alt und mit ZWEI Histogrammen
class SeiteFuerT4(Page):
    #timeout_seconds = Constants.dauerDesThreatmentsInSekunden
    form_model = 'player'
    form_fields = ["Entscheidung"]

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

        # ist es ein Junger oder Alter Workler? 0 - alt, 1 - jung
        # Man muss die ERSTE Runde lesen, danach werden die Felder neu Initialisiert
        postitionAnzeige = getattr(player.in_round(1), f'jungOderAlt{player.round_number}')
        #print("Runde: ", player.round_number, "postitionAnzeige: ", postitionAnzeige)

        if postitionAnzeige == 0:
            player.anzeigeLinks = Constants.old
            player.anzeigeRechts = Constants.young
            player.realEffort = player.oldWorker # alter links
        else:
            player.anzeigeLinks = Constants.young
            player.anzeigeRechts = Constants.old
            player.realEffort = player.youngWorker # junger links


        #print(arbeitsergebnisse)
        #print('old worker: ', player.oldWorker, ' young worker: ', player.youngWorker, ' real eff: ', player.realEffort);

        summe = player.gemeinsamesErgebnisBeiderWorker
        inputFieldValue = player.field_maybe_none('Spieler1_Schaetzung')
        berechnetesErgebnis = player.field_maybe_none('Spieler2_Aut_Berechnet')
        if inputFieldValue is None:
            # Behandle den Fall, wenn das inputFieldValue None ist
            inputFieldValue = ""

        if berechnetesErgebnis is None:
            # Behandle den Fall, wenn das Ergebnis None ist
            berechnetesErgebnis = ""

        return {
            'calculated_field': berechnetesErgebnis,
            'Spieler1_Schaetzung': inputFieldValue,
            'summe': summe
        }

    # Berechne die Auszahlung für diese Runde und addiere sie zur Gesamtauszahlung
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wir wollen messen, wie lange der Spieler auf der Seite war. Hier ist die "Verlass-Zeit"
        dauerAufDerSeite = time.perf_counter() - player.eintrittZeitAufDerSeite
        # Rundenzeiten des Spielers werden in Participant gespeichert.
        speichereZeitAufDerSeite(player, dauerAufDerSeite)

        # Hier weiß ich, ob Alt oder Jung ausgewählt wurde. 
        # Und zwar unabhängig davon, ob das Button rechts oder links stand. 
        neuePunkteInDieserRunde = berechneAuszahlungT34(player.oldWorker, player.youngWorker, player.Entscheidung)
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
        #verdient = player.participant.VerdientePunkte * Constants.bezahlungProRichtigeSchaetzung + Constants.festerAnteilDerBezahlung
        #player.payoff = verdient;
        #player.participant.payoff = verdient;
        pass

# Auszahlung und Statistik werden vorbereitet
class AuszahlungUmfrage(Page):

    form_model = 'player'
    form_fields = ['GeburtsJahr', 'Gender', 'Education',
                   'Occupation', 'Household', 'PoliticalOrientation', 'OlderInPrivate', 'OlderInProfessional',
                   'era4', 'era9', 'era10', 'era11', 'era12']

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == Constants.num_rounds)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        verdient = player.participant.VerdientePunkte * Constants.bezahlungProRichtigeSchaetzung + Constants.festerAnteilDerBezahlung
        if (not player.HatSichQualifiziert):
            verdient = Constants.auszahlungAnQuizVersager
        player.payoff = verdient;
        player.participant.payoff = verdient;


# Ergebnis des Entscheidungsvorlage-Games wird angezeigt
# Auszahlungsinformationen
class Ergebnis(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == Constants.num_rounds)

# Ergebnis für Spieler, die die Quize NICHT korrekt beantwortet haben
class ErgebnisOhneQuiz(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (not player.HatSichQualifiziert)


page_sequence = [Intro, Intro2, Quiz, RealEffortTask, Quiz2, BeforeEstimation, SeiteFuerT1, SeiteFuerT2, SeiteFuerT3, SeiteFuerT4, SeiteFuerT3Bestaetigung, SelbstEinschaetzungUmfrage, AuszahlungUmfrage, Ergebnis, ErgebnisOhneQuiz]