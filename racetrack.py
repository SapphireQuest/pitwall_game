import random
import settings

class Track:
    def __init__(self):
        tracks = settings.tracks
        self.current_track, self.total_laps = random.choice(list(tracks.items()))
        self.is_dry = random.randint(1,10) >= 3
        self.water_percentage = 0 if self.is_dry else random.randint(20,90)
        self.race_weather = []
        self.race_weather.append(self.water_percentage)

    def decide_race_weather(self):
        rain_rising = False
        counter_of_rain_rise = 3
        for _ in range(1,self.total_laps):
            if counter_of_rain_rise == 0:
                rain_rising = False
                counter_of_rain_rise = 3
            
            if rain_rising:
                self.water_percentage += random.randint(8,17)
                counter_of_rain_rise -= 1

            if self.is_dry:
                if random.randint(1,10) > 7:
                    self.water_percentage += random.randint(6,11)
                    rain_rising = True

            else:
                if self.water_percentage < 20:
                    self.water_percentage -= random.randint(4,9)
                elif self.water_percentage >= 20 and self.water_percentage <= 100:
                    if random.randint(1,10) > 5:
                        self.water_percentage -= random.randint(4,10)
                    else:
                        self.water_percentage += random.randint(4,9)


           
            if self.water_percentage < 0:
                self.water_percentage = 0
            if self.water_percentage > 100:
                self.water_percentage = 100
            if self.water_percentage > 0:
                self.is_dry = False
            if self.water_percentage == 0:
                self.is_dry = True
            self.race_weather.append(self.water_percentage)
