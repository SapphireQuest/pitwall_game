import settings
import ui
import racetrack 
import entities

LIFT = settings.LIFT
PUSH = settings.PUSH
PIT = settings.PIT


class Race_Manager:
    def __init__(self):
        self.grid = []
        self.is_race_on = False
        self.current_lap = 1




def main():
    ui.display_starting_screen()
    player_name = ui.get_player_name()
    race_manager = Race_Manager()

    while True:
        track = racetrack.Track()
        track.decide_race_weather()
        ui.display_before_the_race_info(track)
        ui.display_weather_prediction(race_manager.current_lap, track.race_weather, race_manager.is_race_on)

        player_tires = ui.get_player_tires()

        player_car = entities.Car(driver_name = player_name, is_player_controlled = True, current_tire = player_tires)

        race_manager.grid.append(player_car)

        entities.create_ai_drivers(track, race_manager.grid)
        
        ui.display_grid(race_manager.is_race_on, race_manager.grid)

        start = ui.start_race()
        if not start:
            ui.display_new_race() 
            race_manager.grid.clear()
            continue
        race_manager.is_race_on = True
        break


    while True:
        if race_manager.is_race_on:
            ui.display_lap(race_manager.current_lap)
            ui.display_grid(race_manager.is_race_on, race_manager.grid)
            ui.display_current_weather(race_manager.current_lap, track.race_weather)
            ui.display_weather_prediction(race_manager.current_lap, track.race_weather, race_manager.is_race_on)
            
            decision = entities.make_decision()  # 3 pitstop, 2 push, 1 lift
            player_car.drive_lap(decision, track.race_weather, race_manager.current_lap)
            

            # ai_decision()
            # pit_stop()
            # sort_entities()
            race_manager.current_lap += 1
            if race_manager.current_lap > track.total_laps:
                print("RACE END")
                # display_results()
                return 


if __name__ == '__main__':
    main()