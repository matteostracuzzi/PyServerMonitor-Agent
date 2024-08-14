from json import load
from retriever import Retriever


settings_file = 'settings.json'

with open(settings_file,'r') as f:
    settings = load(f)
    