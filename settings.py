from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='AgeFactor', num_demo_participants=None, app_sequence=['TeamWorkStage'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
#real_world_currency_per_point = - hier UMRECHNEN!!!
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['richtigeAntworten', 'AuszahlungUserName', 'VerdientePunkte', 'AnzahlRichtigerAntworten', 'ProlificID']
SESSION_FIELDS = ['ZeitVergangen', 'Spielarten_Folge', 'AuszahlungInPunktenFuerDasOpfer', 'AuszahlungImTeamFolge', 'BeraterEmpfehlungFolge', 'EntscheiderAuszahlungPunkte', 'BeraterAuszahlungPunkte', 'OpferAuszahlungPunkte', 'BeraterKlickfolge']
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'admin'

SECRET_KEY = 'blahblah25'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


