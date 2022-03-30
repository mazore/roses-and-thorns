import json
import numpy as np
import os
import pandas as pd
import requests

"""
def save_game_data(bracket):
    data = dict(mens={}, womens={})
    for i, game in enumerate(bracket.games):
        data['mens'][i] = {
            'winner': None,
            'team1': game.mens1,
            'team2': game.mens2,
        }
        data['womens'][i] = {
            'winner': None,
            'team1': game.womens1,
            'team2': game.womens2,
        }
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_live_data():
    url = 'https://sdataprod.ncaa.com/?operationName=scores_current_web&variables=%7B%22seasonYear%22%3A2021%2C%22current%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%223e1de1bf338658aeac88c93e5cfdc3ddaaaac2d1a91c14e9c300174a46a9d91b%22%7D%7D'
    headers = {
        'authority': 'sdataprod.ncaa.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'content-type': 'application/json',
        'sec-gpc': '1',
        'origin': 'https://www.ncaa.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.ncaa.com/',
        'accept-language': 'en-US,en;q=0.9',
    }
    resp = requests.get(url, headers=headers)
    for game in resp.json()['data']['mmlContests']:
        if game['gameState'] != 'F':
            continue
        for team in game['teams']:
            name = team['nameShort']
            points = team['score']
            print(name, points)
        print()
"""

THORNS = {  # 22 thorns
    'Arizona': 5,
    'Iowa': 7,
    'Texas': 8,
    'LSU': 9,
    'Villanova': 13,
    'Ohio State': 13,
    'Arkansas': 14,
    'Indiana': 15,
    'Miami (FL)': 18,
    'Deleware': 28,
    'Longwood': 30,
    'Baylor': 3,
    'Tennessee': 7,
    'UConn': 7,
    'Kansas': 9,
    'Gonzaga': 10,
    'North Carolina': 13,
    'Michigan': 14,
    'Iowa State': 14,
    'Virginia Tech': 16,
    'Creighton': 19,
    'Montana State': 30,
}


class Game:
    def __init__(self, bracket, m1, m2, w1, w2):
        self.bracket = bracket
        self.mens1 =   self.not_nan(*m1)
        self.mens2 =   self.not_nan(*m2)
        self.womens1 = self.not_nan(*w1)
        self.womens2 = self.not_nan(*w2)

    def not_nan(self, x, y):
        if self.bracket.df[x].isnull()[y]:
            print(f'NaN value at ({x}, {y}) for bracket: {self.bracket.filename}')
            return None
        return self.bracket.df.values[y][x]

class DefaultGame(Game):
    def __init__(self, bracket, x, y):
        m1 = (x, y)
        m2 = (x, y + 1)
        w1 = (x + 1, y)
        w2 = (x + 1, y + 1)
        super().__init__(bracket, m1, m2, w1, w2)


class Bracket:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_excel(filename, header=None)
        self.games = []
        for x in [1, 24]:
            for y in range(1, 30, 4):
                self.games.append(DefaultGame(self, x, y))
            for y in range(34, 63, 4):
                self.games.append(DefaultGame(self, x, y))
        for x in [3, 22]:
            for y in [3, 11, 19, 27, 36, 44, 52, 60]:
                self.games.append(DefaultGame(self, x, y))
        for x in [4, 21]:
            for y in [7, 23, 40, 56]:
                self.games.append(DefaultGame(self, x, y))
        for x in [6, 19]:
            for y in [15, 48]:
                self.games.append(DefaultGame(self, x, y))
        self.games.append(Game(self, (7, 23), (7, 24), (18, 23), (18, 24)))
        self.games.append(Game(self, (7, 40), (7, 41), (18, 40), (18, 41)))
        self.games.append(Game(self, (8, 27), (8, 35), (17, 27), (17, 35)))

    def get_points(self, answers):
        correct = 0
        for game, game_correct in zip(self.games, answers.games):
            for name in ['mens1', 'mens2', 'womens1', 'womens2']:
                if getattr(game, name) == getattr(game_correct, name):
                    correct += 1
        return correct


if __name__ == '__main__':
    answers = Bracket('Answers.xlsx')
    for filename in os.listdir('brackets'):
        points = Bracket('brackets/' + filename).get_points(answers)
        print(filename, points)
