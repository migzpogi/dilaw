from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


def did_lakers_win():
    lal_id = teams.find_team_by_abbreviation('LAL')['id']
    game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=lal_id)
    all_games = game_finder.get_data_frames()[0]
    most_recent = all_games[all_games.SEASON_ID.str[-4:] == '2025'][:1]

    box = boxscore.BoxScore(game_id=most_recent['GAME_ID'][0]).get_dict()
    print(box['game']['homeTeam']['teamTricode'])
    print(box['game']['homeTeam']['score'])

    summary = {
        'won': None,
        'matchup': most_recent['MATCHUP'][0],
        'game_date': most_recent['GAME_DATE'][0],
        'home_score': box['game']['homeTeam']['score'],
        'away_score': box['game']['awayTeam']['score'],
        'home_team': box['game']['homeTeam']['teamTricode'],
        'away_team': box['game']['awayTeam']['teamTricode']
    }

    if most_recent['WL'][0].upper() == 'W':
        summary['won'] = True
    else:
        summary['won'] = False

    return summary

