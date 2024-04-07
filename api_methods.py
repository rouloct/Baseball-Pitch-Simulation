# This file defines a list of methods used to get data from https://statsapi.mlb.com

import requests
from api_classes import Team, Game, Pitch


def fetch_teams(season=None):
    """ Get a list of all teams.

    Args:
        season (str, optional): In the form YYYY. Defaults to None.

    Returns:
        list[Team] | None: Returns a list of Teams or None.
    """
    
    # The target URL for the GET request.
    url = 'https://statsapi.mlb.com/api/v1/teams'
    
    # The default GET request parameters, named "payload" by convention.
    payload = {
        'sportId': 1
        }
    
    # Add extra parameters if passed to function.
    if season is not None:
        payload.update({'season': str(season)})
    
    # Get data with GET request, by convention named 'r'. 
    r = requests.get(url, params=payload)
    
    if r.status_code != 200:
        print(f"Request failed with status code {r.status_code}")
        return None
        
    # Convert the data to JSON.
    data = r.json()
    
    # Get an array of teams.
    data_teams = data.get('teams')
    
    # If data_teams is empty or not found return None.
    if data_teams is None or len(data_teams) == 0:
        return None
    
    # Initialize a list of Teams.
    team_objs = []
    
    # Convert each JSON team to a Team instance.
    for team in data_teams:
        name = str(team.get('name'))
        id = str(team.get('id'))
        franchise_name = str(team.get('franchiseName'))
        club_name = str(team.get('clubName'))
        abbreviation = str(team.get('abbreviation'))
        team_objs.append(Team(name, id, franchise_name, club_name, abbreviation))
        
    return team_objs if len(team_objs) != 0 else None


def fetch_team_by_name(name: str, season=None):
    """Get a team's by its name, franchise name, or club name.

    Args:
        name (str): A name representing the team, e.g. 'Oakland Athletics' or 'Oakland' or 'Athletics'
        season (str, optional): The season in YYYY. Defaults to None
    Returns:
        Team | None: The Team or None if not found
    """
    
    return next((team for team in fetch_teams(season) if name.title() in [team.name, team.franchise_name, team.club_name]), None)


def fetch_games(start_date=None, end_date=None, team_id=None, opponent_id=None):
    """ Get a list of games. Defaults to all games this season.

    Args:
        start_date (str, optional): In the form YYYY-MM-DD. Defaults to None. Error if start_date and not end_date.
        end_date (str, optional): In the form YYYY-MM-DD. Defaults to None. Error if end_date and not start_date or if end_date is before start_date.
        team_id (str, optional): A team's id. Defaults to None. 
        opponent_id (str, optional): An opponent's id. Defaults to None. Error if opponent_id and not team_id.
    
    Returns:
        list[Game] | None: A list of Games or None.
    """
    
    # The target URL for the GET request.
    url = 'https://statsapi.mlb.com/api/v1/schedule'
    
    # The default GET request parameters, named "payload" by convention.
    payload = {
        'sportId': 1, # Baseball.
        'leagueId': 103, # MLB league.
        'gameType': 'R' # Regular season.
    }
    
    # Add extra parameters if passed to function.
    if start_date is not None:
        payload.update({'startDate': start_date})
    
    if end_date is not None:
        payload.update({'endDate': end_date})
        
    if team_id is not None:
        payload.update({'teamId': team_id})
        
    if opponent_id is not None:
        payload.update({'opponentId': opponent_id})

    # Get data with GET request, by convention named 'r'. 
    r = requests.get(url, params=payload)
    
    if r.status_code != 200:
        print(f"Request failed with status code {r.status_code}")
        return None
        
    # Convert the data to JSON.
    data = r.json()
    
    # Get a list of "dates".
    data_dates = data.get('dates')
        
    # If data_dates is empty or not found return None.
    if data_dates is None or len(data_dates) == 0:
        return None
    
    # Get all teams.
    teams = fetch_teams()
    
    # Initialize a list of Games.
    game_objs = []
    
    # Iterate through each date.
    for date in data_dates:
        data_games = date.get('games')
        
        # Iterate through each game.
        for game in data_games:
            
            # Get a variety of data.
            data_home_team = game.get('teams').get('home')
            data_away_team = game.get('teams').get('away')
            home_team_id = str(data_home_team.get('team').get('id'))
            away_team_id = str(data_away_team.get('team').get('id'))
            
            # Get the Team representing the home team and away team.
            home_team = None
            away_team = None
            for team in teams:
                if home_team_id == team.id:
                    home_team = team
                if away_team_id == team.id:
                    away_team = team
                if home_team is not None and away_team is not None:
                    break
                
            # If either Team is not found, do not add the game
            if home_team is None or away_team is None:
                continue
            
            # Get a variety of data.
            link = str(game.get('link'))
            date = str(game.get('officialDate'))
            home_score = data_home_team.get('score')
            away_score = data_away_team.get('score')
            score = f"{home_score} - {away_score}" if home_score is not None and away_score is not None else "Unknown"
            
            # Add a new Game object to the list.
            game_objs.append(Game(home_team, away_team, link, date, score))
        
    # If game_objs is empty return None, otherwise return game_objs
    return game_objs if len(game_objs) != 0 else None


def fetch_pitch_details(game):
    """ Get a list of pitches based on a Game.

    Args:
        game (Game)

    Returns:
        list[Pitch] | None: A list of Pitch objects or None.
    """
    
    url = "http://statsapi.mlb.com" + game.link
    
    # Get data with GET request, by convention named 'r'. 
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"Request failed with status code {r.status_code}")
        return None
        
    # Convert the data to JSON.
    data = r.json()
    
    # Get a list of plays.
    try:
        plays = data.get('liveData').get('plays').get('allPlays')
    except AttributeError:
        # Plays not found. Return None
        print("Error: list of plays in game not found!")
        return None
    
    # Initialize a list of pitch objects.
    pitch_objs = []
    
    # Initialize helper variables
    home_score_before = 0
    away_score_before = 0
    home_score_after = 0
    away_score_after = 0
    
    # Iterate through each play
    for play in plays:
        # If the play is not an at-bat, go to the next one.
        if play.get('result').get('type') != 'atBat':
            continue
        
        # Get a variety of data.
        pitcher_name = play.get('matchup').get('pitcher').get('fullName')
        pitcher_hand = play.get('matchup').get('pitchHand').get('code') # R or L
        batter_name = play.get('matchup').get('batter').get('fullName')
        batter_hand = play.get('matchup').get('batSide').get('code') # R or L
        half_inning = play.get('about').get('halfInning') # top or bottom
        inning = play.get('about').get('inning')
    
        events = play.get('playEvents')
        
        # Set future home score and away score.
        home_score_after = play.get('result').get('homeScore')
        away_score_after = play.get('result').get('awayScore')
        
        # Iterate through each event.
        for event in events:
            # If the event is not a pitch, go to the next one.
            if event.get('isPitch') == False:
                continue
            
            # Get a variety of data.
            result = event.get('details').get('call').get('description')
            pitch_type = event.get('details').get('type').get('description')
            balls_before = event.get('count').get('balls')
            strikes_before = event.get('count').get('strikes')
            outs_before = event.get('count').get('outs')
            pitch_data = event.get('pitchData')
            
            # Add a new Pitch object to the list.
            pitch_objs.append(Pitch(pitcher_name=pitcher_name, pitcher_hand=pitcher_hand, batter_name=batter_name, batter_hand=batter_hand, result=result, pitch_type=pitch_type, balls_before=balls_before, strikes_before=strikes_before, outs_before=outs_before, pitch_data=pitch_data, half_inning=half_inning, inning=inning, home_score_before=home_score_before, away_score_before=away_score_before, home_abbreviation=game.home_team.abbreviation, away_abbreviation=game.away_team.abbreviation))
    
            # Update the home and away score before.
            home_score_before = home_score_after
            away_score_before = away_score_after
            
    return pitch_objs if len(pitch_objs) != 0 else None
    