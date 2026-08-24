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


def display_grid(is_race_on, grid):
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
        table.add_row(str(pos),name, str(current_tire.type_of_compound), str(wear))
    print("")
    console.print(table)

def start_race():
    start_race = input("Start race? (y/n)")
    if start_race.lower() == "y":
        return True
    return False 


def display_lap(current_lap):
    print(Panel(f"LAP {current_lap}", expand=True, border_style="red", style="bold white"))

def display_new_race():
    print(Panel("NEW RACE", expand=True, border_style="red", style="bold white"))