from json import load
from retriever import Retriever
from networking import Receiver, Sender


settings_file = 'settings.json'

with open(settings_file,'r') as f:
    settings = load(f)

if __name__ == '__main__':
    receiver = Receiver()
    retriever = Retriever()

    retriever.start()
    receiver.start()