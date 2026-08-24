import random
import settings

LIFT = settings.LIFT
PUSH = settings.PUSH
PIT = settings.PIT

class Tire:
    def __init__(self, type_of_compound):
        self.type_of_compound = settings.possible_tire_compounds.get(type_of_compound)
        self.deg_level = 100  #100 max performance, 0 puncture

    def degrade_tire(self, decision):
        if decision == PUSH:
            r = random.randint(6,8)
            self.deg_level -= r
        elif decision == LIFT:
            r = random.randint(3,5)
            self.deg_level -= r
            

class Car:
    def __init__(self, driver_name, is_player_controlled, current_tire: Tire):
        self.driver_name = driver_name
        self.total_race_time = 0
        self.is_player_controlled = is_player_controlled
        self.current_tire = current_tire

    def drive_lap(self, decision):
        if decision == PIT: 
            pass
        elif decision == PUSH:
            r = random.uniform(84.234, 86.753)
            self.total_race_time += r
            self.current_tire.degrade_tire(PUSH)
        elif decision == LIFT:
            r = random.uniform(86.903, 90.002)
            self.total_race_time += r
            self.current_tire.degrade_tire(LIFT)


def create_ai_drivers(track, grid):
    for name in settings.driver_names:
        if track.race_weather[0] == 0:
            tire_compound = random.randint(1,3)
        else:
            if track.race_weather[0] <=60:
                tire_compound = 4
            elif track.race_weather[0] > 60 and track.race_weather[0] <= 75:
                tire_compound = random.randint(4,5)
            else:
                tire_compound = 5

        ai_tire = Tire(str(tire_compound))
        ai_car = Car(driver_name = name, is_player_controlled = False, current_tire = ai_tire)
        grid.append(ai_car)

