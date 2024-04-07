from api_methods import fetch_team_by_name, fetch_games, fetch_pitch_details
from helper_methods import print_games, print_pitches, str_to_datetime
import subprocess
import time

IS_WINDOWS = False # Set to True if running on Windows, False if Mac.

MIN_START_DATE = '2015-01-01'
DEF_START_DATE = '2023-01-01' # Default start date.
MAX_END_DATE = '2023-12-31'
MAX_GAMES_TO_SHOW = 100


def prompt_for_start_date():
    """ Prompt user for the start date between MIN_START_DATE and MAX_END_DATE

    Returns:
        str: In the form YYYY-MM-DD.
    """
    
    # Prompt user.
    start_date = input(f"Enter the start date between {MIN_START_DATE} and {MAX_END_DATE} in the form YYYY or YYYY-MM-DD (default {DEF_START_DATE}): ")
    
    # Assume the user entered YYYY-MM-DD. Try converting it to a date. 
    start_date_obj = str_to_datetime(start_date)
    
    # If the conversion failed (user entered invalid string), assume the user entered YYYY. Try converting again.
    if start_date_obj is None:
        start_date += "-01-01"
        start_date_obj = str_to_datetime(start_date)
        
    # If the conversion is successful and the start date is in the valid range, return the string the user entered. 
    if start_date_obj is not None and str_to_datetime(MIN_START_DATE) <= start_date_obj <= str_to_datetime(MAX_END_DATE):
        print(f"Set start date to {start_date}.")
        return start_date
        
    # Otherwise, return the default start date.
    print(f"Set start date to default of {DEF_START_DATE}.")
    return DEF_START_DATE

def prompt_for_end_date(start_date):
    """ Prompt user for the end date between start_date and DEFAULT_END_DATE

    Args:
        start_date (str): The start date the user previously entered.

    Returns:
        str: In the form YYYY-MM-DD.
    """
    
    # Convert the start date to datetime.
    start_date_obj = str_to_datetime(start_date)
    
    # Set the maximum end date as December 31 of the year of the start date.
    max_end = f"{start_date_obj.year}-12-31"
    
    # Prompt the user.
    end_date = input(f"Enter the end date between {start_date} and {max_end} in the form YYYY-MM-DD (default {max_end}): ")
    
    # Try conveting the user's string to a datetime.
    end_date_obj = str_to_datetime(end_date)
    
    # If the conversion is successful and the end date is in the valid range, return the string the user entered.
    if end_date_obj is not None and str_to_datetime(start_date) <= end_date_obj <= str_to_datetime(max_end):
        print(f"Set end date to {end_date}.")
        return end_date
    
    # Otherwise, return the calculted max end date.
    print(f"Set end date to default of {max_end}.")
    return max_end
        

def prompt_for_team(season=None):
    """ Prompt user for name of a team to search for.
    
    Args:
        season (str, optional) : The current season as YYYY. Defaults to None.

    Returns:
        Team | None: The Team or None if team user entered is not found.
    """
        
    # Prompt user for team.
    team_name = input("Enter a team name, e.g. 'Oakland Athletics' or 'Oakland' or 'Athletics' (default all teams): ")
    
    # If no team entered, return None.
    if team_name == '':
        print("No team entered. Will show games with all teams.")
        return None
    
    # Get the team by name.
    team = fetch_team_by_name(team_name, season)
    if team is None:
        print("Team not found. Will show games with all teams.")
        return None
    
    # If the team is found, return it.
    print(f"Set team to {team}.")
    return team
        
        
def prompt_for_opponent(team, season=None):
    """ Prompt user for name of an opponent to search for.

    Args:
        team_id (Team | None): The original team. If None, return None.
        season (str, optional): The season in YYYY. Defaults to None.
        
    Returns:
        str | None : The opponent's id or None if not found or no original team is entered.
    """
    
    # If no original team is entered, do not prompt for an opponent.
    if team is None:
        return None
        
    # Prompt the user.
    opp_name = input("Enter an opposing team's name (default all teams): ")
    
    # If no opponent entered, return None.
    if opp_name == '':
        print("No opponent entered. Will show games against all opponents.")
        return None

    # Get the oppoennt by name.
    opponent = fetch_team_by_name(opp_name, season)
    if opponent is None:
        print("Team not found. Will show games against all opponents.")
        return None
    
    # Validate the opponent is not the same as the team entered.
    if opponent.id == team.id:
        print("Cannot set opponent to self. Will show games against all opponents.")
        return None
    
    # Return the opponent.
    print(f"Set opponent to {opponent.abbreviation} - {opponent.name}.")
    return opponent
    

def prompt_for_game(games):
    """ Prompt user to choose a game out of a list of games.

    Args:
        games (list[Game])

    Returns:
        Game | None: The game selected or None if no games are entered.
    """
        
    if games is None or len(games) == 0:
        return None
    
    total_games_found = len(games)

    # Calculate how many games to show.
    games_showing = MAX_GAMES_TO_SHOW if total_games_found > MAX_GAMES_TO_SHOW else total_games_found
    
    print(f"Showing {games_showing} of {total_games_found} games found...")
    print('')
    print_games(games[:games_showing])
    print('')
    
    # Prompt user.
    try:
        game_index = int(input(f"Enter a game number between 1 and {games_showing} (default 1): "))
    except ValueError:
        game_index = -1
        
    # Select game if valid, otherwise default of game #1.
    if 1 <= game_index <= games_showing:
        game = games[game_index - 1]
        print(f"Selected game number {game_index}.")
    else:
        game = games[0]
        print(f"Selected default game number 1.")
    
    return game
        
    
def prompt_for_pitch(game):
    """ Prompt user to choose a pitch from a game.

    Args:
        game (Game)

    Returns:
        Pitch | None: The pitch selected or None if invalid args.
    """
    
    print('')
    
    pitches = fetch_pitch_details(game)
    
    if pitches is None or len(pitches) == 0:
        return None
    
    pitches_len = len(pitches)
    
    print(f"Showing all {pitches_len} pitches found...")
    print('')
    print_pitches(pitches)
    print('')
    
    # Prompt user.
    try:
        pitch_index = int(input(f"Enter a pitch number between 1 and {pitches_len} (default 1): "))
    except ValueError:
        pitch_index = -1
        
    # Select pitch if valid, otherwise default of pitch #1.
    if 1 <= pitch_index <= pitches_len:
        pitch = pitches[pitch_index - 1]
        print(f"Selected pitch number {pitch_index}-", end='')
    else:
        pitch = pitches[0]
        print(f"Selected default pitch number 1-",end='')
        
    pitch_info = f" {pitch.pitch_type} | {round(pitch.pitch_data.get('startSpeed'))} MPH | {pitch.result}"
    print(pitch_info)
        
    return pitch
    
    
def display_title():
    print('')
    print('')
    print("[[ Rory's Pitch Simulator ]]")
    print('')
    print(f"Simulate any MLB pitch thrown between {MIN_START_DATE} and {MAX_END_DATE}.")
    print('')
    print("Current bugs: 1. Not finding as much game data as expected.")
    print('')
    print('Steps:')
    print("   1. Select a range of dates for games you would like to search for. All the games must be from the same season.")
    print("   2. Select 0-2 teams you would like to search for games with.")
    print(f"   3. Select a game from the first {MAX_GAMES_TO_SHOW} games found by the search.")
    print("   4. Select a pitch from the game to simulate.")
    print("If you leave any prompt blank or enter an invalid option, the default will be selected.")
    print('')
    input('Press ENTER to begin ')
    print('')
    

def prompt_for_rerun():
    """ Prompt the user to rerun the program.
    
    Returns:
        bool
    """
    
    user_input = input("Would you like to run the program again (y or n)? ")
    while True:
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        
        user_input = input("Invalid input. Would you like to run the program again (y or n)? ")
    
    
def run_on_windows(args):
    """ Run the Unity simulation for Windows.

    Args:
        args (dict[str, str]): A list of command line args to pass in.
    """
        
    try:
        subprocess.run(["WindowsBuild\Pitch.exe", *args.values()])
    except (FileNotFoundError, TypeError) as e:
        print(f"Simulation failed to run on Windows: {e}")
        return
    else:
        print("Simulation ran on Windows successfully!")
    
    
def run_on_mac(args):
    """ Run the Unity simulation for Mac.

    Args:
        args (dict[str, str]): A list of command line args to pass in.
    """
    
    # Use devnull to capture unwanted console output.
    with open('/dev/null', 'w') as devnull:
        try:
            subprocess.run(["MacBuild/Pitch.app/Contents/MacOS/Pitch", *args.values()], stdout=devnull, stderr=devnull)
        except (FileNotFoundError, TypeError) as e:
            print(f"Simulation failed to run on Mac: {e}")
            return
        else:
            print("Simulation ran on Mac successfully!")
        

    
if __name__ == '__main__':
    display_title()
    
    while True:
        
        # Prompt user for start date.
        start_date = prompt_for_start_date() 
        print('')

        # Prompt user for end date.
        end_date = prompt_for_end_date(start_date)
        print('')
        
        # Calculate the season.
        season = str_to_datetime(start_date).year
        
        # Prompt user for team.
        team = prompt_for_team(season)
        print('')
        
        # Prompt user for opponent.
        opponent = prompt_for_opponent(team, season)
        print('')
        
        team_id = team.id if team is not None else None
        opponent_id = opponent.id if opponent is not None else None
        
        # Get a list of games based on the user's preferences.
        games = fetch_games(start_date, end_date, team_id, opponent_id)
        
        if games is None:
            print('No games found!')
            if prompt_for_rerun():
                continue
            else:
                break
        
        # Prompt user for game.
        game = prompt_for_game(games)
        print('')

        # Prompt user for pitch.
        pitch = prompt_for_pitch(game)
        print('')
    
        # Get the arguments to call the command line. These are named as a precaution for bugs.
        p_data = pitch.pitch_data
        p_data_coords = pitch.pitch_data.get('coordinates')
        p_data_breaks = pitch.pitch_data.get('breaks')
        
        # Coordinate axis origin is back of home plate.
        pitch_args = {
            'strikeZoneTop': p_data.get('strikeZoneTop'), # Top of strike zone in ft from z=0 (ground)
            'strikeZoneBot': p_data.get('strikeZoneBottom'), # Bottom of strike zone ft from z=0 (ground)
            'aX50': p_data_coords.get('aX'), # Acceleration in X direction at 'y50' in ft/s^2, we assume this to be constant for the pitch.
            'aY50': p_data_coords.get('aY'), # Acceleration in Y direction at 'y50' in ft/s^2, we assume this to be constant for the pitch.
            'aZ50': p_data_coords.get('aZ'), # Acceleration in Z direction at 'y50' in ft/s^2
            'vX50': p_data_coords.get('vX0'), # Velocity in X direction at 'y50' in ft/s
            'vY50': p_data_coords.get('vY0'), # Velocity in Y direction at 'y50' in ft/s
            'vZ50': p_data_coords.get('vZ0'), # Velocity in Z direction at 'y50' in ft/s
            'x50': p_data_coords.get('x0'), # X coordinates at 'y50' in ft
            'y50': p_data_coords.get('y0'), # Y coordinates, taken as close to 50 ft from the back of home plate as possible
            'z50': p_data_coords.get('z0'), # Z coordinates at 'y50' in ft
            'x0': p_data_coords.get('pX'), # X coordinates at y=1.417 in ft
            'z0': p_data_coords.get('pZ'), # X coordinates at =1.417 in ft            
            'spinDirection': p_data_breaks.get('spinDirection'), # The angle the ball is spinning.
            'extension': p_data.get('extension'), # Assumed to mean the distance the pitcher is from the rubber (y=60.5) when the ball is thrown in ft.
        }
        
        # Convert all args to strings.
        pitch_args = {key:str(value) for (key,value) in pitch_args.items()}
        
        # Run the program.
        print("Running the simulation...")
        print('')
        time.sleep(0.5)
        
        if IS_WINDOWS:
            run_on_windows(pitch_args)
        else:
            run_on_mac(pitch_args)
        
        print('')
        if prompt_for_rerun():
            print('')
            continue
        else:
            break
    
    print('')
    print('Program exit successful.')
    