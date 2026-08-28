from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print
import entities
console = Console()



def display_starting_screen():
    print(Panel("F1 PITWALL GAME", expand=False, border_style="red", style="bold white"))


def get_player_name():
    while True:
        player_name = input("Provide your driver name: ")
        if len(player_name) >=2 and len(player_name) <=20:
            break
        else:
            print("Length of player name should be between 2 and 20 characters.")
    return player_name


def display_before_the_race_info(track):
        if track.race_weather[0] == 0:
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
  
        water_on_track = f"{track.race_weather[0]}%"

        table.add_row(track.current_track, str(track.total_laps), weather_info, water_on_track)

        print("")
        console.print(table)


def display_weather_prediction(current_lap, race_weather, is_race_on):
    total_laps = len(race_weather)

    if not is_race_on:
        first_predicted_lap = 1
    else:
        first_predicted_lap = current_lap + 1

    if first_predicted_lap > total_laps:
        return

    laps_left_to_predict = total_laps - first_predicted_lap + 1
    columns_to_draw = min(3, laps_left_to_predict)

    table = Table(title="Weather Prediction")
    row_data = []

    for i in range(columns_to_draw):
        lap_number = first_predicted_lap + i
        weather_value = f"{race_weather[lap_number - 1]}%" 
        
        table.add_column(f"Lap {lap_number}", style="bold white", justify="center")
        row_data.append(weather_value)
        
    table.add_row(*row_data) 
    
    console.print(table)
    print("")


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
    player_tire_compound = entities.Tire(str(tire_compound))
    return player_tire_compound


def display_current_weather(current_lap, race_weather):
    if race_weather[current_lap-1] == 0:
        weather_style = "bold green"
    else:
        weather_style = "bold blue"
    table = Table(title = "Current Lap Weather")
    table.add_column("Water Level", justify="center")
    table.add_row(f"{race_weather[current_lap-1]}%", style=weather_style)
    console.print(table) 



def display_grid(is_race_on, grid):
    if is_race_on:
        title_to_display = "Live Standings"
    else:
        title_to_display = "Grid before the race"

    table = Table(title=title_to_display)
    table.add_column("Pos", justify="right", style="cyan")
    table.add_column("Driver", style="bold white")
    table.add_column("Tire", style="bold yellow")

    if is_race_on:
        table.add_column("Wear", justify="right", style="green")
        table.add_column("Interval", style="bold white")
        table.add_column("Last Lap Time", style="cyan")
        # table.add_column("Pit stops")

    for pos, driver in enumerate(grid, start=1):
        name = driver.driver_name
        current_tire = driver.current_tire
        row_style=""
        if is_race_on:
            wear = driver.current_tire.deg_level
            gap_to_leader = get_gap(pos, grid)
            row_style = ""
            if driver.is_player_controlled:
                row_style = "blue_violet"
            last_lap_time = f"{round(driver.last_lap_time, 3)}s"
        
        if is_race_on:
            table.add_row(str(pos),name, str(current_tire.type_of_compound), str(wear), gap_to_leader, last_lap_time, style=row_style)
        else:
            table.add_row(str(pos),name, str(current_tire.type_of_compound), style=row_style)

    print("")
    console.print(table)


def get_gap(pos, grid):
    if pos == 1:
        return "Interval"
    else:
        previous_driver_time = grid[pos-2].total_race_time
        current_driver_time = grid[pos-1].total_race_time
        gap = current_driver_time - previous_driver_time
        return f"+{round(gap, 3)}s"



def start_race():
    start_race = input("Start race? (y/n)")
    if start_race.lower() == "y":
        return True
    return False 


def display_lap(current_lap):
    print(Panel(f"LAP {current_lap}", expand=True, border_style="red", style="bold white"))

def display_new_race():
    print(Panel("NEW RACE", expand=True, border_style="red", style="bold white"))

def puncture_message():
    print(Panel("PUNCTURE", expand=False, border_style="white", style=" bold red"))