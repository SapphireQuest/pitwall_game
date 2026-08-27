import random
import settings

LIFT = settings.LIFT
PUSH = settings.PUSH
PIT = settings.PIT

class Tire:
    def __init__(self, type_of_compound):
        self.type_of_compound = settings.possible_tire_compounds.get(type_of_compound)
        self.deg_level = 100  #100 max performance, 0 puncture

    def degrade_tire(self, decision, water_level):
        tire = self.type_of_compound
        base_deg = 0

        if tire == "Soft":
            base_deg = random.randint(8, 10)
        elif tire == "Medium":
            base_deg = random.randint(5, 7)
        elif tire == "Hard":
            base_deg = random.randint(3, 5)

        elif tire == "Inter":
            base_deg = random.randint(4, 6)
            if water_level < 20:
                base_deg += (20 - water_level) // 2
            elif water_level > 75:
                base_deg += (water_level - 75) // 6 

        elif tire == "Wet":
            base_deg = random.randint(4, 6)
            if water_level < 20:
                base_deg += (20 - water_level) // 2
            elif 20 <= water_level < 60:
                
                base_deg += (60 - water_level) // 10

        if decision == PUSH:
            base_deg += (base_deg // 5)
        elif decision == LIFT:
            base_deg = (base_deg * 65) // 100 

        self.deg_level = max(0, self.deg_level - base_deg)
            

class Car:
    def __init__(self, driver_name, is_player_controlled, current_tire: Tire):
        self.driver_name = driver_name
        self.total_race_time = 0
        self.is_player_controlled = is_player_controlled
        self.current_tire = current_tire
        self.last_lap_time = 0

    def drive_lap(self, decision, race_weather, current_lap):
        if decision == PIT:
            pass 
            return

        water_level = race_weather[current_lap - 1]
        tire = self.current_tire.type_of_compound
        deg = self.current_tire.deg_level
        
        base_time = 84.0
        
        if tire in ("Soft", "Medium", "Hard"):
            if tire == "Medium": base_time += 0.8
            elif tire == "Hard": base_time += 1.5
                
            if water_level <= 20:
                base_time += water_level * 0.1 
            else:
                base_time += 2.0 + ((water_level - 20) * 0.6) 
                
        elif tire == "Inter":
            base_time += 4.5 
            if water_level < 20:
                base_time += (20 - water_level) * 0.3 
            elif 20 <= water_level <= 75:
                base_time += (water_level - 20) * 0.03 
            else:
                base_time += 1.65 + ((water_level - 75) * 0.5) 
                
        elif tire == "Wet":
            base_time += 5.5 
            if water_level < 60:
                base_time += (60 - water_level) * 0.25 
            else:
                base_time += (water_level - 60) * 0.02 
                
        normal_deg_penalty = (100 - deg) * 0.025
        
        if tire in ("Inter", "Wet"):
            normal_deg_penalty *= 0.5
            
        base_time += normal_deg_penalty
        
        if deg < 30:
            cliff_penalty = (30 - deg) * 0.4
            base_time += cliff_penalty
            
        if decision == LIFT:
            base_time += 2.5
            
        self.last_lap_time = base_time + random.uniform(-0.15, 0.15)
        self.total_race_time += self.last_lap_time
        
        self.current_tire.degrade_tire(decision, water_level)


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


def ai_decision(race_weather, grid, current_lap):
    weather_pointer = current_lap - 1
    water_level = race_weather[weather_pointer]
    for driver in grid: 
        if driver.is_player_controlled == True:
            continue
        tire = driver.current_tire.type_of_compound
        good_tire  = False
        if (tire in ("Soft", "Medium", "Hard") and water_level < 20) or (tire == "Inter" and water_level >= 20 or water_level <= 75) or (tire == "Wet" and water_level >= 60):
            good_tire = True

        if driver.current_tire.deg_level == 0:
            pass
            # pitstop


        