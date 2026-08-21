import settings
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print
console = Console()

grid = []
is_race_on = False
current_lap = 1

class Tire:
    def __init__(self, type):
        self.type = settings.possible_tire_compounds.get(type)
        self.deg_level = 100  #100 max performance, 0 puncture

    def degrade_tire(self, decision):
        if decision == 2:
            r = random.randint(6,8)
            self.deg_level -= r
        elif decision == 1:
            r = random.randint(3,5)
            self.deg_level -= r
            

class Car:
    def __init__(self, driver_name, is_player_controlled, current_tire: Tire):
        self.driver_name = driver_name
        self.total_race_time = 0
        self.is_player_controlled = is_player_controlled
        self.current_tire = current_tire

    def drive_lap(self, decision):
        if decision == 3:
            # pitstop 
            pass
        elif decision == 2:
            # push
            r = random.uniform(84.234, 86.753)
            self.total_race_time += r
            self.current_tire.degrade_tire(2)
        elif decision == 1:
            r = random.uniform(86.903, 90.002)
            self.total_race_time += r
            self.current_tire.degrade_tire(1)


class Track:
    def __init__(self):
        tracks = settings.tracks
        self.current_track, self.total_laps = random.choice(list(tracks.items()))
        self.is_dry = random.randint(1,10) >= 3
        self.water_percentage = 0 if self.is_dry else random.randint(20,90)


    def display_before_the_race_info(self):
        if self.is_dry:
            text_style = "bold green"
            weather_info = "Dry"
        else:
            text_style = "bold blue"
            weather_info = "Wet"

        table = Table(title="Information about the race")
        table.add_column("Track", justify="right", style="bold white")
        table.add_column("Laps",justify="center", style="bold white")
        table.add_column("Weather",justify="center" , style= text_style)
        table.add_column("Water on track", justify="center", style="bold yellow")
  
        water_on_track = f"{self.water_percentage}%"

        table.add_row(self.current_track, str(self.total_laps), weather_info, water_on_track)

        print("")
        console.print(table)


def get_player_name():
    while True:
        player_name = input("Provide your driver name: ")
        if len(player_name) >=2 and len(player_name) <=20:
            break
        else:
            print("Length of player name should be between 2 and 20 characters.")
    return player_name


def get_player_tires():
    # 1 - soft, 2 - med, 3 - hard, 4 - inter, 5 - wet
    table = Table(title="Choose tires")
    table.add_column("Number", justify="right")
    table.add_column("Tire Compound")
    table.add_column("Weather Condition")

    table.add_row("1", "Soft", "Dry", style="bold red")
    table.add_row("2", "Medium", "Dry", style="bold yellow")
    table.add_row("3", "Hard", "Dry", style="bold white")
    table.add_row("4", "Inter", "Wet | 20-75%", style="bold green")
    table.add_row("5", "Wet", "Wet | 60-100%", style="bold blue")

    console.print(table)

    while True: 
        tire_compound = input("Choose your tire compound (1-5): ")
        if tire_compound in ("1", "2", "3", "4", "5"):
            break
        else:
            print("Must be the number between 1 and 5.")
    player_tire_compound = Tire(str(tire_compound))
    return player_tire_compound


def create_ai_drivers(track: Track):
    for name in settings.driver_names:
        if track.is_dry:
            tire_compound = random.randint(1,3)
        else:
            if track.water_percentage <=60:
                tire_compound = 4
            elif track.water_percentage > 60 and track.water_percentage <= 75:
                tire_compound = random.randint(4,5)
            else:
                tire_compound = 5

        ai_tire = Tire(str(tire_compound))
        ai_car = Car(driver_name = name, is_player_controlled = False, current_tire = ai_tire)
        grid.append(ai_car)


def display_starting_screen():
    print(Panel("F1 PITWALL GAME", expand=False, border_style="red", style="bold white"))


def display_grid():
    if is_race_on:
        title_to_display = "Live Standings"
    else:
        title_to_display = "Grid before the race"
    table = Table(title=title_to_display)
    table.add_column("Pos", justify="right", style="cyan")
    table.add_column("Driver", style="bold white")
    table.add_column("Tire", style="bold yellow")
    table.add_column("Wear", justify="right", style="green")

    for pos, driver in enumerate(grid, start=1):
        name = driver.driver_name
        current_tire = driver.current_tire
        wear = driver.current_tire.deg_level
        table.add_row(str(pos),name, str(current_tire.type), str(wear))
    print("")
    console.print(table)


def start_race():
    start_race = input("Start race? (y/n)")
    if start_race.lower() == "y":
        return 1
    return 0 

def display_lap():
    print(Panel(f"LAP {current_lap}", expand=True, border_style="red", style="bold white"))


def make_decision():
    while True:
        decision = input("Decision: 1 - Lift and Coast, 2 - Push, 3 - Pit")
        if not decision.isnumeric():
            print("Decision must be a number.")
            continue
        decision = int(decision)

        if decision in settings.possible_decisions:
            break
        else:
            print("Possible decisions are 1, 2 or 3.")

    if decision == 3:
        print("Pit Stop")
        return 3
    elif decision == 2:
        print("Push")
        return 2
    elif decision == 1:
        print("Lift and Coast")
        return 1


def main():
    global is_race_on
    display_starting_screen()

    player_name = get_player_name()

    while True:
        track = Track()
        track.display_before_the_race_info()

        player_tires= get_player_tires()

        player_car = Car(driver_name = player_name, is_player_controlled = True, current_tire = player_tires)
        grid.append(player_car)

        create_ai_drivers(track)
        
        display_grid()

        start = start_race()
        if start == 0:
            print(Panel("NEW RACE", expand=True, border_style="red", style="bold white"))
            grid.clear()
            continue
        is_race_on = True
        break


    while True:
        if is_race_on:
            display_lap()
            display_grid()
            # display_current_weather()
            # display_weather_prediction()
            
            decision = make_decision()  # 3 pitstop, 2 push, 1 lift
            player_car.drive_lap(decision)


            # ai_decision()
            # pit_stop()






            


if __name__ == '__main__':
    main()