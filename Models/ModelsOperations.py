from typing import Type

from Models.Player import Player
from Models.TypeSetLeg import TypeSetLeg


class ModelsOperations:
    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_parameters_from_old_game_class(game_class: Type) -> tuple[int, TypeSetLeg, int, TypeSetLeg, list[Player]]:
        try:
            game_n_sets = game_class.n_sets
        except AttributeError:
            game_n_sets = game_class.nSets

        try:
            game_set_type = game_class.set_type
        except AttributeError:
            game_set_type = game_class.setType

        try:
            game_n_legs = game_class.n_legs
        except AttributeError:
            game_n_legs = game_class.nLegs

        try:
            game_leg_type = game_class.leg_type
        except AttributeError:
            game_leg_type = game_class.legType

        try:
            game_initial_player_alignment = game_class.initial_player_alignment
        except AttributeError:
            game_initial_player_alignment = game_class.players

        return game_n_sets, game_set_type, game_n_legs, game_leg_type, game_initial_player_alignment
