import os
import json


file = ''
is_template = False

if os.path.isfile('settings.json'):
    file = 'settings.json'
elif os.path.isfile('/run/secrets/river_settings'):
    file = '/run/secrets/river_settings'
else:
    file = 'settings_template.json'
    is_template = True

config = []
with open(file) as f:
    config = json.load(f)
