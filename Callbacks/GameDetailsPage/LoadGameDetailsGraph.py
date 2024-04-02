import plotly
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class LoadGameDetailsGraph(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('url', 'pathname')
        ]
        self.outputs = [
            Output('game-details-graph-div', 'children')
        ]
        self.states = []

        self.logger.info('Initialized Load Game Details Graph Callback')

    def callback(self, url: str) -> list[dcc.Graph]:
        if url.startswith('/database/game-details/'):
            game_key = url.split('/')[-1]
            game = self.get_last_version_of_game_key(game_key)

            players_set_wins = {p.name: [0] for p in game.initial_player_alignment}
            n_sets = {p.name: [0] for p in game.initial_player_alignment}
            for i_set in game.sets:
                for _i_leg in i_set.legs[:-1]:
                    for p in players_set_wins:
                        players_set_wins[p].append(players_set_wins[p][-1])
                        n_sets[p].append(n_sets[p][-1])
                for p in players_set_wins:
                    last_wins_num = players_set_wins[p][-1]
                    if i_set.winner and i_set.winner.name == p:
                        next_wins_num = last_wins_num + 1
                    else:
                        next_wins_num = last_wins_num
                    players_set_wins[p].append(next_wins_num)
                    n_sets[p].append(n_sets[p][-1] + 1)

            players_leg_wins = {p.name: [0] for p in game.initial_player_alignment}
            for i_set in game.sets:
                for i_leg in i_set.legs:
                    for p in players_leg_wins:
                        last_wins_num = players_leg_wins[p][-1]
                        if i_leg.winner and i_leg.winner.name == p:
                            next_wins_num = last_wins_num + 1
                        else:
                            next_wins_num = last_wins_num
                        players_leg_wins[p].append(next_wins_num)

            data = list()
            color_palette = list(reversed(plotly.colors.qualitative.T10))
            adjusted_color_palette = list()
            for i in range(len(players_set_wins.keys())):
                color_palette_index = i % len(color_palette)
                adjusted_color_palette.append(color_palette[-(color_palette_index + 1)])
            adjusted_color_palette = list(reversed(adjusted_color_palette))

            for i, p in enumerate(reversed(players_leg_wins.keys())):
                data.append(
                    go.Scatter(
                        x = list(range(len(players_leg_wins[p]))),
                        y = players_leg_wins[p],
                        name = p,
                        marker = {
                            'color': adjusted_color_palette[i]
                        },
                        line = {
                            'dash': 'dash'
                        },
                        legendgroup = 'leg',
                        legendgrouptitle = {'text': 'Leg Wins'},
                        hovertemplate =
                        'Leg Wins: <b>%{y}</b>' +
                        '<br>Leg Num: <b>%{x}</b>' +
                        '<br>Win Rate: <b>%{text}%</b>',
                        text = [round((wins / num) * 100, 1) if num else 0 for num, wins in
                                enumerate(players_leg_wins[p])]
                    )
                )

            for i, p in enumerate(reversed(players_set_wins.keys())):
                hover_texts = list()
                for s in range(len(players_set_wins[p])):
                    set_num = n_sets[p][s]
                    player_set_wins = players_set_wins[p][s]
                    if set_num:
                        win_rate = round((player_set_wins / set_num) * 100, 1)
                    else:
                        win_rate = '0.0'
                    hover_text = f'Set Wins: <b>{player_set_wins}</b>' + \
                                 f'<br>Set Num: <b>{set_num}</b>' + \
                                 f'<br>Win Rate: <b>{win_rate} %</b>'
                    hover_texts.append(hover_text)

                data.append(
                    go.Scatter(
                        x = list(range(len(players_set_wins[p]))),
                        y = players_set_wins[p],
                        name = p,
                        marker = {
                            'color': adjusted_color_palette[i]
                        },
                        legendgroup = 'set',
                        legendgrouptitle = {'text': 'Set Wins'},
                        hovertemplate = '%{text}',
                        text = hover_texts
                    )
                )

            graph = dcc.Graph(
                figure = {
                    'data': data,
                    'layout': go.Layout(
                        paper_bgcolor = '#303030',
                        plot_bgcolor = '#303030',
                        font = {
                            'color': 'white'
                        },
                        xaxis = {
                            'gridcolor': '#444444',
                            'title': 'Leg Number',
                            'dtick': 1
                        },
                        yaxis = {
                            'gridcolor': '#444444',
                            'title': 'Amount'
                        },
                        margin = {'t': 40, 'b': 80, 'l': 60, 'r': 40},
                        legend = {'traceorder': 'reversed+grouped'}
                    )
                },
                style = {
                    'height': '100%',
                    'width': '100%'
                }
            )

            return [graph]
        else:
            raise PreventUpdate
