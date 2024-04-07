from tabulate import tabulate
from datetime import datetime

def print_games(games):
    """ Print a list of Games using tabulate.

    Args:
        games (list[Game])
    """
    
    headers = ['#', 'Date', 'Teams', 'Result']
    
    table_data = []
    for index, game in enumerate(games):
        table_data.append([
            index + 1,
            game.date,
            f"{game.home_team.abbreviation} vs {game.away_team.abbreviation}",
            game.score
        ])
        
    print(tabulate(table_data, headers=headers))
    

def print_pitches(pitches):
    """ Print a list of Pitches using tabulate.

    Args:
        pitches (list[Pitch])
    """
    
    headers = ['#','Inn', 'Score', 'Outs', 'Count', 'Type', 'Speed', 'Result', 'Pitcher', 'Batter']
    
    table_data = []
    
    for index, pitch in enumerate(pitches):
        pitcher_parts = pitch.pitcher_name.split()
        batter_parts = pitch.batter_name.split()
        pitcher_name = f"{pitcher_parts[0][0].upper()}. {' '.join(pitcher_parts[1:])}" if len(pitcher_parts) > 1 else pitch.pitcher_name
        batter_name = f"{batter_parts[0][0].upper()}. {' '.join(batter_parts[1:])}" if len(batter_parts) > 1 else pitch.batter_name
        
        table_data.append([
            index + 1,
            f"{pitch.half_inning.title()[:3]} {pitch.inning}",
            f"{pitch.home_score_before} {pitch.home_abbreviation} {pitch.away_abbreviation} {pitch.away_score_before}",
            f"{pitch.outs_before} Outs",
            f"{pitch.balls_before}-{pitch.strikes_before} Count",
            pitch.pitch_type,
            f"{round(pitch.pitch_data.get('startSpeed'))} MPH",
            pitch.result,
            f"{pitcher_name} ({pitch.pitcher_hand})",
            f"{batter_name} ({pitch.batter_hand})"
        ])
        
    print(tabulate(table_data, headers=headers))


def str_to_datetime(date_str):
    """ Convert a string in YYYY-MM-DD to a datetime.

    Args:
        date_str (str)

    Returns:
        datetime | None: Returns None if the string cannot be converted.
    """
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj
    except ValueError:
        return None
