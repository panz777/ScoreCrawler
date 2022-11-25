import requests
import json
import simplejson
import time

END_POINT = "https://new.scoresaber.com/api/"


def _url(path):
    return END_POINT + path


class ScoreSaberApi:
    session: requests.Session

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': 'UnityPlayer/2019.3.15f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
                'X-Unity-Version': '2019.3.15f1'
            }
        )

    def safe_get_json(self, url, trial=0):
        r = self.session.get(url)
        time.sleep(0.2)
        try:
            return r.json()
        except (json.decoder.JSONDecodeError, simplejson.errors.JSONDecodeError):
            print(f"Error: {r.text}, Trial: {trial}")
            if trial == -1:
                print("Request failed")
                raise Exception("Request failed")
            else:
                time.sleep(8)
                return self.safe_get_json(url, trial + 1)

    def get_player(self, player_id: int):
        r = self.safe_get_json(_url(f"player/{player_id}/full"))
        return r

    def get_players(self, offset: int):
        r = self.safe_get_json(_url(f"players/{offset}"))
        return r

    def get_scores(self, player_id, offset: int):
        r = self.safe_get_json(_url(f"player/{player_id}/scores/top/{offset}"))
        return r

    def get_replay(self, player_id, song_id):
        r = self.safe_get_json(f"https://ssdecode.azurewebsites.net/?playerID={player_id}&songID={song_id}")
        return r


if __name__ == '__main__':
    import progressbar

    a = ScoreSaberApi()
    print(a.get_players(1))
    print(a.get_player(76561198333869741))
    print(a.get_scores(76561198333869741, 1)["scores"])

