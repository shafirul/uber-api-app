import os
import yaml

try:
    with open('ENV.yaml', 'r') as f:
        keys = yaml.load(f)
except IOError:
    keys = os.environ

CLIENT_ID = keys['CLIENT_ID']
SERVER_TOKEN = keys['SERVER_TOKEN']
SECRET = keys['SECRET']
SECRET_KEY = keys['SECRET_KEY']