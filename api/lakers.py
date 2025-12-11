from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


def did_lakers_win(last_x_games=2):
    lal_id = teams.find_team_by_abbreviation('LAL')['id']
    game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=lal_id)
    all_games = game_finder.get_data_frames()[0]
    most_recent = all_games[all_games.SEASON_ID.str[-4:] == '2025'][:last_x_games]

    list_of_previous_games = []

    for idx, game_id in enumerate(most_recent['GAME_ID']):
        box = boxscore.BoxScore(game_id=game_id).get_dict()

        summary = {
            'won': None,
            'matchup': most_recent['MATCHUP'][idx],
            'matchup_score': None,
            'game_date': most_recent['GAME_DATE'][idx],
            'home_score': box['game']['homeTeam']['score'],
            'away_score': box['game']['awayTeam']['score'],
            'home_team': box['game']['homeTeam']['teamTricode'],
            'away_team': box['game']['awayTeam']['teamTricode'],
        }

        if '@' in summary['matchup']:
            summary['lal_score'] = summary['away_score']
            summary['opp_score'] = summary['home_score']
        else:
            summary['lal_score'] = summary['home_score']
            summary['opp_score'] = summary['away_score']

        if most_recent['WL'][idx] is not None:
            if most_recent['WL'][idx].upper() == 'W':
                summary['won'] = True
            else:
                summary['won'] = False
        else:
            summary['won'] = None

        list_of_previous_games.append(summary)

    for result in list_of_previous_games:
        if result['won'] is not None:
            return result

    # box = boxscore.BoxScore(game_id=most_recent['GAME_ID'][0]).get_dict()
    # print(box['game']['homeTeam']['teamTricode'])
    # print(box['game']['homeTeam']['score'])

    # summary = {
    #     'won': None,
    #     'matchup': most_recent['MATCHUP'][0],
    #     'game_date': most_recent['GAME_DATE'][0],
    #     'home_score': box['game']['homeTeam']['score'],
    #     'away_score': box['game']['awayTeam']['score'],
    #     'home_team': box['game']['homeTeam']['teamTricode'],
    #     'away_team': box['game']['awayTeam']['teamTricode']
    # }

    #
    # if most_recent['WL'][0].upper() == 'W':
    #     summary['won'] = True
    # else:
    #     summary['won'] = False
    #
    # return summary