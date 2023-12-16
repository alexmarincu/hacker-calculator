import flet as ft
from .App import App


def _main(page: ft.Page) -> None:
    App(page)


def start() -> None:
    ft.app(target=_main, assets_dir="ui/assets")
