import settings
from rich.console import Console
from rich.table import Table
console = Console()

class Car:
    def __init__(self, driver_name, is_player_controlled):
        self.driver_name = driver_name
        self.total_race_time = 0
        self.is_player_controlled = is_player_controlled


laps = 10
current_lap = 1 
grid = []
is_race_on = 1
# 1 - soft, 2 - med, 3 - hard, 4 - inter, 5 - wet

def main():
    player_name = input("Provide your driver name: ")
    player_car = Car(driver_name = player_name, is_player_controlled = True)
    grid.append(player_car)
    
    for name in settings.driver_names:
        ai_car = Car(driver_name = name, is_player_controlled = False)
        grid.append(ai_car)

    
    


    while True:
        if is_race_on:
            table = Table(title="Live Standings")
            table.add_column("Pos", justify="right", style="cyan")
            table.add_column("Driver", style="bold white")
            table.add_column("Tire", style="bold yellow")
            table.add_column("Wear", justify="right", style="green")
        
            table.add_row("1", "Verstappen", "Medium", "85%")
            table.add_row("2", "Player", "Soft", "42%") 
            table.add_row("3", "Norris", "Hard", "96%")

            console.print(table)

            while True:
                while True:
                    decision = input("Decision: 1 - Lift and Coast, 2 - Push, 3 - Pit")
                    if decision.isnumeric():
                        break
                    else:
                        print("Decision must be a number")
                decision = int(decision)
                if decision in settings.possible_decisions:
                    break
                else:
                    print("Possible decisions are 1, 2 or 3")

            if decision == 3:
                print("Pit Stop")
            elif decision == 2:
                print("Push")
            elif decision == 1:
                print("Lift and Coast")


if __name__ == '__main__':
    main()