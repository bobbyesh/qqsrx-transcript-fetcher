import pickle
import yagmail
from transcript_fetcher import *


class Messenger:

    filename = 'previous_episodes.pickle'
    username = 'bobbyeshleman'
    recipient = 'bobbyeshleman@gmail.com'
    yag = yagmail.SMTP(username)

    def __init__(self):
        try:
            with open(self.filename, 'rb') as f:
                self.previous_episodes = pickle.load(f)
        except OSError as error:
            print("couldn't read file: ", error)
            self.previous_episodes = []

    def send_string(self, ep_title, ep_transcript):
        if self.episode_is_new(ep_title):
            print('sending ', ep_title)
            self.yag.send(self.recipient, ep_title, ep_transcript)
            self.add_episode_to_previous(ep_title)
            self.log_episode()
        else:
            print('not sending: episode previously sent')

    def episode_is_new(self, episode_title):
        return episode_title not in self.previous_episodes

    def add_episode_to_previous(self, episode_title):
        self.previous_episodes.append(episode_title)

    def log_episode(self):
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.previous_episodes, f)
        except OSError as error:
                print('failed at wb', error)


if __name__ == '__main__':
    fetcher = TranscriptFetcher()
    messenger = Messenger()
    transcripts = fetcher.get_transcripts()
    for episode in transcripts:
        messenger.send_string(episode.title, episode.transcript)
