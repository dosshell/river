import os
import json

config = []
if os.path.isfile('settings.json'):
    with open('settings.json') as f:
        config = json.load(f)
elif os.path.isfile('/run/secrets/river_settings'):
    with open('/run/secrets/river_settings') as f:
        config = json.load(f)
else:
    with open('settings_template.json') as f:
        config = json.load(f)
