from ScoreSaberApi import ScoreSaberApi
import progressbar
import pickle
import os
import re
import json
import gzip

a = ScoreSaberApi()
top_players = []

with open("top_players.pkl", "rb") as players_file:
    top_players = pickle.load(players_file)


def getReplayData(player_id, song_id):
    return a.get_replay(player_id, song_id)


def getSongOfPlayer(player_id: int):
    save_file_path = f"player/player_{player_id}.gz"
    if os.path.isfile(save_file_path):
        return
    player_scores = []

    bar = progressbar.ProgressBar().start()
    j = 1
    while j <= 100:
        scores_json = a.get_scores(player_id, j)
        scores_list = []
        if "scores" in scores_json:
            new_scores = scores_json["scores"]
        else:
            new_scores = []
        if len(new_scores) <= 0:
            break
        player_scores += new_scores
        for elem in new_scores:
            song_id = elem["leaderboardId"]
            res = getReplayData(player_id, song_id)
            if "errorMessage" in res:
                continue
            with gzip.GzipFile("replay/" + str(player_id) + "_" + str(song_id) + ".gz", "wb") as players_song_file:
                j_s = str(res)
                j_b = bytes(j_s, 'utf-8')
                players_song_file.write(j_b)
                print(str(song_id) + "done")
        bar.update(j)
        j += 1

    with gzip.GzipFile(save_file_path, "w") as players_score_file:
        j_s = str(player_scores)
        j_b = bytes(j_s, 'utf-8')
        players_score_file.write(j_b)

    return


counter = 0
for player in top_players:
    getSongOfPlayer(int(player['playerId']))
    if counter % 100 == 0:
        print(counter)
    counter += 1

