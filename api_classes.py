# This file defines a list of classes that represent data from https://statsapi.mlb.com

class Team:
    def __init__(self, name, id, franchise_name, club_name, abbreviation):
        """ A class to store information about a team.

        Args:
            All of type str.
        """
        self.name = name
        self.id = id
        self.franchise_name = franchise_name
        self.club_name = club_name
        self.abbreviation = abbreviation
        
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Game:
    def __init__(self, home_team, away_team, link, date, score):
        """ A class to store information about a game.

        Args:
            home_team (Team)
            away_team (Team)
            link (str): A link to API information about the game, not including base of "https://statsapi.mlb.com".
            date (str): A date in YYYY-MM-DD format.
            score (str): A score in "X-Y" format, X is the home team's score and Y is the away team's score.
        """
        self.home_team = home_team
        self.away_team = away_team
        self.link = link
        self.date = date
        self.score = score


class Pitch:
    def __init__(self, pitcher_name, pitcher_hand, batter_name, batter_hand, result, pitch_type, balls_before, strikes_before, outs_before, pitch_data, half_inning, inning, home_score_before, away_score_before, home_abbreviation, away_abbreviation):
        self.pitcher_name = pitcher_name
        self.pitcher_hand = pitcher_hand
        self.batter_name = batter_name
        self.batter_hand = batter_hand
        self.result = result
        self.pitch_type = pitch_type
        self.balls_before = balls_before
        self.strikes_before = strikes_before
        self.outs_before = outs_before
        self.pitch_data = pitch_data
        self.half_inning = half_inning
        self.inning = inning
        self.home_score_before = home_score_before
        self.away_score_before = away_score_before
        self.home_abbreviation = home_abbreviation
        self.away_abbreviation = away_abbreviation
    
    def __str__(self):
        speed = self.pitch_data.get('startSpeed')
        return f"{self.half_inning.title()[:3]} {self.inning} | " \
            f"{self.home_abbreviation} {self.home_score_before} - {self.away_abbreviation} {self.away_score_before} | " \
            f"{self.outs_before} Outs | " \
            f"{self.balls_before}-{self.strikes_before} Count | " \
            f"{self.pitch_type} ({round(speed)} MPH) | {self.result} | " \
            f"{self.pitcher_name} ({self.pitcher_hand}HP) vs {self.batter_name} ({self.batter_hand}HB)"
