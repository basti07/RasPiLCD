import LCD
import spotify_api
from time import sleep
from threading import Thread, Event

class Display:
    TRACK = None

    def __init__(self):
        data_pins = list(range(5,13))
        self.lcd = LCD.LCD(rs_pin=21, e_pin=16, data_pins=data_pins)
        self.api = spotify_api.SpotifyApi()

        self.api.refresh_token()
        self.TRACK = self.api.get_track()

    def print_track(self):
        self.lcd.set_ddram(0x00)
        self.lcd.write_string(self.TRACK[0])

    # def print_duration(self):
        # self.lcd.set_ddram(0x40)
        # self.lcd.write_string(self.TRACK[1])

    def print_duration(self):
        self.lcd.set_ddram(0x40)
        self.lcd.data(62)
        self.lcd.set_ddram(0x4F)
        self.lcd.data(60)

        prog = int((self.TRACK[2] / self.TRACK[1]) * 14)
        self.lcd.set_ddram(0x41)
        for i in range(1, prog+1):
            self.lcd.data(255)

    def scroll(self, new_track_evt):
        while True:
            for i in range(len(self.TRACK[0])):
                self.lcd.set_ddram(0x00)
                self.lcd.write_string(self.TRACK[0][i:] + i * " ")
                self.print_duration()
                if new_track_evt.is_set():
                    for i in range(0x40, 0x4F):
                        self.lcd.set_ddram(i)
                        self.lcd.data(0x20)
                    return
                sleep(0.5)

    def update(self):
        while True:
            sleep(5)
            new_track = self.api.get_track()
            self.TRACK = new_track
            if self.TRACK[0] != new_track[0]: return

    def show(self):
        self.print_track()
        while True:
            new_track_evt = Event()

            t1 = Thread(target=self.update)
            t2 = Thread(target=self.scroll, args=(new_track_evt, ))
            t1.start()
            t2.start()

            t1.join()
            new_track.set() # new_track als Parameter in Thread1 und statt return set()
            t2.join()


