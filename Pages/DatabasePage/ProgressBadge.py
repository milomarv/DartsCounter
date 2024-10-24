from typing import Optional
import dash_bootstrap_components as dbc


class ProgressBadge:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(finished: str, additional_text_style: Optional[dict] = None) -> dbc.Badge:
        if not additional_text_style:
            additional_text_style = {}

        if finished == 'finished':
            progress_badge_color = 'success'
            progress_badge_text = 'Finished'
        elif finished == 'in_progress':
            progress_badge_color = 'primary'
            progress_badge_text = 'In Progress'
        else:
            progress_badge_color = 'danger'
            progress_badge_text = 'Not Finished'

        progress_badge = dbc.Badge(
            progress_badge_text,
            color=progress_badge_color,
            style={'font-size': '1rem', **additional_text_style},
        )

        return progress_badge
