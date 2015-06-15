import os
import yaml

try:
    with open('ENV.yaml', 'r') as f:
        keys = yaml.load(f)
except IOError:
    keys = os.environ

client_id = keys['client_id']
server_token = keys['server_token']
secret = keys['secret']
secret_key = keys['secret_key']