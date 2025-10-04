from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
#SESSION_CONFIGS = [dict(name='AgeFactor', num_demo_participants=None, app_sequence=['TeamWorkStage'])]
#SESSION_CONFIGS = [dict(name='AgeFactor', num_demo_participants=None, app_sequence=['DeciderStage'])]
SESSION_CONFIGS = [dict(name='AgeFactor', num_demo_participants=None, app_sequence=['DeciderStageHiring'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False
#real_world_currency_per_point = - hier UMRECHNEN!!!
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['richtigeAntworten', 'AuszahlungUserName', 'VerdientePunkte', 'AnzahlRichtigerAntworten', 'ProlificID', 'zugeordneteRole', 'gewaehlteSequenz', 'VerdientePunkteImTestSpiel', 'HatMoreDetailsAngeschaut', 'zeitRunde1', 'zeitRunde2', 'zeitRunde3', 'zeitRunde4', 'zeitRunde5', 'zeitRunde6', 'zeitRunde7', 'zeitRunde8', 'zeitRunde9', 'zeitRunde10', 'StudienNumber', 'HatAbgebrochen', 'BestaetigungQ1', 'BestaetigungQ2']
SESSION_FIELDS = ['ZeitVergangen', 'Spielarten_Folge', 'AuszahlungInPunktenFuerDasOpfer', 'ergebnisseVonTWS', 'aktuellAngezeigteErgebnisse']
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'admin'

SECRET_KEY = 'blahblah25'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


