import flet as ft
from .App import App


def _main(page: ft.Page) -> None:

    def onMaximizeButtonClick(_: ft.ControlEvent) -> None:
        page.window_maximized = not page.window_maximized
        page.update()

    def onMinimizeButtonClick(_: ft.ControlEvent) -> None:
        page.window_minimized = True
        page.update()

    def onCloseButtonClick(_: ft.ControlEvent) -> None:
        page.window_close()

    def onInfoButtonClick(_: ft.ControlEvent) -> None:
        page.launch_url('https://github.com/alexmarincu/hacker-calculator')

    page.title = "Hacker Calculator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_min_width = 600
    page.window_min_height = 400
    page.window_width = 600
    page.window_height = 400
    page.window_always_on_top = True
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.appbar = ft.AppBar(
        leading=ft.WindowDragArea(
            content=ft.Container(
                padding=ft.padding.only(left=10),
                content=ft.Image(src="icon.png", scale=0.7)
            ),
        ),
        bgcolor='#202324',
        title=ft.WindowDragArea(
            expand=True,
            content=ft.Text("Hacker Calculator")
        ),
        actions=[
            ft.IconButton(
                icon=ft.icons.INFO,
                on_click=onInfoButtonClick
            ),
            ft.IconButton(
                icon=ft.icons.MINIMIZE,
                scale=0.8,
                style=ft.ButtonStyle(
                    shape={
                        ft.MaterialState.DEFAULT:
                        ft.RoundedRectangleBorder(radius=2),
                    },
                ),
                on_click=onMinimizeButtonClick
            ),
            ft.IconButton(
                icon=ft.icons.SQUARE_OUTLINED,
                scale=0.8,
                style=ft.ButtonStyle(
                    shape={
                        ft.MaterialState.DEFAULT:
                        ft.RoundedRectangleBorder(radius=2),
                    },
                ),
                on_click=onMaximizeButtonClick
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE,
                scale=0.8,
                style=ft.ButtonStyle(
                    shape={
                        ft.MaterialState.DEFAULT:
                        ft.RoundedRectangleBorder(radius=2),
                    },
                ),
                on_click=onCloseButtonClick
            ),
            ft.VerticalDivider(width=10, color=ft.colors.TRANSPARENT)
        ]
    )
    page.fonts = {
        "JetBrainsMono NF":
        "fonts/JetBrainsMonoNerdFont-Regular.ttf",
    }
    page.theme = ft.Theme(font_family="JetBrainsMono NF")
    app = App()

    def onKey(ev: ft.KeyboardEvent):
        if ev.key == "Escape":
            if (app.expressionTextField.current.value != "")\
                    or (not app.expressionTextFieldFocused):
                app.resetInput()
            else:
                page.window_close()

    page.on_keyboard_event = onKey
    page.add(app)
    page.window_center()
    app.expressionTextField.current.focus()


def start() -> None:
    ft.app(target=_main, assets_dir="ui/assets")
