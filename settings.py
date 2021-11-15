from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='BadCounsel', num_demo_participants=None, app_sequence=['InterestedCounsel'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'DKK'
USE_POINTS = True
#real_world_currency_per_point = - hier UMRECHNEN!!!
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['zugeordneteRole', 'AuszahlungUserName']
SESSION_FIELDS = ['AngebotsMatrix', 'Spielarten_Folge', 'AuszahlungInPunktenFuerDasOpfer', 'AuszahlungImTeamFolge', 'BeraterEmpfehlungFolge', 'EntscheiderAuszahlungPunkte', 'BeraterAuszahlungPunkte', 'OpferAuszahlungPunkte']
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah25'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


