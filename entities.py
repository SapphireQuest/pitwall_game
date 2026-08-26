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
        self.last_lap_time = 0

    def drive_lap(self, decision, race_weather, current_lap):
        water_level = race_weather[current_lap-1]
        tire = self.current_tire.type_of_compound
        if decision == PIT: 
            pass

        if tire in ("Soft", "Medium", "Hard"):
            if water_level < 20: 
                min_time, max_time = 84.0, 86.5
            else: 
                min_time, max_time = 105.0, 115.0
                
        elif tire == "Inter":
            if water_level < 20:
                min_time, max_time = 89.0, 92.0
            elif 20 <= water_level <= 75:
                min_time, max_time = 90.0, 93.0
            else:
                min_time, max_time = 100.0, 105.0
                
        elif tire == "Wet":
            if water_level < 60:
                min_time, max_time = 94.0, 98.0
            else:
                min_time, max_time = 95.0, 98.0

        if decision == LIFT:
            min_time += 2.5
            max_time += 2.5
            
        self.last_lap_time = random.uniform(min_time, max_time)
        self.total_race_time += self.last_lap_time
        self.current_tire.degrade_tire(decision)


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


def make_decision():
    while True:
        print("Decision: 1 - Lift and Coast, 2 - Push, 3 - Pit")
        decision = input()
        if not decision.isnumeric():
            print("Decision must be a number.")
            continue
        decision = int(decision)

        if decision in settings.possible_decisions:
            break
        else:
            print("Possible decisions are 1, 2 or 3.")

    if decision == PIT:
        print("Pit Stop")
        return PIT
    elif decision == PUSH:
        print("Push")
        return PUSH
    elif decision == LIFT:
        print("Lift and Coast")
        return LIFT

