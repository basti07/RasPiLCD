import requests
from time import sleep
import urllib.parse
import json

class SpotifyApi:
    AUTH_CODE = None
    ACCESS_TOKEN = None
    REFRESHTOKEN = None
    JSON_DATA = None

    def __init__(self):
        self.JSON_DATA = self.load_json()

        self.AUTH_CODE = self.JSON_DATA["authorization_code"]
        self.ACCESS_TOKEN = self.JSON_DATA["access_token"]
        self.REFRESHTOKEN = self.JSON_DATA["refresh_token"]


#-------------------- Methods for Token Requests --------------------

    def refresh_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic ..."}
        data = {"grant_type":"refresh_token", "refresh_token":self.REFRESHTOKEN}

        r = self.send_request(url, headers, data)

        if r.status_code == 200:
            self.save_tokens(r)

        return r


    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic ..."}
        data = {"grant_type":"authorization_code", "code":self.AUTH_CODE, "redirect_uri":"http://127.0.0.1:3000"}

        r = self.send_request(url, headers, data)

        if r.status_code == 200:
            self.save_tokens(r)

        return r


#-------------------- Requests --------------------

    def get_track(self):
        url = "https://api.spotify.com/v1/me/player"
        headers = {"Authorization":"Bearer {}".format(self.ACCESS_TOKEN)}

        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            print("Errorcode {}".format(r.status_code))
            return r.status_code

        r = r.json()
        track = str(r["item"]["name"])
        artist = str(r["item"]["artists"][0]["name"])
        duration_ms = r["item"]["duration_ms"]
        progress_ms = r["progress_ms"]
        #print("{} - {}".format(track, artist))
        #print("{}/{}".format(self.to_min(progress_ms), self.to_min(duration_ms)))

        #duration = "{}/{}".format(self.to_min(progress_ms), self.to_min(duration_ms))

        return track, duration_ms, progress_ms


#-------------------- Helper Methods --------------------

    def send_request(self, url, header, data):
        return requests.post(url, headers=header, data=urllib.parse.urlencode(data))

    def save_tokens(self, request):
        request = request.json()

        self.ACCESS_TOKEN = request["access_token"]
        self.JSON_DATA["access_token"] = self.ACCESS_TOKEN

        if "refresh_token" in request:
            self.REFRESHTOKEN = request["request_token"]
            self.JSON_DATA["refresh_token"] = self.REFRESHTOKEN

        with open("tokens.json", "w") as f:
            json.dump(self.JSON_DATA, f)


    def load_json(self):
        with open("tokens.json", "r") as f:
            return json.load(f)


    def to_min(self, ms):
        time = ms/(1000*60)
        minutes = int(time)
        seconds = int((time - minutes) * 60)
        return "{}:{:02d}".format(minutes, seconds)

